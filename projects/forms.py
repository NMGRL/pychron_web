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
from django.urls import reverse_lazy

from samples.models import PrincipalInvestigatorTbl, ProjectTbl


class ProjectForm(forms.ModelForm):
    principal_investigator = forms.ModelChoiceField(label='Principal Investigator',
                                                    queryset=PrincipalInvestigatorTbl.objects.all(),
                                                    widget=autocomplete.ModelSelect2(
                                                        url=reverse_lazy('principalinvestigator-autocomplete')))
    name = forms.CharField(label='Project')

    class Meta:
        fields = ['principal_investigator', 'name']
        model = ProjectTbl

    def __init__(self, *args, **kwargs):
        # kwargs.pop('instance')
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_project'

        self.helper.add_input(Submit('submit', 'Submit'))

# class ProjectForm(forms.Form):
#     name = forms.CharField(label='Project')
#     # latitude = forms.FloatField(label='Latitude', required=False, initial=35)
#     # longitude = forms.FloatField(label='Longitude', required=False, initial=-105)
#     principal_investigator = forms.CharField(label='Principal Investigator', initial='NMGRL')
#     project = forms.CharField(label='Project', initial='REFERENCES')
#
#     def __init__(self, *args, **kwargs):
#         kwargs.pop('instance')
#         super().__init__(*args, **kwargs)
#
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-exampleForm'
#         self.helper.form_class = 'blueForms'
#         self.helper.form_method = 'post'
#         self.helper.form_action = 'submit_sample'
#
#         self.helper.add_input(Submit('submit', 'Submit'))

# ============= EOF =============================================
