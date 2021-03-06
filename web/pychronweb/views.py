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
import os

from django.conf import settings
from django.db.models import Count
from django.db.models.functions import ExtractYear, TruncYear
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    p = os.path.join(settings.BASE_DIR, 'plugins', 'home.html')
    body = ''
    if os.path.isfile(p):
        with open(p, 'r') as rfile:
            body = rfile.read()

    context = {'labspecific_content': body,
               'app_title': settings.APP_TITLE}
    return HttpResponse(template.render(context, request))
# ============= EOF =============================================
