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

from samples.models import Sampletbl


class SampleTable(tables.Table):
    material = tables.Column(accessor='materialid__name',
                             verbose_name='Material')
    project = tables.Column(accessor='projectid__name',
                            verbose_name='Project',
                            linkify=lambda record: '/projects/{}'.format(record.projectid_id))
    id = tables.Column(linkify=True, accessor='id')
    name = tables.Column(linkify=True, accessor='name')

    class Meta:
        model = Sampletbl
        template_name = "django_tables2/bootstrap.html"
        fields = ['id', 'name', 'latitude', 'longitude',
                  'unit']

# ============= EOF =============================================
