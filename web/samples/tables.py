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

from analyses.models import Irradiationpositiontbl, AnalysisTbl
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
            from django.templatetags.static import static
            src = static(f'samples/img/{escape(self.image)}')
            return mark_safe(f'<a href=/events/{escape(self.event_tag)}/{value}>'
                             f'<img src={src} '
                             f'style="width:16px;height:16px;"></a>')


def render_row(record):
    ipt = Irradiationpositiontbl.objects.filter(sampleid=record.id).first()
    c = ''
    if ipt:
        c = 'loaded_for_irradiation'
        a = AnalysisTbl.objects.filter(irradiation_positionid=ipt.id).first()
        if a:
            c = 'analyzed'
    return c


class SamplesColumn(tables.Column):
    def get_url(self, record, **kw):
        return reverse('samples:detail', args=[record.id])


class SampleTable(tables.Table):
    material = tables.Column(accessor='materialid__name',
                             verbose_name='Material',
                             linkify=lambda record: reverse('materials:detail', args=[record.materialid_id]))
    grainsize = tables.Column(accessor='materialid__grainsize')
    project = tables.Column(accessor='projectid__name',
                            verbose_name='Project',
                            linkify=lambda record: reverse('projects:detail', args=[record.projectid_id]))
    principal_investigator = tables.Column(accessor='projectid__principal_investigatorid__full_name',
                                           verbose_name='Principal Investigator',
                                           linkify=lambda
                                               record: reverse('principal_investigators:detail',
                                                               args=[record.projectid.principal_investigatorid.id]))

    lat = tables.Column(verbose_name='Latitude', accessor='lat')
    lon = tables.Column(verbose_name='Longitude', accessor='lon')
    id = SamplesColumn(accessor='id')
    name = SamplesColumn(accessor='name')
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
