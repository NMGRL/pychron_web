# from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
# from django.views.generic import DetailView
#
# from projects.filters import ProjectFilter
# from projects.forms import ProjectForm
# from django.contrib.auth.decorators import login_required
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
