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

from samples.models import ProjectTbl


class PIColumn(tables.Column):
    def get_url(self, record=None, **kw):
        return f'/principal_investigators/{record.principal_investigatorid.id}'


class ProjectTable(tables.Table):
    id = tables.Column(linkify=True, accessor='id', verbose_name='IR#')
    name = tables.Column(linkify=True, accessor='name')

    piname = PIColumn(verbose_name='Principal Investigator',
                      accessor='principal_investigatorid__full_name')

    class Meta:
        model = ProjectTbl
        template_name = "django_tables2/bootstrap.html"
        fields = ['id', 'name', 'piname']
        attrs = {'class': 'table table-condensed'}

def closure():
    _state = {}

    def duplicate_render_row(record):
        c = 'g0'
        if _state:
            c = _state['c']

        name = record.name
        if _state and name != _state['name']:
            c = 'g1'
            if _state['c'] == c:
                c = 'g0'

        _state['name'] = name
        _state['c'] = c
        return c
        # ipt = Irradiationpositiontbl.objects.filter(sampleid=record.id).first()
        # c = ''
        # if ipt:
        #     c = 'loaded_for_irradiation'
        #     a = Analysistbl.objects.filter(irradiation_positionid=ipt.id).first()
        #     if a:
        #         c = 'analyzed'
        # return c

    return duplicate_render_row


class DuplicateProjectTable(ProjectTable):
    nsamples = tables.Column(accessor='nsamples')

    class Meta:
        model = ProjectTbl
        template_name = "django_tables2/bootstrap.html"
        fields = ['id', 'name', 'piname', 'nsamples']
        attrs = {'class': 'table table-condensed'}

        row_attrs = {'class': closure()}
# ============= EOF =============================================
