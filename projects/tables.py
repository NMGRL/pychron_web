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

# ============= EOF =============================================
