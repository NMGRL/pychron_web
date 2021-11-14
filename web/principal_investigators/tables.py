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

from samples.models import PrincipalInvestigatorTbl


class PrincipalInvestigatorColumn(tables.Column):
    def get_url(self, record, **kw):
        return reverse('principal_investigator:detail', args=[record.id])


class PrincipalInvestigatorsTable(tables.Table):
    id = PrincipalInvestigatorColumn(accessor='id')
    name = PrincipalInvestigatorColumn(accessor='full_name')

    class Meta:
        model = PrincipalInvestigatorTbl
        template_name = "django_tables2/bootstrap.html"
        fields = ['id', 'name']
        attrs = {'class': 'table table-condensed'}

# ============= EOF =============================================
