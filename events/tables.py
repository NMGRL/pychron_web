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
from django.utils.html import escape
from django.utils.safestring import mark_safe

from events.models import EventsTbl
from events.util import get_pizza_tracker
from table_util import ImageColumn


class TrackerTable(tables.Table):
    sample = tables.Column(accessor='sample')
    received = ImageColumn('/static/events/img/package.png', accessor='received')
    prepped = ImageColumn('/static/events/img/beaker.png', accessor='prepped')
    irradiated = ImageColumn('/static/events/img/radioactivity.png', accessor='irradiated')
    analyzed = ImageColumn('/static/events/img/assembled_diagram.png', accessor='analyzed')

    material = tables.Column(accessor='material',
                             verbose_name='Material',
                             linkify=lambda record: f'/materials/{record["material"]}/')
    # grainsize = tables.Column(accessor='materialid__grainsize')
    project = tables.Column(accessor='project',
                            verbose_name='Project',
                            linkify=lambda record: f'/projects/{record["project"]}')
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


class EventsTable(tables.Table):
    event_type = tables.Column(accessor='event_type__name', verbose_name='Event Type')
    message = tables.Column(accessor='message')
    created_at = tables.DateTimeColumn(accessor='created_at', verbose_name='Created At',
                                       format='m/d/Y h:i A')
    event_at = tables.DateTimeColumn(accessor='event_at', verbose_name='Event At',
                                     format='m/d/Y h:i A')
    user = tables.Column(accessor='user')
    sample = tables.Column(linkify=lambda record: f'/samples/{record.sample.id}',
                           verbose_name='Sample',
                           accessor='sample.name')
    project = tables.Column(accessor='sample__projectid__name',
                            verbose_name='Project',
                            linkify=lambda record: f'/projects/{record.sample.projectid_id}')
    principal_investigator = tables.Column(accessor='sample__projectid__principal_investigatorid__full_name',
                                           verbose_name='Principal Investigator',
                                           linkify=lambda
                                               record: f'/principal_investigators/'
                                                       f'{record.sample.projectid.principal_investigatorid.id}')
    class Meta:
        attrs = {'class': 'table table-condensed'}
# ============= EOF =============================================
