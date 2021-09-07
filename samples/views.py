import re

from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import DetailView

from samples.filters import SampleFilter
from samples.forms import SampleForm
from samples.models import Sampletbl, Materialtbl, Samplesubmittbl
from samples.tables import SampleTable
from samples.models import Projecttbl, Principalinvestigatortbl

from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    samples = get_sample_queryset(request)
    sample_filter = SampleFilter(request.GET, queryset=samples)
    table = SampleTable(sample_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    context = {'table': table,
               'filter': sample_filter}

    template = loader.get_template('samples/index.html')
    return HttpResponse(template.render(context, request))


def get_sample_queryset(request):
    is_manager = any(g.name == 'manager' for g in request.user.groups.all())

    if is_manager:
        samples = Sampletbl.objects.all()
    else:
        samples = Sampletbl.objects.filter(samplesubmittbl__user_id=request.user.id)

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


@login_required
def submit_sample(request):
    # template = loader.get_template('samples/add_sample.html')
    # context = {'samples': Sampletbl.objects.order_by('-id')[:10]}
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            s = Sampletbl()
            s.name = form.cleaned_data['name']

            material = form.cleaned_data['material']
            # print('masdf', material)
            # gs = form.cleaned_data['grainsize']
            # dbmat = Materialtbl.objects.filter(name__exact=material,
            #                                    grainsize__exact=gs).first()
            # if not dbmat:
            #     dbmat = Materialtbl(grainsize=gs, name=material)
            #     dbmat.save()

            s.materialid = material

            project = form.cleaned_data['project']

            s.projectid = project

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
        form = SampleForm(request.POST)
        if form.is_valid():
            s = Sampletbl()
            s.id = sample_id
            s.name = form.cleaned_data['name']

            material = form.cleaned_data['material']
            s.materialid = material

            project = form.cleaned_data['project']
            s.projectid = project

            for attr in ('unit', 'lat', 'lon'):
                print(attr, form.cleaned_data[attr])
                setattr(s, attr, form.cleaned_data[attr])

            s.save()

            return HttpResponseRedirect(f'/samples/{s.id}/')


class SampleDetailView(DetailView):
    model = Sampletbl

    def get_context_data(self, **kw):
        context = super(SampleDetailView, self).get_context_data(**kw)
        project = self.object.projectid

        form = SampleForm(initial={'principal_investigator': project.principal_investigatorid.id,
                                   'project': project,
                                   'material': self.object.materialid,
                                   'name': self.object.name,
                                   'unit': self.object.unit})

        context['form'] = form
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
        qs = Materialtbl.objects.all()

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
        qs = Projecttbl.objects.all()

        p = self.forwarded.get('principal_investigator')
        if p:
            qs = qs.filter(principal_investigatorid__id=p)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
