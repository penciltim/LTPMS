#coding=utf-8
from django import forms
from project.models import Project, WeeklyReport

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('xiangmujingli',)
        
class WeeklyReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        exclude = ('xiangmujingli',)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()