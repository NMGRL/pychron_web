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
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms

from samples.models import Materialtbl, Projecttbl, Sampletbl, Principalinvestigatortbl


def matchoices():
    return [(m['id'], m['name']) for m in Materialtbl.objects.values('name', 'id').distinct()]


class SampleForm(forms.ModelForm):
    name = forms.CharField(label='Sample')
    lat = forms.FloatField(label='Latitude', required=False, initial=35)
    lon = forms.FloatField(label='Longitude', required=False, initial=-105)
    # principal_investigator = forms.CharField(label='Principal Investigator', initial='NMGRL')
    principal_investigator = forms.ModelChoiceField(label='Principal Investigator',
                                                    queryset=Principalinvestigatortbl.objects,
                                                    widget=autocomplete.ModelSelect2(
                                                        url='principalinvestigator-autocomplete'))
    project = forms.ModelChoiceField(label='Project',
                                     queryset=Projecttbl.objects,
                                     widget=autocomplete.ModelSelect2(url='project-autocomplete',
                                                                      forward=['principal_investigator']),
                                     )
    material = forms.ModelChoiceField(label='Material',
                                      queryset=Materialtbl.objects,
                                      widget=autocomplete.ModelSelect2(url='material-autocomplete'),
                                      # to_field_name='name'
                                      )
    # material = forms.ChoiceField(label='Material', choices=matchoices)
    unit = forms.CharField(label='Unit', required=False)

    # grainsize = forms.CharField(label='Grainsize', required=False)

    class Meta:
        model = Sampletbl
        fields = ('principal_investigator', 'project', 'name', 'material', 'unit', 'lat', 'lon')
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'id-exampleForm'
    #     self.helper.form_class = 'blueForms'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = 'submit_sample'
    #
    #     self.helper.add_input(Submit('submit', 'Submit'))

# ============= EOF =============================================
