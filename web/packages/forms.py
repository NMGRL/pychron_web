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
from crispy_forms.layout import Submit, Layout, Fieldset, Div
from dal import autocomplete
from django import forms

# from leaflet.forms.fields import PointField
# from leaflet.forms.widgets import LeafletWidget
from django.forms import HiddenInput

from packages.models import PackageAssociationTbl
from samples.models import Materialtbl, ProjectTbl, SampleTbl, PrincipalInvestigatorTbl


class PackageAssocationForm(forms.ModelForm):
    project = forms.ModelChoiceField(label='Project',
                                     required=False,
                                     queryset=ProjectTbl.objects,
                                     widget=autocomplete.ModelSelect2(
                                         url='project-autocomplete'))

    sample = forms.ModelChoiceField(label='Sample',
                                    queryset=SampleTbl.objects,
                                    widget=autocomplete.ModelSelect2(
                                        url='sample-autocomplete',
                                        forward=['project']),
                                    )

    class Meta:
        model = PackageAssociationTbl
        fields = ('project', 'sample',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_package_association'

        self.helper.add_input(Submit('submit', 'Submit'))


class PackagesForm(forms.Form):
    name = forms.CharField(label='Name', help_text='Enter the name for a new Package or select and existing Package')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_package'

        self.helper.add_input(Submit('submit', 'Submit'))

# # class PIProjectForm(forms.Form):
# #     principal_investigator = forms.CharField(label='Principal Investigator')
# #     project = forms.CharField(label='Project')
# #
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         self.helper = FormHelper()
# #         self.helper.form_id = 'id-exampleForm'
# #         self.helper.form_class = 'blueForms'
# #         self.helper.form_method = 'post'
# #         self.helper.form_action = 'submit_pp'
# #
# #         self.helper.add_input(Submit('submit', 'Submit'))
#
#
# class SampleForm(forms.ModelForm):
#     name = forms.CharField(label='Sample')
#     lat = forms.FloatField(label='Latitude', required=False, initial=35)
#     lon = forms.FloatField(label='Longitude', required=False, initial=-105)
#     # principal_investigator = forms.CharField(label='Principal Investigator', initial='NMGRL')
#     # principal_investigator = forms.ModelChoiceField(label='Principal Investigator',
#     #                                                 queryset=PrincipalInvestigatorTbl.objects.all(),
#     #                                                 widget=autocomplete.ModelSelect2(
#     #                                                     url='principalinvestigator-autocomplete'))
#     project = forms.ModelChoiceField(label='Project',
#                                      queryset=ProjectTbl.objects,
#                                      widget=autocomplete.ModelSelect2(
#                                          url='project-autocomplete'))
#
#     material = forms.ModelChoiceField(label='Material',
#                                       queryset=Materialtbl.objects,
#                                       widget=autocomplete.ModelSelect2(url='material-autocomplete'),
#                                       # to_field_name='name'
#                                       )
#     # material = forms.ChoiceField(label='Material', choices=matchoices)
#     unit = forms.CharField(label='Unit', required=False)
#     location = forms.CharField(label='Location', required=False)
#     lithology = forms.CharField(label='Lithology', required=False)
#
#     northing = forms.FloatField(label='Northing', required=False)
#     easting = forms.FloatField(label='Easting', required=False)
#     datum = forms.ChoiceField(label='Datum', required=False,
#                               choices=[(1, 'NAD83'), (2, 'NAD27')],
#                               # initial='NAD83'
#                               )
#     pointloc = PointField(label='',
#                           widget=LeafletWidget(attrs={'map_width': '100%', 'map_height': '100px'}),
#                           required=False)
#     zone = forms.ChoiceField(label='Zone',
#                              choices=[(i, i) for i in range(1, 61)],
#                              required=False)
#
#     # grainsize = forms.CharField(label='Grainsize', required=False)
#     remembered_fields = ('project', 'material', 'lat', 'lon', 'unit', 'easting', 'northing', 'datum', 'zone')
#
#     class Meta:
#         model = SampleTbl
#         fields = ('project', 'material',
#                   'name', 'unit', 'location', 'lithology',
#                   'lat', 'lon', 'easting',
#                   'northing', 'zone', 'datum', 'pointloc')
#
#
#     @staticmethod
#     def project_label(obj):
#         return obj.piname
#
#     @staticmethod
#     def material_label(obj):
#         return obj.full_name
#
#     def __init__(self, *args, **kwargs):
#         form_action = None
#         if 'form_action' in kwargs:
#             form_action = kwargs.pop('form_action')
#
#         super().__init__(*args, **kwargs)
#
#         self.fields['project'].label_from_instance = self.project_label
#         self.fields['material'].label_from_instance = self.material_label
#
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-exampleForm'
#         self.helper.form_class = 'blueForms'
#         self.helper.form_method = 'post'
#         self.helper.form_action = form_action or 'submit_sample'
#
#         self.helper.add_input(Submit('submit', 'Submit'))
#
#         col1 = Div(
#             Div(Div('project', css_class='col-md-3'),
#                 css_class='row'),
#             Div(Div('material', css_class='col-md-3'),
#                 css_class='row'),
#             Div(Div('name', css_class='col-md-6'),
#                 css_class='row'),
#             Div(Div('unit', css_class='col-md-4'),
#                 Div('location', css_class='col-md-4'),
#                 Div('lithology', css_class='col-md-4'),
#                 css_class='row'),
#             Div(Div('lat', css_class='col-md-5'),
#                 Div('lon', css_class='col-md-5'),
#                 css_class='row'),
#             Div(Div('easting', css_class='col-md-5'),
#                 Div('northing', css_class='col-md-5'),
#                 css_class='row'),
#             Div(Div('zone', css_class='col-md-2'),
#                 Div('datum', css_class='col-md-3'),
#                 css_class='row'),
#             css_class='col-lg-5')
#         col2 = Div('pointloc', css_class='col-lg-7')
#
#         self.helper.layout = Layout(Div(Div(col1, col2, css_class='row'),
#                                         css_class='container-fluid'))
# ============= EOF =============================================
