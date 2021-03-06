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

from django.urls import path

from . import views

app_name = 'analyses'
urlpatterns = [
    path('recent', views.recent_analyses, name='recent'),
    path('series', views.series, name='series'),
    path('task/<str:task_id>/', views.TaskView.as_view(), name='task')
    # path('chart', views.line_chart, name='line_chart'),
    # path('chartJSON', views.LineChartJSONView.as_view(), name='line_chart_json'),

    # path('submit_project', views.submit_project, name='submit_project'),
    # path('entry', views.entry, name='entry'),
    # path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail')

]
# ============= EOF =============================================
