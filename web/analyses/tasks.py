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
import base64
import datetime
import json
import os
import struct

import bokeh
from bokeh.plotting import figure
from git import Repo
from git.exc import GitCommandError
from celery import shared_task
from django.conf import settings
from numpy import array

from .models import AnalysisTbl, RepositoryAssociationTbl


@shared_task
def make_all_series():
    return json.dumps({'cocktails': make_series('cocktail'),
                       'airs': make_series('air'),
                       'blank_cocktails': make_series('blank_cocktail'),
                       'blank_airs': make_series('blank_air')})


@shared_task
def make_recent_analyses():
    context = {}
    analyses = AnalysisTbl.objects.order_by('-id')[:2]
    # repos = {ai.repository for ai in analyses}
    repo_associations = RepositoryAssociationTbl.objects.filter(analysisID__in=[a.id for a in analyses])
    repos = {r.repository for r in repo_associations}

    # repos = ['Irradiation-NM-321', ]
    for r in repos:
        clone_repo(r)

    for assoc in sorted(repo_associations, key=lambda a: a.analysisID.timestamp, reverse=True):
        plot_assoc(context, assoc)

    return json.dumps(context)


def make_series(atype):
    ans = AnalysisTbl.objects.filter(analysis_type=atype,
                                     mass_spectrometer='jan').order_by('-id')[:20]
    repo_associations = RepositoryAssociationTbl.objects.filter(analysisID__in=[a.id for a in ans])
    repos = {r.repository for r in repo_associations}

    for r in repos:
        clone_repo(r)

    x, y = [], []
    ys = {}
    for assoc in repo_associations:
        ans = assoc.analysisID
        x.append(ans.timestamp)

        ans = assoc.analysisID
        uuid = ans.uuid
        repo = assoc.repository
        if settings.ANALYSES_DEBUG:
            uuid = '0a0ff3c4-ef60-4f26-8241-298c57558916'
            repo = 'Irradiation-NM-321'

        path = get_analysis_path(repo, uuid, modifier='intercepts')
        for iso in ('Ar40', 'Ar36'):
            with open(path, 'r') as rfile:
                jobj = json.load(rfile)
                value = jobj[iso]['value']
                arr = ys.get(iso, [])
                arr.append(value)
                ys[iso] = arr

    ret = {}
    for iso in ('Ar40', 'Ar36'):
        plot = figure(y_axis_label=iso,
                      x_axis_type='datetime',
                      height=150)
        plot.scatter(x, ys[iso])
        ret[iso] = bokeh.embed.json_item(plot, iso)
        # script, div = components(plot)
        # ret.append({'script': script, 'div': div})

    plot = figure(y_axis_label=f'Ar40/Ar36 {atype}',
                  x_axis_type='datetime',
                  height=150)

    plot.scatter(x, array(ys['Ar40']) / array(ys['Ar36']))
    ret['ar4036'] = bokeh.embed.json_item(plot, 'ar4036')
    # script, div = components(plot)
    #
    # ret.append({'script': script, 'div': div})
    # return ret
    return ret


def unpack(blob, fmt, step=8):
    blob = base64.b64decode(blob)
    return list(
        zip(
            *[
                struct.unpack(fmt, blob[i: i + step])
                for i in range(0, len(blob), step)
            ]
        )
    )


def plot_assoc(context, assoc):
    repo = assoc.repository
    ans = assoc.analysisID
    uuid = ans.uuid
    if settings.ANALYSES_DEBUG:
        uuid = '0a0ff3c4-ef60-4f26-8241-298c57558916'
        repo = 'Irradiation-NM-321'
    plot_analysis(context, repo, uuid)


def get_analysis_path(repo, uuid, modifier=None):
    root, tail = uuid[:2], uuid[2:]
    path = os.path.join('/home/app', repo, root)
    if modifier:
        path = os.path.join(path, modifier)
        if modifier == '.data':
            modifier = 'dat'
        else:
            modifier = modifier[:4]

        tail = f'{tail}.{modifier}'
    path = os.path.join(path, f'{tail}.json')

    # path = os.path.join('/home/app', repo, root, '.data', f'{tail}.dat.json')

    return path


def plot_analysis(context, repo, uuid):
    path = get_analysis_path(repo, uuid)
    with open(path, 'r') as rfile:
        jobj = json.load(rfile)

    ts = jobj['timestamp']
    for fmt in ('%Y-%m-%d %H:%M:%S',"%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            rundt = datetime.datetime.strptime(ts, fmt)
            break
        except ValueError:
            continue

    runid = f'{jobj["identifier"]}-{jobj["aliquot"]}{jobj["increment"] or ""}'
    rows = [('Irradiation', f'{jobj["irradiation"]} {jobj["irradiation_level"]}{jobj["irradiation_position"]}'),
            ('RunID', runid),
            ('Run Delta', str(datetime.datetime.now()-rundt))]

    rows.extend([(k, jobj[k] or '') for k in ('project',
                                              'sample',
                                              'timestamp',
                                              'comment',
                                              'note',
                                              'experiment_queue_name',
                                              'measurement',
                                              'extraction'
                                              )])
    # context['table'] = rows
    path = get_analysis_path(repo, uuid, '.data')

    with open(path, 'r') as rfile:
        dataobj = json.load(rfile)
        # x = [1,2,3,4]
        # y = [1,23,123,31]
        signals = dataobj['signals']
        figures = []
        fmt = dataobj['format']
        for si in signals:
            x, y = unpack(si['blob'], fmt)

            plot = figure(y_axis_label=si['isotope'],
                          height=150)
            plot.scatter(x, y)
            figures.append(bokeh.embed.json_item(plot, si['isotope']))
            # script, div = components(plot)
            # figures.append((script, div))

        analyses = context.get('analyses', [])
        analyses.append({'runid': runid, 'figures': figures, 'table': rows})
        context['analyses'] = analyses


def clone_repo(name):
    if settings.ANALYSES_DEBUG:
        name = 'Irradiation-NM-321'

    organization = settings.PYCHRON_DATA_ORGANIZATION
    url = f'https://github.com/{organization}/{name}'
    print(f'clone repo {name} url={url}')
    repo_path = f'/home/app/{name}'
    if not os.path.isdir(repo_path):
        try:
            Repo.clone_from(url, repo_path)
            print(f'repo {name} cloned')
        except GitCommandError as e:
            print(e)
    else:
        print('repo already exists. pulling')
        repo = Repo(repo_path)
        o = repo.remotes.origin
        o.fetch()
        repo.git.merge('FETCH_HEAD')

# ============= EOF =============================================
