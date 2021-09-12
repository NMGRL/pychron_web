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

from analyses.models import Analysistbl
from samples.models import ProjectTbl


class AnalysisTable(tables.Table):
    # id = tables.Column(accessor='id', verbose_name='ID')
    # identifier = tables.Column(accessor='irradiation_positionid__identifier')
    runid = tables.Column(accessor='runid', verbose_name='RunID')
    # analysis_type = tables.Column(accessor='analysis_type')
    measurement = tables.Column(accessor='measurementname', verbose_name='Measurement')
    extraction = tables.Column(accessor='extractionname', verbose_name='Extraction')
    timestamp = tables.Column(accessor='dtimestamp', verbose_name='Run Timestamp')
    extract_value = tables.Column(accessor='extract_value')
    # extract_units = tables.Column(accessor='extract_units')
    cleanup = tables.Column(accessor='cleanup')
    duration = tables.Column(accessor='duration')

    class Meta:
        model = Analysistbl
        template_name = "django_tables2/bootstrap.html"
        fields = ['timestamp', 'runid', 'measurement','extraction', 'duration', 'extract_value', 'cleanup']


# ============= EOF =============================================
