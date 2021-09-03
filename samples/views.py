from crispy_forms.layout import Submit
from django import forms
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from samples.filters import SampleFilter
from samples.forms import SampleForm
from samples.models import Sampletbl, Materialtbl, Projecttbl, Principalinvestigatortbl
from samples.tables import SampleTable


def index(request):
    samples = Sampletbl.objects.all()
    sample_filter = SampleFilter(request.GET, queryset=samples)
    table = SampleTable(sample_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    context = {'table': table,
               'filter': sample_filter}

    template = loader.get_template('samples/index.html')
    return HttpResponse(template.render(context, request))


from django.contrib.auth.decorators import login_required

@login_required
def entry(request):
    form = SampleForm()

    samples = Sampletbl.objects.all()
    sample_filter = SampleFilter(request.GET, queryset=samples)
    table = SampleTable(sample_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    context = {'sample_form': form,
               'table': table,
               'filter': sample_filter}

    template = loader.get_template('samples/entry.html')
    return HttpResponse(template.render(context, request))


def submit_sample(request):
    # template = loader.get_template('samples/add_sample.html')
    # context = {'samples': Sampletbl.objects.order_by('-id')[:10]}
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            s = Sampletbl()
            s.name = form.cleaned_data['name']

            material = form.cleaned_data['material']
            gs = form.cleaned_data['grainsize']
            dbmat = Materialtbl.objects.filter(name__exact=material,
                                               grainsize__exact=gs).first()
            if not dbmat:
                dbmat = Materialtbl(grainsize=gs, name=material)
                dbmat.save()

            s.materialid = dbmat

            project = form.cleaned_data['project']
            pi = form.cleaned_data['principal_investigator']
            pi = pi.strip()
            if ',' in pi:
                lastname, firstinitial = pi.split(',')
                dbpi = Principalinvestigatortbl.objects.filter(last_name__exact=lastname.strip(),
                                                               first_initial__exact=firstinitial.strip()).first()
                if not dbpi:
                    dbpi = Principalinvestigatortbl(last_name=lastname, first_initial=firstinitial)
                    dbpi.save()
            else:
                dbpi = Principalinvestigatortbl.objects.filter(last_name__exact=pi).first()
                if not dbpi:
                    dbpi = Principalinvestigatortbl(last_name=pi)

            dbprj = Projecttbl.objects.filter(name__exact=project,
                                              principal_investigatorid=dbpi).first()
            if not dbprj:
                dbprj = Projecttbl(name=project, principal_investigatorid=dbpi)
                dbprj.save()

            s.projectid = dbprj

            s.save()
            return HttpResponseRedirect('/samples/entry')

    return HttpResponse('Failed ')
