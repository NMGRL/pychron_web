import base64
import json
import os.path
import struct

import bokeh.embed
from bokeh.embed import components
from bokeh.plotting import figure
from celery import shared_task, current_app
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
# from django.views.generic import DetailView
#
# from projects.filters import ProjectFilter
# from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from tasks import make_all_series, make_recent_analyses


class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()
        return JsonResponse(response_data)


@login_required
def series(request):
    context = {}

    task = make_all_series.delay()
    context['task_id'] = task.id
    context['task_status'] = task.status
    # ar40, ar36, ratios = zip(*[make_series(atype) for atype in ('cocktail', 'air', 'blank_unknown', 'blank_cocktail',
    #                                                             'blank_air')])
    # context['ar40'] = ar40
    # context['ar36'] = ar36
    # context['ratios'] = ratios
    template = loader.get_template('analyses/series.html')
    return HttpResponse(template.render(context, request))


@login_required
def recent_analyses(request):
    # get the last n analyses
    # group by repository identifier
    # clone each identifier
    # extract regressions
    # plot each isotope

    context = {}
    task = make_recent_analyses.delay()
    context['task_id'] = task.id
    context['task_status'] = task.status
    context['isotags'] = ['Ar40', 'Ar39', 'Ar38', 'Ar37', 'Ar36']
    # for repo, uuid in (('Irradiation-NM-321', '0a0ff3c4-ef60-4f26-8241-298c57558916'),):
    #     plot_analyses(context, repo, uuid)
    # for a in analyses:
    #     plot_analyses(context, )
    template = loader.get_template('analyses/recent.html')
    return HttpResponse(template.render(context, request))


