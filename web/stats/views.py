import re
from itertools import groupby
from operator import attrgetter, itemgetter, or_

import palettable.scientific.scientific
import pyproj
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.db.models import Q, Count
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, ExtractWeekDay
from django.shortcuts import render
from django.contrib.gis.geos.point import Point

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, CreateView
from django_tables2 import RequestConfig

from analyses.models import AnalysisTbl
from irradiations.models import Irradiationtbl
from analyses.tables import AnalysisTable
from events.forms import EventsForm
from events.models import EventsTbl, EventValuesTbl
from events.tables import EventsTable, TrackerTable, SimpleEventsTable
from events.util import get_pizza_tracker
from projects.forms import ProjectForm
from samples.filters import SampleFilter
from samples.forms import SampleForm
from samples.models import SampleTbl, Materialtbl, Samplesubmittbl, Userpiassociationtbl
from samples.tables import SampleTable
from samples.models import ProjectTbl, PrincipalInvestigatorTbl

from django.contrib.auth.decorators import login_required

from stats.tables import YearStatsTable, MonthStatsTable, DayOfWeekTable
from util import get_center
from analyses.models import AnalysisTbl

def analyses_by_day(request):
    ds = AnalysisTbl.objects.all().values(weekday=ExtractWeekDay('timestamp')).\
        annotate(total=Count('weekday')).order_by('-total')
    return ds


def index(request):
    template = loader.get_template('stats/index.html')
    context = {}

    # ans = AnalysisTbl.objects.order_by('timestamp').annotate(total=Count('year')).order_by(
    #     'total')[:10]

    # ans = AnalysisTbl.objects.annotate(year=ExtractYear('timestamp')).annotate(total=Count('year')).aggregate(
    #     'year').order_by(
    #     'year').values()[:10]
    # 'total')[:10]

    ans = AnalysisTbl.objects.all().values(year=ExtractYear('timestamp')).annotate(total=Count('year')).order_by(
        'year')

    irs = Irradiationtbl.objects.all().values(year=ExtractYear('create_date')).annotate(total=Count(
        'year')).order_by('year')

    ss = AnalysisTbl.objects.all().values(year=ExtractYear('timestamp')).annotate(total=Count(
        'irradiation_positionid_id', distinct=True))

    ms = AnalysisTbl.objects.all().values(month=ExtractMonth('timestamp')).\
        annotate(total=Count('month')).order_by('-total')

    maxn = max([mi['total'] for mi in ms])
    for mi in ms:
        mi['percent_less'] = (maxn-mi['total'])/maxn*100

    ds = analyses_by_day(request)
    context['daystable'] = DayOfWeekTable(ds)

    data = []
    for a in ans:
        record = {'year': a['year'], 'total': a['total']}
        for i in irs:
            if i['year'] == a['year']:
                record['irradiations'] = i['total']
                break
        for si in ss:
            if si['year'] == a['year']:
                record['positions'] = si['total']
                break
        data.append(record)

    context['yeartable'] = YearStatsTable(data)
    context['monthtable'] = MonthStatsTable(ms)
    return HttpResponse(template.render(context, request))
