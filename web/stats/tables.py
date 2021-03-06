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
import calendar

import django_tables2 as tables

from analyses.models import AnalysisTbl
from samples.models import ProjectTbl


class DayOfWeekTable(tables.Table):
    weekday = tables.Column()
    total = tables.Column(accessor='total', verbose_name='Total Analyses')
    percent_less = tables.Column(accessor='total', verbose_name='%Delta from Max')

    def render_percent_less(self, value):
        maxn = max([mi['total'] for mi in self.data])
        return '{:0.2f}'.format((maxn - value) / maxn * 100)

    def render_weekday(self, value):
        return calendar.day_name[value-1]


class MonthStatsTable(tables.Table):
    # year = tables.Column(accessor='year', attrs={'td': {'width': '50px'}})
    month = tables.Column()
    total = tables.Column(accessor='total', verbose_name='Total Analyses')
    percent_less = tables.Column(accessor='total', verbose_name='%Delta from Max')

    def render_percent_less(self, value):
        maxn = max([mi['total'] for mi in self.data])
        return '{:0.2f}'.format((maxn - value) / maxn * 100)

    def render_month(self, value):
        return calendar.month_name[value]


class YearStatsTable(tables.Table):
    # id = tables.Column(accessor='id', verbose_name='ID')
    # identifier = tables.Column(accessor='irradiation_positionid__identifier')
    year = tables.Column(accessor='year', verbose_name='Year', attrs={'td': {'width': '50px'}})
    total = tables.Column(accessor='total', verbose_name='Total Analyses')
    total_irradiations = tables.Column(accessor='irradiations', verbose_name='Total Irradiations')
    total_irradiated_positions = tables.Column(accessor='positions',
                                               verbose_name='Total Irradiated Positions Analyzed')

    change = tables.Column(accessor='total', verbose_name='%Delta from Prev.')

    # analysis_type = tables.Column(accessor='analysis_type')
    # measurement = tables.Column(accessor='measurementname', verbose_name='Measurement')
    # extraction = tables.Column(accessor='extractionname', verbose_name='Extraction')
    # timestamp = tables.Column(accessor='dtimestamp', verbose_name='Run Timestamp')
    # extract_value = tables.Column(accessor='extract_value')
    # extract_units = tables.Column(accessor='extract_units')
    # cleanup = tables.Column(accessor='cleanup')
    # duration = tables.Column(accessor='duration')

    class Meta:
        # model = AnalysisTbl
        template_name = "django_tables2/bootstrap.html"
        # fields = ['timestamp', 'runid', 'measurement','extraction', 'duration', 'extract_value', 'cleanup']

    def render_change(self, value, record):
        idx = self.data.data.index(record)
        c = 0
        if idx:
            p = self.data[idx - 1]['total']
            c = (value - p) / p * 100
        return '{:0.2f}'.format(c)
# ============= EOF =============================================
