from crispy_forms.layout import Submit
from django import forms
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import DetailView

from projects.filters import ProjectFilter
from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required

from projects.models import Projecttbl, Principalinvestigatortbl
from projects.tables import ProjectTable
from samples.models import Sampletbl
from samples.tables import SampleTable


def index(request):
    projects = Projecttbl.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=projects)
    table = ProjectTable(project_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    context = {'table': table,
               'filter': project_filter}

    template = loader.get_template('projects/index.html')
    return HttpResponse(template.render(context, request))


@login_required
def entry(request):
    form = ProjectForm()

    projects = Projecttbl.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=projects)
    table = ProjectTable(project_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    context = {'form': form,
               'table': table,
               'filter': project_filter}

    template = loader.get_template('projects/entry.html')
    return HttpResponse(template.render(context, request))


@login_required
def submit_project(request):
    # template = loader.get_template('samples/add_sample.html')
    # context = {'samples': Sampletbl.objects.order_by('-id')[:10]}
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            s = Projecttbl()
            s.name = form.cleaned_data['name']

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

            dbprj = Projecttbl.objects.filter(name__exact=s.name,
                                              principal_investigatorid=dbpi).first()
            if not dbprj:
                dbprj = Projecttbl(name=s.name, principal_investigatorid=dbpi)
                dbprj.save()

            s.projectid = dbprj

            s.save()
            return HttpResponseRedirect('/projects/entry')

    return HttpResponse('Failed ')


class ProjectDetailView(DetailView):
    model = Projecttbl

    def get_context_data(self, **kw):
        context = super(ProjectDetailView, self).get_context_data(**kw)

        data = Sampletbl.objects.filter(projectid_id=self.object.id).all()
        table=SampleTable(data)
        table.paginate(page=self.request.GET.get("page", 1), per_page=10)
        context['table'] =table
        return context