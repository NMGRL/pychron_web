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
import django_tables2 as tables
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

from events.models import EventsTbl, EventValuesTbl
from events.util import get_pizza_tracker
from table_util import ImageColumn


class TrackerTable(tables.Table):
    sample = tables.Column(accessor='sample')
    received = ImageColumn('events/img/package.png', accessor='received')
    prepped = ImageColumn('events/img/beaker.png', accessor='prepped')
    irradiated = ImageColumn('events/img/radioactivity.png', accessor='irradiated')
    analyzed = ImageColumn('events/img/assembled_diagram.png', accessor='analyzed')

    material = tables.Column(accessor='material',
                             verbose_name='Material',
                             linkify= lambda record: '',)
                             # linkify=lambda record: reverse('materials:detail'))
    # grainsize = tables.Column(accessor='materialid__grainsize')
    project = tables.Column(accessor='project',
                            verbose_name='Project',
                            linkify=lambda record: f'projects/{record["project"]}')

    # principal_investigator = tables.Column(accessor='projectid__principal_investigatorid__full_name',
    #                                        verbose_name='Principal Investigator',
    #                                        linkify=lambda
    #                                            record: f'/principal_investigators/{record.projectid.principal_investigatorid.id}')

    # assigned = tables.Column(accessor='sample')
    # prepped = tables.Column(accessor='sample')
    # irradiated = tables.Column(accessor='sample')
    # analyzed = tables.Column(accessor='sample')

    class Meta:
        attrs = {'class': 'table table-condensed'}


class SimpleEventsTable(tables.Table):
    event_type = tables.Column(accessor='event_type__name', verbose_name='Event Type',
                               attrs={'td':{'class': 'details'}})
    message = tables.Column(accessor='message')
    created_at = tables.DateTimeColumn(accessor='created_at', verbose_name='Created At',
                                       format='m/d/Y h:i A')
    event_at = tables.DateTimeColumn(accessor='event_at', verbose_name='Event At',
                                     format='m/d/Y h:i A')
    user = tables.Column(accessor='user')

    class Meta:
        attrs = {'class': 'table table-condensed'}

    def render_event_type(self, record):
        values = EventValuesTbl.objects.filter(event_id=record.id).all()
        t = f'{record.event_type.name}'
        if values:
            values = '<br/>'.join([f'{v.name}: {v.value}' for v in values])
            t = format_html(f'{t}<span class="detailstext">{values}</span>')
        return format_html(t)


class EventsTable(SimpleEventsTable):
    sample = tables.Column(linkify=lambda record: f'samples/{record.sample.id}',
                           verbose_name='Sample',
                           accessor='sample.name')
    project = tables.Column(accessor='sample__projectid__name',
                            verbose_name='Project',
                            linkify=lambda record: f'projects/{record.sample.projectid_id}')
    principal_investigator = tables.Column(accessor='sample__projectid__principal_investigatorid__full_name',
                                           verbose_name='Principal Investigator',
                                           linkify=lambda
                                               record: reverse(f'principal_investigators:detail',
                                                               args=[
                                                                   record.sample.projectid.principal_investigatorid.id])
                                           )
# ============= EOF =============================================
