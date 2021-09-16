# ===============================================================================
# Copyright 2021 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import datetime
import os
from itertools import groupby
from operator import itemgetter

import pytz

from analyses.models import Irradiationtbl, Analysistbl
from events.models import EventsTbl
from django.conf import settings

os.environ['TZ'] = settings.TIME_ZONE


def get_event(es, tag):
    for e in es:
        if e['event_type__name'] == tag:
            return e


def event(es, tag):
    e = get_event(es, tag)
    s = ''
    if e:
        t = e['event_at'].astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%m/%d/%Y %I:%M %a')
        s = f'{t} {e["user__username"]}'

    return s


def get_pizza_tracker(sids):
    evts = EventsTbl.objects
    if sids:
        evts = evts.filter(sample_id__in=sids)

    evts = evts.order_by('sample_id').order_by('-event_at').values('sample_id',
                                                                   'sample__name',
                                                                   'sample__projectid__name',
                                                                   'sample__materialid__name',
                                                                   'event_type__name',
                                                                   'event_at',
                                                                   'user__username')
    ts = []
    for s, es in groupby(evts, key=itemgetter('sample_id')):
        ans = []

        irradiations = Irradiationtbl.objects
        irradiations = irradiations.filter(leveltbl__irradiationpositiontbl__sampleid=s,
                                           leveltbl__irradiationpositiontbl__identifier__isnull=False)
        irradiations = irradiations.values('name', 'leveltbl__name',
                                           'leveltbl__irradiationpositiontbl__position',
                                           'leveltbl__irradiationpositiontbl__identifier')

        if irradiations:
            ans = Analysistbl.objects.filter(irradiation_positionid__sampleid=s).order_by('timestamp').first()

        es = list(es)
        istring = ','.join(
            ['{}{}{} {}'.format(i['name'], i['leveltbl__name'], i['leveltbl__irradiationpositiontbl__position'],
                                i['leveltbl__irradiationpositiontbl__identifier']) for i in irradiations])

        istring = f'{istring[:30]}...' if len(istring) > 30 else istring
        e0 = es[0]
        t = {'sample': e0['sample__name'],
             'received': event(es, 'received') or False,
             'prepped': event(es, 'prepped') or False,
             'project': e0['sample__projectid__name'],
             'material': e0['sample__materialid__name'],
             'irradiated': istring or False,
             'analyzed': ans.dtimestamp if ans else False
             }
        ts.append(t)

    return ts
# ============= EOF =============================================
