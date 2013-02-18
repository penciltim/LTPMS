# coding=utf-8
from django.core.context_processors import csrf
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from models import *
from project.forms import ProjectForm

def base_site(request):
    return render_to_response('base_site.html', locals(), context_instance=RequestContext(request))

def project_list(request):
    page = request.GET.get('page')
    num_per_page = request.GET.get('num_per_page')
    if not num_per_page:
        num_per_page = 25
#    need to get all objects everytime?
    project_list = Project.objects.all()
    paginator = Paginator(project_list, num_per_page)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        projects = paginator.page(paginator.num_pages)
#    assert False
    return render_to_response('project/project_list.html', locals())

def project_view(request, project_id):
    p = Project.objects.get(id=project_id)
    form = ProjectForm(instance=p)
    return render_to_response('project/project_view.html', {'form': form})

# 增
def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/project/')
    else:
        form = ProjectForm()
    return render_to_response('project/project_form.html', {'form': form})
# 删
def project_delete(request, project_id):
    Project.objects.get(id=project_id).delete()
    return HttpResponseRedirect('/project/')

# 改
def project_update(request):
    project_list = Project.objects.all()
    return render_to_response('project/project.html', locals())

# 查
def project_edit(request, project_id):
    p = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/project/')
    else:
        form = ProjectForm(instance=p)
    return render_to_response('project/project_form.html', {'form': form})


def purchase(request):
    purchase_list = Purchase.objects.all()
    return render_to_response('project/purchase_list.html', locals())

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
