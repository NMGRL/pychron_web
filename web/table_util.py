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
import django_tables2 as tables
from django.templatetags.static import static
from django.utils.html import escape
from django.utils.safestring import mark_safe


class ImageColumn(tables.Column):
    def __init__(self, image, *args, **kw):
        self._image_src = image
        super(ImageColumn, self).__init__(*args, **kw)

    def render(self, value):
        if value:
            src = self._image_src
            if not isinstance(value, bool):
                dt = value

        else:
            dt = ''
            src = ''
            # t = f'<img class="icon" src="{self._image_src}"/></a>'
        src = static(src)
        return mark_safe(f'<img class="icon" src="{src}"/> {dt}')

# ============= EOF =============================================
