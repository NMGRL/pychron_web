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
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

from analyses.models import Irradiationpositiontbl, Analysistbl
from events.models import EventsTbl
from samples.models import SampleTbl


class ActionColumn(tables.Column):
    class Meta:
        attrs = {'class': 'table table-condensed'}

    def __init__(self, tag, image, *args, **kw):
        super(ActionColumn, self).__init__(*args, **kw)
        self.event_tag = tag
        self.image = image

    def render(self, value):
        evts = EventsTbl.objects.filter(sample__id=value).all()
        if any(e.event_type.name == self.event_tag for e in evts.all()):
            return mark_safe('')
        else:
            return mark_safe(f'<a href=/events/{escape(self.event_tag)}/{value}>'
                             f'<img src="/static/samples/img/{escape(self.image)}"/ '
                             f'style="width:16px;height:16px;"></a>')


def render_row(record):
    ipt = Irradiationpositiontbl.objects.filter(sampleid=record.id).first()
    c = ''
    if ipt:
        c = 'loaded_for_irradiation'
        a = Analysistbl.objects.filter(irradiation_positionid=ipt.id).first()
        if a:
            c = 'analyzed'
    return c


class SampleTable(tables.Table):
    material = tables.Column(accessor='materialid__name',
                             verbose_name='Material',
                             linkify=lambda record: f'/materials/{record.materialid_id}/')
    grainsize = tables.Column(accessor='materialid__grainsize')
    project = tables.Column(accessor='projectid__name',
                            verbose_name='Project',
                            linkify=lambda record: f'/projects/{record.projectid_id}')
    principal_investigator = tables.Column(accessor='projectid__principal_investigatorid__full_name',
                                           verbose_name='Principal Investigator',
                                           linkify=lambda
                                               record: f'/principal_investigators/{record.projectid.principal_investigatorid.id}')

    lat = tables.Column(verbose_name='Latitude', accessor='lat')
    lon = tables.Column(verbose_name='Longitude', accessor='lon')
    id = tables.Column(linkify=True, accessor='id')
    name = tables.Column(linkify=True, accessor='name')
    irradiations = tables.Column(empty_values=())

    received = ActionColumn('received', 'arrow-down-double-3.png', accessor='id', verbose_name='Check In')
    prepped = ActionColumn('prepped', 'beaker.png', accessor='id', verbose_name='Prep')

    class Meta:
        model = SampleTbl
        template_name = "django_tables2/bootstrap.html"
        fields = ['id', 'name', 'lat', 'lon',
                  'unit']

        attrs = {'class': 'table table-condensed'}
        row_attrs = {'class': render_row}

    # def render_id(self, record):

    def render_irradiations(self, record):
        ipts = Irradiationpositiontbl.objects.filter(sampleid_id=record.id).all()

        t = ''
        if ipts:
            names = {f'{i.levelid.irradiationid.name}' for i in ipts}
            t = ','.join(list(names))

        return format_html(t)
# ============= EOF =============================================