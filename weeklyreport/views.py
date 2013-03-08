# coding=utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from models import *
from weeklyreport.forms import WeeklyReportForm

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
#    assert False
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
            wr.save()
            return HttpResponseRedirect('/weeklyreport/')
    else:
        form = WeeklyReportForm()
    return render_to_response('weeklyreport/form.html', {'form': form}, context_instance=RequestContext(request))

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