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

from table_util import ImageColumn


class TrackerTable(tables.Table):
    sample = tables.Column(accessor='sample')
    received = ImageColumn('/static/events/img/dialog-ok.png', accessor='received')
    prepped = ImageColumn('/static/events/img/dialog-ok.png', accessor='prepped')
    irradiated = ImageColumn('/static/events/img/dialog-ok.png', accessor='irradiated')
    analyzed = ImageColumn('/static/events/img/dialog-ok.png', accessor='analyzed')
    # assigned = tables.Column(accessor='sample')
    # prepped = tables.Column(accessor='sample')
    # irradiated = tables.Column(accessor='sample')
    # analyzed = tables.Column(accessor='sample')


class EventsTable(tables.Table):
    message = tables.Column(accessor='message')
    created_at = tables.Column(accessor='created_at')
    event_at = tables.Column(accessor='event_at')
    event_type = tables.Column(accessor='event_type__name')
    user = tables.Column(accessor='user')

    # class Meta:
    #     attrs = {'class': 'smalltable'}
# ============= EOF =============================================
