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
from users.views import dashboard, signup, add_user, manage, activate, set_password

urlpatterns = [
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r'^signup/$', signup, name='signup'),
    url(r'^add_user/$', add_user, name='add_user'),
    # url(r'^set_password/(?P<user_id>\d+)/$', set_password, name='set_password'),
    url(r'^set_password/$', set_password, name='set_password'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        activate, name='activate'),
]

# ============= EOF =============================================
