# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from project.models import Xiangmujingli
        
class WeeklyReport(models.Model):
    gongzuofenlei = models.CharField(u'工作分类', max_length=20, blank=True)
    xiangmumingcheng = models.CharField(u'项目名称', max_length=150, blank=True)
    zixiangmu = models.CharField(u'子项目', max_length=150, blank=True)
    xiangmujingli = models.ForeignKey(Xiangmujingli, verbose_name='项目经理')
    jinzhan = models.CharField(u'累计进展', max_length=20, blank=True)
    benzhoujinzhan = models.TextField(u'本周进展', blank=True)
    xiazhoujihua = models.TextField(u'下周计划', blank=True)
    cunzaiwenti = models.TextField(u'存在问题', blank=True)
    jiejuejianyi = models.TextField(u'解决建议', blank=True)
    jiejueshijian = models.CharField(u'解决时间', max_length=20, blank=True)
    shuchuwendang = models.FileField(u'输出文档', upload_to='weeklyreport/', blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    class Meta:
        verbose_name = u"周报"
        verbose_name_plural = verbose_name
