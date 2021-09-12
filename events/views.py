# from itertools import groupby
#
# import django_tables2
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.shortcuts import render
#
# # Create your views here.
# from django.template import loader
# import django_tables2 as tables
#
# from events.models import EventsTbl
# from samples.filters import SampleFilter
# from samples.views import get_sample_queryset
# from util import get_center
#
#
#
# @login_required
# def index(request):
#     samples = get_sample_queryset(request)
#     sample_filter = SampleFilter(request.GET, queryset=samples)
#     table = EventSampleTable(sample_filter.qs)
#     page = request.GET.get('page', 1)
#     table.paginate(page=page, per_page=20)
#
#     records = [r.record for r in table.paginated_rows]
#     center, records = get_center(records)
#
#     records = groupby(sorted(records, key=lambda x: x.projectid.id),
#                       key=lambda x: x.projectid.id)
#
#     from palettable.cartocolors.qualitative import Vivid_10
#     cs = Vivid_10.hex_colors
#     records = [({'color': ci}, list(gs)) for ((gi, gs), ci) in zip(records, cs)]
#
#     evts = EventsTbl.objects.all()
#     eventstable = EventsTable(evts)
#
#     context = {'table': table,
#                'filter': sample_filter,
#                'samples': records,
#                'center': center,
#                'events': eventstable
#                }
#
#     template = loader.get_template('events/index.html')
#     return HttpResponse(template.render(context, request))
