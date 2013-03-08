#coding=utf-8
from django import forms
from weeklyreport.models import WeeklyReport

        
class WeeklyReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        exclude = ('xiangmujingli',)