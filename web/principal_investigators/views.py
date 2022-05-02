from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.generic import DetailView
from django_tables2 import MultiTableMixin, RequestConfig

from materials.filters import MaterialFilter
from materials.tables import MaterialTable
from principal_investigators.filters import PrincipalInvestigatorsFilter
from principal_investigators.forms import PrincipalInvestigatorForm
from principal_investigators.tables import PrincipalInvestigatorsTable
from projects.filters import ProjectFilter
from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required

from samples.models import ProjectTbl, PrincipalInvestigatorTbl, Materialtbl, Userpiassociationtbl
from projects.tables import ProjectTable
from samples.models import SampleTbl
from samples.tables import SampleTable


def get_principal_investigator_queryset(request):
    is_manager = any(g.name == 'manager' for g in request.user.groups.all())

    if is_manager:
        pis = PrincipalInvestigatorTbl.objects.all()
    else:
        apis = Userpiassociationtbl.objects.filter(user=request.user.id).values('principal_investigatorid').all()
        pis = PrincipalInvestigatorTbl.objects.filter(Q(projecttbl__sampletbl__samplesubmittbl__user_id=request.user.id)|
                                                      Q(id__in=apis),
                                                      )
    pis = pis.distinct()
    pis = pis.order_by('-id')
    return pis


def make_context(request):
    pis = get_principal_investigator_queryset(request)
    tfilter = PrincipalInvestigatorsFilter(request.GET, queryset=pis)
    table = PrincipalInvestigatorsTable(tfilter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    context = {'table': table,
               'filter': tfilter}
    return context

@login_required
def index(request):
    context = make_context(request)

    template = loader.get_template('principal_investigators/index.html')
    return HttpResponse(template.render(context, request))


@login_required
def entry(request):
    form = PrincipalInvestigatorForm()

    projects = PrincipalInvestigatorTbl.objects.order_by('-id').all()
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
    if request.method == 'POST':
        form = PrincipalInvestigatorForm(request.POST)
        if form.is_valid():
            pi = form.cleaned_data['name'].strip()
            if ',' in pi:
                lastname, firstinitial = pi.split(',')
                dbpi = PrincipalInvestigatorTbl.objects.filter(last_name__exact=lastname.strip(),
                                                           first_initial__exact=firstinitial.strip()).first()
                if not dbpi:
                    dbpi = PrincipalInvestigatorTbl(last_name=lastname, first_initial=firstinitial)
            else:
                dbpi = PrincipalInvestigatorTbl.objects.filter(last_name__exact=pi).first()
                if not dbpi:
                    dbpi = PrincipalInvestigatorTbl(last_name=pi)

            dbpi.save()
        else:
            ctx = make_context(request)
            ctx['form'] = form
            return render(request, 'principal_investigators/entry.html', ctx)

    return HttpResponseRedirect(reverse('principal_investigators:entry'))


class PrincipalInvestigatorDetailView(DetailView):
    model = PrincipalInvestigatorTbl
    template_name = 'principal_investigators/principalinvestigatortbl_detail.html'

    def get_context_data(self, **kw):
        context = super(PrincipalInvestigatorDetailView, self).get_context_data(**kw)

        data = ProjectTbl.objects.filter(principal_investigatorid=self.object).all()
        table = ProjectTable(data)
        table.prefix = 'project'
        RequestConfig(self.request, paginate={'per_page': 20}).configure(table)
        context['projects'] = table

        data = SampleTbl.objects.filter(projectid__principal_investigatorid=self.object).all()
        table = SampleTable(data)
        table.prefix = 'sample'
        RequestConfig(self.request, paginate={'per_page': 20}).configure(table)
        context['samples'] = table
        return context
