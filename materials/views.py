from dal import autocomplete
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import DetailView

from materials.filters import MaterialFilter
from materials.tables import MaterialTable
from projects.filters import ProjectFilter
from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required

from samples.models import ProjectTbl, PrincipalInvestigatorTbl, Materialtbl
from projects.tables import ProjectTable
from samples.models import SampleTbl
from samples.tables import SampleTable


def index(request):
    materials = Materialtbl.objects.all()
    material_filter = MaterialFilter(request.GET, queryset=materials)
    table = MaterialTable(material_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    context = {'table': table,
               'filter': material_filter}

    template = loader.get_template('materials/index.html')
    return HttpResponse(template.render(context, request))


@login_required
def entry(request):
    pass
    # form = ProjectForm()
    #
    # projects = ProjectTbl.objects.all()
    # project_filter = ProjectFilter(request.GET, queryset=projects)
    # table = ProjectTable(project_filter.qs)
    # table.paginate(page=request.GET.get("page", 1), per_page=10)
    # context = {'form': form,
    #            'table': table,
    #            'filter': project_filter}
    #
    # template = loader.get_template('projects/entry.html')
    # return HttpResponse(template.render(context, request))


@login_required
def submit_material(request):
    pass
    # # template = loader.get_template('samples/add_sample.html')
    # # context = {'samples': SampleTbl.objects.order_by('-id')[:10]}
    # if request.method == 'POST':
    #     form = ProjectForm(request.POST)
    #     if form.is_valid():
    #         s = ProjectTbl()
    #         s.name = form.cleaned_data['name']
    #
    #         pi = form.cleaned_data['principal_investigator']
    #         pi = pi.strip()
    #         if ',' in pi:
    #             lastname, firstinitial = pi.split(',')
    #             dbpi = PrincipalInvestigatorTbl.objects.filter(last_name__exact=lastname.strip(),
    #                                                            first_initial__exact=firstinitial.strip()).first()
    #             if not dbpi:
    #                 dbpi = PrincipalInvestigatorTbl(last_name=lastname, first_initial=firstinitial)
    #                 dbpi.save()
    #         else:
    #             dbpi = PrincipalInvestigatorTbl.objects.filter(last_name__exact=pi).first()
    #             if not dbpi:
    #                 dbpi = PrincipalInvestigatorTbl(last_name=pi)
    #
    #         dbprj = ProjectTbl.objects.filter(name__exact=s.name,
    #                                           principal_investigatorid=dbpi).first()
    #         if not dbprj:
    #             dbprj = ProjectTbl(name=s.name, principal_investigatorid=dbpi)
    #             dbprj.save()
    #
    #         s.projectid = dbprj
    #
    #         s.save()
    #         return HttpResponseRedirect('/projects/entry')
    #
    # return HttpResponse('Failed ')


class MaterialDetailView(DetailView):
    model = Materialtbl
    template_name = 'materials/materialtbl_detail.html'

    def get_context_data(self, **kw):
        context = super(MaterialDetailView, self).get_context_data(**kw)

        data = SampleTbl.objects.filter(materialid_id=self.object.id).order_by('-id').all()
        table = SampleTable(data)
        table.paginate(page=self.request.GET.get("page", 1), per_page=20)
        context['table'] = table
        return context


