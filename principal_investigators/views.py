from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import DetailView

from materials.filters import MaterialFilter
from materials.tables import MaterialTable
from principal_investigators.filters import PrincipalInvestigatorsFilter
from principal_investigators.forms import PrincipalInvestigatorForm
from principal_investigators.tables import PrincipalInvestigatorsTable
from projects.filters import ProjectFilter
from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required

from samples.models import Projecttbl, Principalinvestigatortbl, Materialtbl
from projects.tables import ProjectTable
from samples.models import Sampletbl
from samples.tables import SampleTable

@login_required
def index(request):
    pis = Principalinvestigatortbl.objects.all()
    tfilter = PrincipalInvestigatorsFilter(request.GET, queryset=pis)
    table = PrincipalInvestigatorsTable(tfilter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    context = {'table': table,
               'filter': tfilter}

    template = loader.get_template('principal_investigators/index.html')
    return HttpResponse(template.render(context, request))


@login_required
def entry(request):

    form = PrincipalInvestigatorForm()

    projects = Principalinvestigatortbl.objects.all()
    tfilter = PrincipalInvestigatorsFilter(request.GET, queryset=projects)
    table = PrincipalInvestigatorsTable(tfilter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    context = {'form': form,
               'table': table,
               'filter': tfilter}

    template = loader.get_template('principal_investigators/entry.html')
    return HttpResponse(template.render(context, request))


@login_required
def submit_principal_investigator(request):
    pass
    # # template = loader.get_template('samples/add_sample.html')
    # # context = {'samples': Sampletbl.objects.order_by('-id')[:10]}
    # if request.method == 'POST':
    #     form = ProjectForm(request.POST)
    #     if form.is_valid():
    #         s = Projecttbl()
    #         s.name = form.cleaned_data['name']
    #
    #         pi = form.cleaned_data['principal_investigator']
    #         pi = pi.strip()
    #         if ',' in pi:
    #             lastname, firstinitial = pi.split(',')
    #             dbpi = Principalinvestigatortbl.objects.filter(last_name__exact=lastname.strip(),
    #                                                            first_initial__exact=firstinitial.strip()).first()
    #             if not dbpi:
    #                 dbpi = Principalinvestigatortbl(last_name=lastname, first_initial=firstinitial)
    #                 dbpi.save()
    #         else:
    #             dbpi = Principalinvestigatortbl.objects.filter(last_name__exact=pi).first()
    #             if not dbpi:
    #                 dbpi = Principalinvestigatortbl(last_name=pi)
    #
    #         dbprj = Projecttbl.objects.filter(name__exact=s.name,
    #                                           principal_investigatorid=dbpi).first()
    #         if not dbprj:
    #             dbprj = Projecttbl(name=s.name, principal_investigatorid=dbpi)
    #             dbprj.save()
    #
    #         s.projectid = dbprj
    #
    #         s.save()
    #         return HttpResponseRedirect('/projects/entry')
    #
    # return HttpResponse('Failed ')


class PrincipalInvestigatorDetailView(DetailView):
    model = Principalinvestigatortbl
    template_name = 'principal_investigators/principalinvestigatortbl_detail.html'

    def get_context_data(self, **kw):
        context = super(PrincipalInvestigatorDetailView, self).get_context_data(**kw)

        data = Projecttbl.objects.filter(principal_investigatorid_id=self.object.id).all()
        table = ProjectTable(data)
        table.paginate(page=self.request.GET.get("page", 1), per_page=20)
        context['table'] = table
        return context
