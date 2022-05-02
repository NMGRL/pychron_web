from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic import DetailView
from django_tables2 import RequestConfig

from projects.filters import ProjectFilter
from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required

from samples.models import ProjectTbl, PrincipalInvestigatorTbl, Userpiassociationtbl
from projects.tables import ProjectTable, DuplicateProjectTable
from samples.models import SampleTbl
from samples.tables import SampleTable
from util import get_center


def get_project_sample_queryset(request, projectid):
    is_manager = any(g.name == 'manager' for g in request.user.groups.all())

    q = SampleTbl.objects.filter(projectid_id=projectid)
    if not is_manager:
        pis = Userpiassociationtbl.objects.filter(user=request.user.id).values('principal_investigatorid')
        q = SampleTbl.objects.filter(projectid__principal_investigatorid_id__in=pis)

    q = q.order_by('-id')
    return q


def get_project_queryset(request):
    is_manager = any(g.name == 'manager' for g in request.user.groups.all())

    if is_manager:
        projects = ProjectTbl.objects.all()
    else:
        pis = Userpiassociationtbl.objects.filter(user=request.user.id).values('principal_investigatorid')
        projects = ProjectTbl.objects.filter(
            Q(principal_investigatorid__in=pis) | Q(sampletbl__samplesubmittbl__user_id=request.user.id))

    projects = projects.distinct()
    projects = projects.order_by('-id')
    return projects


@login_required
def index(request):
    # projects = ProjectTbl.objects.all()
    projects = get_project_queryset(request)

    project_filter = ProjectFilter(request.GET, queryset=projects)
    table = ProjectTable(project_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    context = {'table': table,
               'filter': project_filter}

    template = loader.get_template('projects/index.html')
    return HttpResponse(template.render(context, request))


@login_required
def entry(request):
    form = ProjectForm()

    projects = ProjectTbl.objects.order_by('-id').all()
    project_filter = ProjectFilter(request.GET, queryset=projects)
    table = ProjectTable(project_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    context = {'form': form,
               'table': table,
               'filter': project_filter}

    template = loader.get_template('projects/entry.html')
    return HttpResponse(template.render(context, request))


@login_required
def submit_project(request):
    # template = loader.get_template('samples/add_sample.html')
    # context = {'samples': SampleTbl.objects.order_by('-id')[:10]}
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            dbpi = form.cleaned_data['principal_investigator']

            if name == '?':
                nir = ProjectTbl.objects.order_by('-id').first()
                name = f'{dbpi.last_name}{nir.id + 1:05n}'

            dbprj = ProjectTbl.objects.filter(name__exact=name,
                                              principal_investigatorid=dbpi).first()
            if not dbprj:
                dbprj = ProjectTbl(name=name, principal_investigatorid=dbpi)
                dbprj.save()

            return HttpResponseRedirect(reverse('projects:entry'))

    return HttpResponse('Failed ')


class ProjectDetailView(DetailView):
    model = ProjectTbl
    template_name = 'projects/projecttbl_detail.html'

    def get_context_data(self, **kw):
        context = super(ProjectDetailView, self).get_context_data(**kw)
        projects = get_project_sample_queryset(self.request, self.object.id)
        table = SampleTable(projects)
        table.paginate(page=self.request.GET.get("page", 1), per_page=20)
        context['table'] = table

        center, records = get_center(projects)
        context['samples'] = records
        context['center'] = center
        return context


@login_required
def cleanup(request):
    duplicate_projects = ProjectTbl.objects.values(
        'name'
    ).annotate(name_count=Count('name')).filter(name_count__gt=1)
    dups = ProjectTbl.objects.filter(name__in=[item['name'] for item in duplicate_projects]).order_by('name')
    table = DuplicateProjectTable(dups)
    context = {'project_table': table}
    template = loader.get_template('projects/cleanup.html')
    RequestConfig(request).configure(table)

    return HttpResponse(template.render(context, request))
