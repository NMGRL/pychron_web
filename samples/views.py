import re
from itertools import groupby
from operator import attrgetter, itemgetter

import palettable.scientific.scientific
import pyproj
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.db.models import Q
from django.shortcuts import render
from django.contrib.gis.geos.point import Point

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import DetailView

from analyses.models import Analysistbl, Irradiationtbl
from analyses.tables import AnalysisTable
from events.forms import EventsForm
from events.models import EventsTbl
from events.tables import EventsTable, TrackerTable
from samples.filters import SampleFilter
from samples.forms import SampleForm
from samples.models import SampleTbl, Materialtbl, Samplesubmittbl, Userpiassociationtbl
from samples.tables import SampleTable
from samples.models import ProjectTbl, Principalinvestigatortbl

from django.contrib.auth.decorators import login_required

from util import get_center


def is_manager(user):
    return any(g.name == 'manager' for g in user.groups.all())


def get_event(es, tag):
    for e in es:
        if e['event_type__name'] == tag:
            return e


def event(es, tag):
    e = get_event(es, tag)
    s = ''
    if e:
        t = e['event_at'].strftime('%m/%d/%Y %H:%M')
        s = f'{t} {e["user__username"]}'

    return s


@login_required
def index(request):
    samples = get_sample_queryset(request)
    sample_filter = SampleFilter(request.GET, queryset=samples)
    table = SampleTable(sample_filter.qs)
    page = request.GET.get('page', 1)
    table.paginate(page=page, per_page=20)

    records = [r.record for r in table.paginated_rows]
    sids = [r.id for r in records]
    center, records = get_center(records)

    evts = EventsTbl.objects.filter(sample_id__in=sids).order_by('sample_id').values('sample_id',
                                                                                     'sample__name',
                                                                                     'event_type__name',
                                                                                     'event_at',
                                                                                     'user__username')
    ts = []
    for s, es in groupby(evts, key=itemgetter('sample_id')):
        ans = []

        irradiations = Irradiationtbl.objects
        irradiations = irradiations.filter(leveltbl__irradiationpositiontbl__sampleid=s,
                                           leveltbl__irradiationpositiontbl__identifier__isnull=False)
        irradiations = irradiations.values('name', 'leveltbl__name',
                                           'leveltbl__irradiationpositiontbl__position',
                                           'leveltbl__irradiationpositiontbl__identifier')

        if irradiations:
            ans = Analysistbl.objects.filter(irradiation_positionid__sampleid=s).order_by('timestamp').first()

        es = list(es)
        istring = ','.join(
            ['{}{}{} {}'.format(i['name'], i['leveltbl__name'], i['leveltbl__irradiationpositiontbl__position'],
                                i['leveltbl__irradiationpositiontbl__identifier']) for i in irradiations])

        istring = f'{istring[:30]}...' if len(istring) > 30 else istring
        t = {'sample': es[0]['sample__name'],
             'received': event(es, 'received') or False,
             'prepped': event(es, 'prepped') or False,

             'irradiated': istring or False,
             'analyzed': ans.dtimestamp if ans else False
             }
        ts.append(t)

    tracker = TrackerTable(ts)

    records = groupby(sorted(records, key=lambda x: x.projectid.id),
                      key=lambda x: x.projectid.id)

    from palettable.cartocolors.qualitative import Vivid_10
    cs = Vivid_10.hex_colors
    records = [({'color': ci}, list(gs)) for ((gi, gs), ci) in zip(records, cs)]
    context = {'table': table,
               'filter': sample_filter,
               'samples': records,
               'center': center,
               'tracker': tracker
               }

    template = loader.get_template('samples/index.html')
    return HttpResponse(template.render(context, request))


def get_sample_queryset(request):
    if is_manager(request.user):
        samples = SampleTbl.objects.all()
    else:
        samples = SampleTbl.objects.filter(samplesubmittbl__user_id=request.user.id)
        pis = Userpiassociationtbl.objects.filter(user=request.user.id).values('principal_investigatorid')
        samples = samples or SampleTbl.objects.filter(projectid__principal_investigatorid__in=pis)
    samples = samples.order_by('-id')
    return samples


@login_required
def entry(request):
    form = SampleForm()

    samples = get_sample_queryset(request)
    sample_filter = SampleFilter(request.GET, queryset=samples)
    table = SampleTable(sample_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    context = {'form': form,
               'table': table,
               'filter': sample_filter}

    template = loader.get_template('samples/entry.html')
    return HttpResponse(template.render(context, request))


PROJECTIONS = {}


@login_required
def submit_sample(request):
    # template = loader.get_template('samples/add_sample.html')
    # context = {'samples': SampleTbl.objects.order_by('-id')[:10]}
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            s = SampleTbl()
            s.name = form.cleaned_data['name']
            material = form.cleaned_data['material']

            s.materialid = material
            project = form.cleaned_data['project']

            s.projectid = project
            # for v in ('unit', 'lat', 'lon'):
            #     setattr(s, v, form.cleaned_data[v])
            s.unit = form.cleaned_data['unit']
            northing = form.cleaned_data['northing']
            easting = form.cleaned_data['easting']
            zone = form.cleaned_data['zone']
            datum = None
            lat, lon = None, None
            if northing or easting:
                if zone in PROJECTIONS:
                    p = PROJECTIONS[zone]
                else:
                    kw = {}
                    if datum:
                        kw['datum'] = datum
                    p = pyproj.Proj(proj='utm', zone=int(zone), **kw)

                lon, lat = p(easting, northing, inverse=True)
                # s.lon = lon
                # s.lat = lat
            else:
                pointloc = form.cleaned_data['pointloc']
                lon, lat = pointloc.coords

            if lon or lat:
                s.lon = lon
                s.lat = lat

            s.save()

            ss = Samplesubmittbl()
            ss.user = request.user
            ss.sample = s
            ss.save()

            return HttpResponseRedirect('/samples/entry')

    return HttpResponse('Failed {}'.format(form.errors))


@login_required
def edit_sample(request, sample_id):
    if request.method == 'POST':
        s = None
        form = SampleForm(request.POST)
        if form.is_valid():
            s = SampleTbl()
            s.id = sample_id
            s.name = form.cleaned_data['name']

            material = form.cleaned_data['material']
            s.materialid = material

            project = form.cleaned_data['project']
            s.projectid = project

            for attr in ('unit', 'lat', 'lon'):
                setattr(s, attr, form.cleaned_data[attr])

            s.save()

        form = EventsForm(request.POST)
        if form.is_valid():
            e = EventsTbl()
            e.event_type = form.cleaned_data['event_type']
            e.user = request.user
            if not s:
                s = SampleTbl.objects.filter(id=sample_id).first()
            e.sample = s
            e.message = form.cleaned_data['message']

            dt = form.cleaned_data['event_at']
            e.event_at = dt
            e.save()

    return HttpResponseRedirect(f'/samples/{s.id}/')


class SampleDetailView(DetailView):
    model = SampleTbl

    def get_context_data(self, **kw):
        context = super(SampleDetailView, self).get_context_data(**kw)
        samples = False
        if is_manager(self.request.user):
            samples = True
        else:
            if not self.request.user.is_anonymous:
                pis = Userpiassociationtbl.objects.filter(user=self.request.user.id).values('principal_investigatorid')
                samples = SampleTbl.objects.filter(samplesubmittbl__user_id=self.request.user.id)
                samples = samples or SampleTbl.objects.filter(projectid__principal_investigatorid__in=pis)
                samples = samples.filter(id=self.object.id).first()

        if samples:
            project = self.object.projectid
            lat = self.object.lat
            lon = self.object.lon
            form = SampleForm(initial={
                'principal_investigator': project.principal_investigatorid.id,
                'project': project,
                'material': self.object.materialid,
                'name': self.object.name,
                'lat': lat,
                'lon': lon,
                'unit': self.object.unit})

            context['form'] = form

            # events
            event_form = EventsForm()
            context['event_form'] = event_form
            e = EventsTbl.objects.filter(sample_id=self.object.id)
            t = EventsTable(e)
            context['events'] = t

            # find near by samples
            if lat and lon:

                ns = SampleTbl.objects.filter(lat__gte=lat - 1,
                                              lat__lte=lat + 1,
                                              lon__gte=lon - 1,
                                              lon__lte=lon + 1,
                                              )
                ns = ns.filter(~Q(id=self.object.id)).all()

                print('asdf', ns, ns.count())
                for ni in ns:
                    print(ni, ni.lat, ni.lon)
                context['nearby_samples'] = ns

            data = Analysistbl.objects.filter(irradiation_positionid__sampleid_id=self.object.id)
            atable = AnalysisTable(data.order_by('-timestamp'))
            atable.paginate(page=self.request.GET.get("page", 1), per_page=10)
            context['analyses'] = atable
            context['nanalyses'] = data.count()

            s = data.order_by('timestamp').first()
            if s:
                context['analyses_start'] = s.dtimestamp
            e = data.order_by('-timestamp').first()
            if e:
                context['analyses_end'] = e.dtimestamp

        return context


class PrincipalInvestigatorAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return item.full_name

    def get_selected_result_label(self, item):
        return self.get_result_label(item)

    def get_queryset(self):
        qs = Principalinvestigatortbl.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class MaterialAutocomplete(autocomplete.Select2QuerySetView):

    def get_result_label(self, item):
        return item.full_name

    def get_selected_result_label(self, item):
        return self.get_result_label(item)

    def get_queryset(self):
        qs = Materialtbl.objects.order_by('name').all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ProjectAutocomplete(autocomplete.Select2QuerySetView):

    def get_result_label(self, item):
        return item.piname

    def get_selected_result_label(self, item):
        return item.piname

    def get_queryset(self):
        # if self.request.user.groups.first().name in ('manager',)
        # else:
        qs = ProjectTbl.objects.order_by('principal_investigatorid__last_name').all()

        p = self.forwarded.get('principal_investigator')
        if p:
            qs = qs.filter(principal_investigatorid__id=p)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
