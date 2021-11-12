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

from events.models import EventsTbl, EventTypeTbl


class EventsForm(forms.ModelForm):
    event_type = forms.ModelChoiceField(label='Event Type',
                                        queryset=EventTypeTbl.objects.order_by('index').all(),
                                        to_field_name='name')
    message = forms.CharField(label='Message', required=False,
                              widget=forms.Textarea(attrs={'rows': 4}))
    event_at = forms.SplitDateTimeField(label='Event At',
                                        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'},
                                                                         time_attrs={'type': 'time'}),
                                        required=False,
                                        help_text='Specify the time of the <b>Event</b>. If left blank use current '
                                                  'date and time')
    event_values = forms.CharField(label='Event Values',
                                   help_text='Specify events using the format <code>Name: Value</code>.  For example  '
                                             '<b>Sieve: 400micron</b> '
                                             'Separate multiple values with the <b>|</b> character. For example  '
                                             '<b>Sieve: 400micron|Wash: DI 5mins</b>',
                                   widget=forms.Textarea(attrs={'rows': 5}),
                                   required=False)

    class Meta:
        model = EventsTbl
        fields = ('event_type', 'message', 'event_at', 'event_values')
        # widgets = {
        #     'event_at': forms.widgets.SplitDateTimeWidget(date_attrs={'type': 'date'})
        # }

    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        self.fields['event_type'].label_from_instance = self.label_from_instance

        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'edit_sample'

        self.helper.add_input(Submit('submit', 'Submit'))

    @staticmethod
    def label_from_instance(obj):
        return obj.name
# ============= EOF =============================================
