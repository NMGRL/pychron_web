# from itertools import groupby
#
# import django_tables2
import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader
import django_tables2 as tables
from django_tables2 import RequestConfig


# from events.tables import EventsTable, TrackerTable
from django.http import HttpResponseRedirect

from events.util import get_pizza_tracker
from events.models import EventsTbl, EventTypeTbl
from events.tables import EventsTable, TrackerTable
from samples.models import SampleTbl

@login_required
def prepped_event(request, sample_id):
    e = EventsTbl()
    s = SampleTbl.objects.filter(id=sample_id).first()
    e.sample = s
    et = EventTypeTbl.objects.filter(name='prepped').first()
    e.event_type = et
    e.event_at = datetime.datetime.now()
    e.user = request.user
    e.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def received_event(request, sample_id):
    e = EventsTbl()
    s = SampleTbl.objects.filter(id=sample_id).first()
    e.sample = s
    et = EventTypeTbl.objects.filter(name='received').first()
    e.event_type = et
    e.event_at = datetime.datetime.now()
    e.user = request.user
    e.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def index(request):
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
#
#     context = {'table': table,
#                'filter': sample_filter,
#                'samples': records,
#                'center': center,
#                'events': eventstable
#                }
    evts = EventsTbl.objects.all()
    eventstable = EventsTable(evts)
    RequestConfig(request).configure(eventstable)

    sids = None
    ts = get_pizza_tracker(sids)

    tracker = TrackerTable(ts)

    RequestConfig(request).configure(tracker)
    context = {'events': eventstable, 'tracker': tracker}

    template = loader.get_template('events/index.html')
    return HttpResponse(template.render(context, request))
