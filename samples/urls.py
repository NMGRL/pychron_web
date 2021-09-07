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
from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = 'samples'
urlpatterns = [
    path('', views.index, name='index'),
    path('submit_sample', views.submit_sample, name='submit_sample'),
    re_path(r'edit_sample/(?P<sample_id>\d+)/$', views.edit_sample, name='edit_sample'),
    path('entry', views.entry, name='entry'),
    path('<int:pk>/', views.SampleDetailView.as_view(), name='detail')
]
# ============= EOF =============================================
