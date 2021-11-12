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
from django import forms
from django.core.validators import RegexValidator

# validator = RegexValidator(, 'Single name or LastName,FirstInitial e.g. Ross,J')


class PrincipalInvestigatorForm(forms.Form):
    # name = forms.CharField(label='Principal Investigator')
    name = forms.RegexField(r'^\w+,{0,1}\w{1}$', label='Principal Investigator',
                            help_text=' Enter a <code>SingleName</code> or <code>lastName,firstInitial</code>  e.g '
                                      '<b>NMGRL</b> or <b>"Ross,J"</b>')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_principal_investigator'

        self.helper.add_input(Submit('submit', 'Submit'))

# ============= EOF =============================================
