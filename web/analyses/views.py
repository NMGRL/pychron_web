import base64
import json
import os.path
import struct

from bokeh.embed import components
from bokeh.plotting import figure
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# from django.views.generic import DetailView
#
# from projects.filters import ProjectFilter
# from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from git import Repo
from git.exc import GitCommandError

#
# from samples.models import ProjectTbl, PrincipalInvestigatorTbl
# from projects.tables import ProjectTable
# from samples.models import SampleTbl
# from samples.tables import SampleTable
#
#
# def get_project_queryset(request):
#     is_manager = any(g.name == 'manager' for g in request.user.groups.all())
#
#     if is_manager:
#         projects = ProjectTbl.objects.all()
#     else:
#         projects = ProjectTbl.objects.filter(sampletbl__samplesubmittbl__user_id=request.user.id)
#
#     projects = projects.order_by('-id')
#     return projects
#
#
# @login_required
# def index(request):
#     # projects = ProjectTbl.objects.all()
#     projects = get_project_queryset(request)
#
#     project_filter = ProjectFilter(request.GET, queryset=projects)
#     table = ProjectTable(project_filter.qs)
#     table.paginate(page=request.GET.get("page", 1), per_page=20)
#     context = {'table': table,
#                'filter': project_filter}
#
#     template = loader.get_template('projects/index.html')
#     return HttpResponse(template.render(context, request))
#
#
# @login_required
# def entry(request):
#     form = ProjectForm()
#
#     projects = ProjectTbl.objects.all()
#     project_filter = ProjectFilter(request.GET, queryset=projects)
#     table = ProjectTable(project_filter.qs)
#     table.paginate(page=request.GET.get("page", 1), per_page=20)
#     context = {'form': form,
#                'table': table,
#                'filter': project_filter}
#
#     template = loader.get_template('projects/entry.html')
#     return HttpResponse(template.render(context, request))
#
#
# @login_required
# def submit_project(request):
#     # template = loader.get_template('samples/add_sample.html')
#     # context = {'samples': SampleTbl.objects.order_by('-id')[:10]}
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             s = ProjectTbl()
#             s.name = form.cleaned_data['name']
#
#             pi = form.cleaned_data['principal_investigator']
#             pi = pi.strip()
#             if ',' in pi:
#                 lastname, firstinitial = pi.split(',')
#                 dbpi = PrincipalInvestigatorTbl.objects.filter(last_name__exact=lastname.strip(),
#                                                                first_initial__exact=firstinitial.strip()).first()
#                 if not dbpi:
#                     dbpi = PrincipalInvestigatorTbl(last_name=lastname, first_initial=firstinitial)
#                     dbpi.save()
#             else:
#                 dbpi = PrincipalInvestigatorTbl.objects.filter(last_name__exact=pi).first()
#                 if not dbpi:
#                     dbpi = PrincipalInvestigatorTbl(last_name=pi)
#
#             dbprj = ProjectTbl.objects.filter(name__exact=s.name,
#                                               principal_investigatorid=dbpi).first()
#             if not dbprj:
#                 dbprj = ProjectTbl(name=s.name, principal_investigatorid=dbpi)
#                 dbprj.save()
#
#             s.projectid = dbprj
#
#             s.save()
#             return HttpResponseRedirect('/projects/entry')
#
#     return HttpResponse('Failed ')
#
#
# class ProjectDetailView(DetailView):
#     model = ProjectTbl
#     template_name = 'projects/projecttbl_detail.html'
#
#     def get_context_data(self, **kw):
#         context = super(ProjectDetailView, self).get_context_data(**kw)
#
#         data = SampleTbl.objects.filter(projectid_id=self.object.id).order_by('-id').all()
#         table = SampleTable(data)
#         table.paginate(page=self.request.GET.get("page", 1), per_page=20)
#         context['table'] = table
#         return context
from analyses.models import AnalysisTbl

from analyses.models import RepositoryAssociationTbl


@login_required
def recent_regressions(request):
    # get the last n analyses
    # group by repository identifier
    # clone each identifier
    # extract regressions
    # plot each isotope

    context = {}
    analyses = AnalysisTbl.objects.order_by('-id')[:2]
    # repos = {ai.repository for ai in analyses}
    repo_associations = RepositoryAssociationTbl.objects.filter(analysisID__in=[a.id for a in analyses])
    repos = {r.repository for r in repo_associations}

    # repos = ['Irradiation-NM-321', ]
    for r in repos:
        clone_repo(r)

    for assoc in repo_associations:
        plot_assoc(context, assoc)
    # for repo, uuid in (('Irradiation-NM-321', '0a0ff3c4-ef60-4f26-8241-298c57558916'),):
    #     plot_analyses(context, repo, uuid)
    # for a in analyses:
    #     plot_analyses(context, )
    template = loader.get_template('analyses/recent.html')
    return HttpResponse(template.render(context, request))


def unpack(blob, fmt, step=8):
    blob = base64.b64decode(blob)
    return list(
        zip(
            *[
                struct.unpack(fmt, blob[i: i + step])
                for i in range(0, len(blob), step)
            ]
        )
    )


def plot_assoc(context, assoc):
    repo = assoc.repository
    ans = assoc.analysisID
    uuid = ans.uuid
    if settings.ANALYSES_DEBUG:
        uuid = '0a0ff3c4-ef60-4f26-8241-298c57558916'
        repo = 'Irradiation-NM-321'
    plot_analysis(context, repo, uuid)


def plot_analysis(context, repo, uuid):
    root, tail = uuid[:2], uuid[2:]
    path = os.path.join('/home/app', repo, root, f'{tail}.json')
    with open(path, 'r') as rfile:
        jobj = json.load(rfile)
        print(jobj.keys())
    runid = f'{jobj["identifier"]}-{jobj["aliquot"]}{jobj["increment"] or ""}'
    rows = [('Irradiation', f'{jobj["irradiation"]} {jobj["irradiation_level"]}{jobj["irradiation_position"]}'),
            ('RunID', runid)]

    rows.extend([(k, jobj[k] or '') for k in ('project',
                                              'sample',
                                              'timestamp',
                                              'comment',
                                              'note',
                                              'experiment_queue_name',
                                              'measurement',
                                              'extraction'
                                              )])
    # context['table'] = rows
    path = os.path.join('/home/app', repo, root, '.data', f'{tail}.dat.json')
    with open(path, 'r') as rfile:
        dataobj = json.load(rfile)
        # x = [1,2,3,4]
        # y = [1,23,123,31]
        signals = dataobj['signals']
        figures = []
        fmt = dataobj['format']
        for si in signals:
            x, y = unpack(si['blob'], fmt)

            plot = figure(y_axis_label=si['isotope'],
                          height=150)
            plot.scatter(x, y)
            script, div = components(plot)
            figures.append((script, div))

        analyses = context.get('analyses', [])
        analyses.append({'runid': runid, 'figures': figures, 'table': rows})
        context['analyses'] = analyses


def clone_repo(name):
    if settings.ANALYSES_DEBUG:
        name = 'Irradiation-NM-321'

    organization = settings.PYCHRON_DATA_ORGANIZATION
    url = f'https://github.com/{organization}/{name}'
    print(f'clone repo {name} url={url}')
    repo_path = f'/home/app/{name}'
    if not os.path.isdir(repo_path):
        try:
            Repo.clone_from(url, repo_path, depth=10)
            print(f'repo {name} cloned')
        except GitCommandError as e:
            print(e)
    else:
        print('repo already exists. pulling')
        repo = Repo(repo_path)
        o = repo.remotes.origin
        o.fetch()
        o.pull()
