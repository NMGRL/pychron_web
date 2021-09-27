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
from django import forms

from events.models import EventsTbl, EventTypeTbl




class EventsForm(forms.ModelForm):
    event_type = forms.ModelChoiceField(label='Event Type',
                                        queryset=EventTypeTbl.objects.order_by('index').all(),
                                        to_field_name='name')
    message = forms.CharField(label='Message', required=False)
    event_at = forms.SplitDateTimeField(label='Event At',
                                        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'},
                                                                         time_attrs={'type': 'time'}),
                                        required=False)
    # name = forms.CharField(label='Sample')
    # lat = forms.FloatField(label='Latitude', required=False, initial=35)
    # lon = forms.FloatField(label='Longitude', required=False, initial=-105)
    # principal_investigator = forms.CharField(label='Principal Investigator', initial='NMGRL')
    # principal_investigator = forms.ModelChoiceField(label='Principal Investigator',
    #                                                 queryset=PrincipalInvestigatorTbl.objects,
    #                                                 widget=autocomplete.ModelSelect2(
    #                                                     url='principalinvestigator-autocomplete'))
    # project = forms.ModelChoiceField(label='Project',
    #                                  queryset=ProjectTbl.objects,
    #                                  widget=autocomplete.ModelSelect2(url='project-autocomplete',
    #                                                                   forward=['principal_investigator']),
    #                                  )
    # material = forms.ModelChoiceField(label='Material',
    #                                   queryset=Materialtbl.objects,
    #                                   widget=autocomplete.ModelSelect2(url='material-autocomplete'),
    #                                   # to_field_name='name'
    #                                   )
    # material = forms.ChoiceField(label='Material', choices=matchoices)
    # unit = forms.CharField(label='Unit', required=False)
    #
    # northing = forms.FloatField(label='northing', required=False)
    # easting = forms.FloatField(label='easting', required=False)
    # zone = forms.ChoiceField(label='zone',
    #                          choices=[(i,i) for i in range(1, 61)],
    #                          required=False)

    # grainsize = forms.CharField(label='Grainsize', required=False)

    class Meta:
        model = EventsTbl
        fields = ('event_type', 'message', 'event_at')
        # widgets = {
        #     'event_at': forms.widgets.SplitDateTimeWidget(date_attrs={'type': 'date'})
        # }

    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)

        self.fields['event_type'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return obj.name
# ============= EOF =============================================
