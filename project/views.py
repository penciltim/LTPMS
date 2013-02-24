# coding=utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from models import *
from project.forms import ProjectForm

@login_required
def home(request):
    return render_to_response('home.html', locals())

@login_required
def project_list(request):
    if request.GET.get('num_per_page'):
        request.session['num_per_page'] = request.GET.get('num_per_page')
        return HttpResponseRedirect('/project/')
    else:
        try:
            request.session['num_per_page']
        except KeyError:
            request.session['num_per_page'] = 25
    page = request.GET.get('page')
#    need to get all objects everytime?
    project_list = Project.objects.all()
    paginator = Paginator(project_list, request.session['num_per_page'])
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        projects = paginator.page(paginator.num_pages)
#    assert False
    return render_to_response('project/project_list.html', locals(), context_instance=RequestContext(request))

def project_view(request, project_id):
    p = Project.objects.get(id=project_id)
    form = ProjectForm(instance=p)
    return render_to_response('project/project_view.html', {'form': form})

# add
@login_required
def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            xiangmujingli = Xiangmujingli.objects.get(user=request.user)
            p.xiangmujingli = xiangmujingli
            form.save()
            return HttpResponseRedirect('/project/')
    else:
        form = ProjectForm()
    return render_to_response('project/project_form.html', {'form': form}, context_instance=RequestContext(request))

# delete
@login_required
def project_delete(request, project_id):
    p = Project.objects.get(id=project_id)
    if p.xiangmujingli == Xiangmujingli.objects.get(user=request.user):
        p.delete()
    return HttpResponseRedirect('/project/')

# change
@login_required
def project_edit(request, project_id):
    p = Project.objects.get(id=project_id)
    if p.xiangmujingli == Xiangmujingli.objects.get(user=request.user):
        if request.method == 'POST':
            form = ProjectForm(request.POST, instance=p)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/project/')
        else:
            form = ProjectForm(instance=p)
        return render_to_response('project/project_form.html', {'form': form}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/project/')

def purchase(request):
    purchase_list = Purchase.objects.all()
    return render_to_response('project/purchase_list.html', locals())

def about(request):
    return render_to_response('about.html')

def display_meta(request):
    values = request.META.items()
    values.sort()
    return render_to_response('display_meta.html', locals())

def test(request):
    request.session['fav_color'] = 'blue'
    fav_color = request.session['fav_color']
    del request.session['fav_color']
    if request.user.is_authenticated():
        user = request.user.username
        assert False
    else:
        assert False
