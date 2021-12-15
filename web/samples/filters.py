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
import django_filters
from django_filters import FilterSet, ChoiceFilter

from analyses.models import AnalysisTbl
from irradiations.models import Irradiationpositiontbl
from samples.models import SampleTbl, ProjectTbl


class SampleFilter(FilterSet):
    state = ChoiceFilter(choices=[('Not Irradiated', 'Not Irradiated'),
                                  ('Not Analyzed', 'Not Analyzed'),
                                  ('Irradiated', 'Irradiated'),
                                  ('Analyzed', 'Analyzed'),
                                  ], method='state_filter')

    class Meta:
        model = SampleTbl
        fields = {'name': ['icontains', ],
                  'materialid__name': ['icontains', ],
                  'projectid__name': ['icontains', ],
                  'projectid__principal_investigatorid__last_name': ['icontains', ]
                  }

    def state_filter(self, qs, name, value):
        sampleid_ids = Irradiationpositiontbl.objects.filter(sampleid__isnull=False).values_list('sampleid__id',
                                                                                                 flat=True)
        if value == 'Not Irradiated':
            r = qs.exclude(id__in=sampleid_ids)
        elif value == 'Irradiated':
            r = qs.filter(id__in=sampleid_ids).all()
        elif value == 'Analyzed':
            ips = Irradiationpositiontbl.objects.filter(sampleid__isnull=False)
            sids = AnalysisTbl.objects.filter(irradiation_positionid__in=ips).values_list(
                'irradiation_positionid__sampleid_id', flat=True)
            r = qs.filter(id__in=sids).all()
        elif value == 'Not Analyzed':
            ips = Irradiationpositiontbl.objects.filter(sampleid__isnull=False)
            sids = AnalysisTbl.objects.filter(irradiation_positionid__in=ips).values_list(
                'irradiation_positionid__sampleid_id', flat=True)
            r = qs.exclude(id__in=sids)
        return r

# ============= EOF =============================================
