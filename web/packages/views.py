import re
from itertools import groupby
from operator import attrgetter, itemgetter, or_

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
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, CreateView
from django_tables2 import RequestConfig


from django.contrib.auth.decorators import login_required

from util import get_center

from packages.models import PackagesTbl, PackageAssociationTbl
from packages.tables import PackageTable, PackageAssociationTable

from packages.forms import PackagesForm


def is_manager(user):
    return any(g.name == 'manager' for g in user.groups.all())


@login_required
def index(request):

    # samples = get_sample_queryset(request)
    # sample_filter = SampleFilter(request.GET, queryset=samples)
    # table = SampleTable(sample_filter.qs)
    # page = request.GET.get('page', 1)
    # table.paginate(page=page, per_page=20)
    #
    # records = [r.record for r in table.paginated_rows]
    # sids = [r.id for r in records]
    # center, records = get_center(records)
    #
    # ts = get_pizza_tracker(sids)
    #
    # tracker = TrackerTable(ts)
    #
    # records = groupby(sorted(records, key=lambda x: x.projectid.id),
    #                   key=lambda x: x.projectid.id)
    #
    # from palettable.cartocolors.qualitative import Vivid_10
    # cs = Vivid_10.hex_colors
    # records = [({'color': ci}, list(gs)) for ((gi, gs), ci) in zip(records, cs)]
    # context = {'table': table,
    #            'filter': sample_filter,
    #            'samples': records,
    #            'center': center,
    #            'tracker': tracker
    #            }
    # RequestConfig(request).configure(table)
    # RequestConfig(request).configure(tracker)

    form = PackagesForm()
    qs = PackagesTbl.objects.order_by('id').all()
    table = PackageTable(qs)
    context = {'table': table,
               'form': form}
    template = loader.get_template('packages/index.html')
    return HttpResponse(template.render(context, request))

#
# def get_sample_queryset(request):
#     if is_manager(request.user):
#         samples = SampleTbl.objects.all()
#     else:
#         samples = SampleTbl.objects.filter(samplesubmittbl__user_id=request.user.id)
#         pis = Userpiassociationtbl.objects.filter(user=request.user.id).values('principal_investigatorid')
#         samples = samples or SampleTbl.objects.filter(projectid__principal_investigatorid__in=pis)
#     samples = samples.order_by('-id')
#     return samples


@login_required
def entry(request):
    # form = SampleForm()
    # psample = request.session.get('sample')
    # if psample:
    #     for k in form.remembered_fields:
    #         v = psample.get(k)
    #         if k == 'project':
    #             v = ProjectTbl.objects.filter(id=v).first()
    #         elif k == 'material':
    #             v = Materialtbl.objects.filter(id=v).first()
    #
    #         form.fields[k].initial = v
    #
    # # projform = ProjectForm()
    #
    # samples = get_sample_queryset(request)
    # sample_filter = SampleFilter(request.GET, queryset=samples)
    # table = SampleTable(sample_filter.qs)
    # table.paginate(page=request.GET.get("page", 1), per_page=20)
    # context = {'form': form,
    #            # 'projform':projform,
    #            'table': table,
    #            'filter': sample_filter}
    context = {}
    template = loader.get_template('packages/entry.html')
    return HttpResponse(template.render(context, request))

#
# PROJECTIONS = {}
#
#
# def set_sample_from_form(s, form):
#     s.name = form.cleaned_data['name']
#     s.materialid = form.cleaned_data['material']
#     s.projectid = form.cleaned_data['project']
#
#     for attr in ('unit', 'location', 'lithology'):
#         setattr(s, attr, form.cleaned_data[attr])
#
#     northing = form.cleaned_data['northing']
#     easting = form.cleaned_data['easting']
#     zone = form.cleaned_data['zone']
#     datum = form.cleaned_data['datum']
#     datum = 'NAD83' if int(datum) == 1 else 'NAD27'
#
#     key = '{}{}'.format(zone, datum)
#     if northing or easting:
#         if key in PROJECTIONS:
#             p = PROJECTIONS[key]
#         else:
#             p = pyproj.Proj(proj='utm', zone=int(zone), datum=datum)
#             PROJECTIONS[key] = p
#
#         lon, lat = p(easting, northing, inverse=True)
#         # s.lon = lon
#         # s.lat = lat
#     else:
#         pointloc = form.cleaned_data['pointloc']
#         if not pointloc:
#             lat = form.cleaned_data['lat']
#             lon = form.cleaned_data['lon']
#         else:
#             lon, lat = pointloc.coords
#
#     if lon or lat:
#         s.lon = lon or 0
#         s.lat = lat or 0
#
#     s.save()


@login_required
def submit_package(request):
    # template = loader.get_template('samples/add_sample.html')
    # context = {'samples': SampleTbl.objects.order_by('-id')[:10]}
    if request.method == 'POST':

        form = PackagesForm(request.POST)

        if form.is_valid():
            s = PackagesTbl()
            s.name = form.cleaned_data['name']
            s.save()

            return HttpResponseRedirect(reverse('packages:index'))

    return HttpResponse('Failed {}'.format(form.errors))


@login_required
def edit_package(request, sample_id):
    if request.method == 'POST':
        pass
    #     s = None
    #     form = SampleForm(request.POST)
    #     if form.is_valid():
    #         # s = SampleTbl()
    #         # s.id = sample_id
    #         sid = sample_id
    #         s = SampleTbl.objects.filter(id=sample_id).first()
    #         set_sample_from_form(s, form)
    #
    #     form = EventsForm(request.POST)
    #     if form.is_valid():
    #         e = EventsTbl()
    #         e.event_type = form.cleaned_data['event_type']
    #         e.user = request.user
    #         if not s:
    #             s = SampleTbl.objects.filter(id=sample_id).first()
    #         e.sample = s
    #         e.message = form.cleaned_data['message']
    #
    #         dt = form.cleaned_data['event_at']
    #         if dt:
    #             e.event_at = dt
    #         else:
    #             e.event_at = timezone.now()
    #         e.save()
    #
    #         for ei in form.cleaned_data['event_values'].split('|'):
    #             if ':' in ei:
    #                 args = ei.split(':')
    #                 name = args[0]
    #                 value = ':'.join(args[1:])
    #                 ev = EventValuesTbl(name=name, value=value, event=e)
    #                 ev.save()
    #
    #         sid = s.id
    # else:
    #     sid = sample_id
    sid = 1
    return HttpResponseRedirect(reverse('packages:detail', args=[sid]))


class PackageDetailView(DetailView):
    model = PackagesTbl

    def get_context_data(self, **kw):
        context = super(PackageDetailView, self).get_context_data(**kw)
        # samples = False
        # if is_manager(self.request.user):
        #     samples = True
        # else:
        #     if not self.request.user.is_anonymous:
        #         pis = Userpiassociationtbl.objects.filter(user=self.request.user.id).values('principal_investigatorid')
        #         samples = SampleTbl.objects.filter(samplesubmittbl__user_id=self.request.user.id)
        #         samples = samples or SampleTbl.objects.filter(projectid__principal_investigatorid__in=pis)
        #         samples = samples.filter(id=self.object.id).first()
        #
        # if samples:
        #     project = self.object.projectid
        #     lat = self.object.lat
        #     lon = self.object.lon
        #     form = SampleForm(initial={
        #         'principal_investigator': project.principal_investigatorid.id,
        #         'project': project,
        #         'material': self.object.materialid,
        #         'name': self.object.name,
        #         'lat': lat,
        #         'lon': lon,
        #         'unit': self.object.unit},
        #         form_action='edit_sample')
        #
        #     context['form'] = form
        #
        #     # events
        #     event_form = EventsForm()
        #     context['event_form'] = event_form
        #     e = EventsTbl.objects.filter(sample_id=self.object.id)
        #     t = SimpleEventsTable(e)
        #     context['events'] = t
        #
        #     # find near by samples
        #     if lat and lon:
        #         ns = SampleTbl.objects.filter(lat__gte=lat - 1,
        #                                       lat__lte=lat + 1,
        #                                       lon__gte=lon - 1,
        #                                       lon__lte=lon + 1,
        #                                       )
        #         ns = ns.filter(~Q(id=self.object.id)).all()
        #         context['nearby_samples'] = ns
        #
        #     data = AnalysisTbl.objects.filter(irradiation_positionid__sampleid_id=self.object.id)
        #     atable = AnalysisTable(data.order_by('-timestamp'))
        #     atable.paginate(page=self.request.GET.get("page", 1), per_page=10)
        #     context['analyses'] = atable
        #     context['nanalyses'] = data.count()
        #
        #     s = data.order_by('timestamp').first()
        #     if s:
        #         context['analyses_start'] = s.dtimestamp
        #     e = data.order_by('-timestamp').first()
        #     if e:
        #         context['analyses_end'] = e.dtimestamp
        qs = PackageAssociationTbl.objects.filter(package__id=self.object.id)
        table = PackageAssociationTable(qs)
        context['table'] = table
        return context

#
# class PrincipalInvestigatorAutocomplete(autocomplete.Select2QuerySetView):
#
#     def get_result_label(self, item):
#         return item.full_name
#
#     def get_selected_result_label(self, item):
#         return self.get_result_label(item)
#
#     def get_queryset(self):
#         qs = PrincipalInvestigatorTbl.objects.order_by('last_name')
#         if self.q:
#             if ',' in self.q:
#                 ln, fi = self.q.split(',')[:2]
#                 qs = qs.filter(Q(last_name__icontains=ln) & Q(first_initial__icontains=fi))
#
#             else:
#                 ln, fi = self.q, self.q
#                 qs = qs.filter(Q(last_name__icontains=ln) | Q(first_initial__icontains=fi))
#
#         return qs.all()
#
#
# class MaterialAutocomplete(autocomplete.Select2QuerySetView):
#
#     def get_result_label(self, item):
#         return item.full_name
#
#     def get_selected_result_label(self, item):
#         return self.get_result_label(item)
#
#     def get_queryset(self):
#         qs = Materialtbl.objects.order_by('name').all()
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#         return qs
#
#
# class ProjectAutocomplete(autocomplete.Select2QuerySetView):
#
#     def get_result_label(self, item):
#         return item.piname
#
#     def get_selected_result_label(self, item):
#         return item.piname
#
#     def get_queryset(self):
#         # if self.request.user.groups.first().name in ('manager',)
#         # else:
#         qs = ProjectTbl.objects.order_by('principal_investigatorid__last_name').all()
#
#         p = self.forwarded.get('principal_investigator')
#         if p:
#             qs = qs.filter(principal_investigatorid__id=p)
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs
