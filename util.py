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

def get_center(records):
    records = [r for r in records if r.lat or r.lon]
    n = len(records)
    if n:
        center = [sum((r.lat for r in records)) / n, sum((r.lon for r in records)) / n]
    else:
        center, records = (0,0), []
    return center, records
# ============= EOF =============================================
