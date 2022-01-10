from dal import autocomplete
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic import DetailView

from materials.filters import MaterialFilter
from materials.forms import MaterialForm
from materials.tables import MaterialTable
from projects.filters import ProjectFilter
from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required

from samples.models import SampleTbl, Materialtbl
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

    form = MaterialForm()
    #
    materials = Materialtbl.objects.all()
    material_filter = MaterialFilter(request.GET, queryset=materials)
    table = MaterialTable(material_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    context = {'form': form,
               'table': table,
               'filter': material_filter}

    template = loader.get_template('materials/entry.html')
    return HttpResponse(template.render(context, request))


@login_required
def submit_material(request):
    # # template = loader.get_template('samples/add_sample.html')
    # # context = {'samples': SampleTbl.objects.order_by('-id')[:10]}
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            s = Materialtbl()
            s.name = form.cleaned_data['name']
            s.grainsize = form.cleaned_data['grainsize']

            s.save()
            return HttpResponseRedirect(reverse('materials:entry'))

    return HttpResponse('Failed ')


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


