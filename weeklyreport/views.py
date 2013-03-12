# coding=utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.timezone import utc
from models import *
from weeklyreport.forms import WeeklyReportForm
import datetime
import time

# weeklyreport management
@login_required
def weeklyreport_list(request):
    if request.GET.get('num_per_page'):
        request.session['num_per_page'] = request.GET.get('num_per_page')
        return HttpResponseRedirect('/weeklyreport/')
    else:
        try:
            request.session['num_per_page']
        except KeyError:
            request.session['num_per_page'] = 25
    page = request.GET.get('page')
    pm_id = request.GET.get('pm_id')
    w = request.GET.get('week')
    if pm_id:
        pm = Xiangmujingli.objects.get(id=pm_id)
        if w:            
            weeklyreport_list = WeeklyReport.objects.filter(xiangmujingli=pm, week=w)
        else:
            weeklyreport_list = WeeklyReport.objects.filter(xiangmujingli=pm)
    else:
        if w:            
            weeklyreport_list = WeeklyReport.objects.filter(week=w)
        else:
            weeklyreport_list = WeeklyReport.objects.all()
    paginator = Paginator(weeklyreport_list, request.session['num_per_page'])
    try:
        weeklyreports = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        weeklyreports = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        weeklyreports = paginator.page(paginator.num_pages)

    xiangmujingli_list = Xiangmujingli.objects.all()
    return render_to_response('weeklyreport/list.html', locals(), context_instance=RequestContext(request))

# add
@login_required
def weeklyreport_add(request):
    if request.method == 'POST':
        form = WeeklyReportForm(request.POST, request.FILES)
        if form.is_valid():
            wr = form.save(commit=False)
            xiangmujingli = Xiangmujingli.objects.get(user=request.user)
            wr.xiangmujingli = xiangmujingli
            if (request.POST.get('week') == 'this_week'):
                wr.week = time.strftime('%Y-%m-%d', time.localtime(get_week_begin()))
            elif (request.POST.get('week') == 'last_week'):
                wr.week = time.strftime('%Y-%m-%d', time.localtime(get_week_begin(N= -1)))
            wr.save()
            return HttpResponseRedirect('/weeklyreport/')
    else:
        week_begin_day = time.strftime('%Y-%m-%d', time.localtime(get_week_begin()))
        week_end_day = time.strftime('%Y-%m-%d', time.localtime(get_week_end()))
        last_week_begin_day = time.strftime('%Y-%m-%d', time.localtime(get_week_begin(N= -1)))
        last_week_end_day = time.strftime('%Y-%m-%d', time.localtime(get_week_end(N= -1)))
        form = WeeklyReportForm()
    return render_to_response('weeklyreport/form.html', locals(), context_instance=RequestContext(request))

def get_week_begin(ts=time.time(), N=0):
    """
    N为0时获取时间戳ts当周的开始时间戳，N为负数时前数N周，N为整数是后数N周，此函数将周一作为周的第一天
    """
    w = int(time.strftime('%w', time.localtime(ts)))
    return get_day_begin(int(ts - (w - 1) * 86400)) + N * 604800
def get_week_end(ts=time.time(), N=0):
    w = int(time.strftime('%w', time.localtime(ts)))
    return get_day_begin(int(ts - (w - 1) * 86400), N=6) + N * 604800
def get_day_begin(ts=time.time(), N=0):
    """
    N为0时获取时间戳ts当天的起始时间戳，N为负数时前数N天，N为正数是后数N天
    """
    return int(time.mktime(time.strptime(time.strftime('%Y-%m-%d', time.localtime(ts)), '%Y-%m-%d'))) + 86400 * N

# delete
@login_required
def weeklyreport_delete(request, wr_id):
    wr = WeeklyReport.objects.get(id=wr_id)
    if wr.xiangmujingli == Xiangmujingli.objects.get(user=request.user):
        wr.delete()
    return HttpResponseRedirect('/weeklyreport/')

# change
@login_required
def weeklyreport_edit(request, wr_id):
    wr = WeeklyReport.objects.get(id=wr_id)
    if wr.xiangmujingli == Xiangmujingli.objects.get(user=request.user):
        if request.method == 'POST':
            form = WeeklyReportForm(request.POST, request.FILES, instance=wr)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/weeklyreport/')
        else:
            form = WeeklyReportForm(instance=wr)
        return render_to_response('weeklyreport/form.html', {'form': form}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/weeklyreport/')
