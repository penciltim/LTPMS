#coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Xiangmujingli(models.Model):
    xiangmujingli = models.CharField(u'名字', max_length=4)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.xiangmujingli
    class Meta:
        verbose_name = u"项目经理"
        verbose_name_plural = verbose_name

class Changjia(models.Model):
    changjiamingcheng = models.CharField(u'厂家名称', max_length=50)
    def __unicode__(self):
        return self.changjiamingcheng
    class Meta:
        verbose_name = u"厂家"
        verbose_name_plural = verbose_name

class Project(models.Model):
    xiangmunianfen = models.CharField(u'年份', max_length=4, choices=[('2009',2009),('2010',2010),('2011',2011),('2012',2012),('2013',2013)])
    xiangmumingcheng = models.CharField(u'项目名称', max_length=150)
    xiangmujingli = models.ForeignKey(Xiangmujingli, verbose_name='项目经理')
    xiangmubianhao = models.CharField(u'项目编号', max_length=14)
    keyanpifuhao = models.CharField(u'可研批复号', max_length=150)
    keyanpifujine = models.FloatField(u'可研批复金额', )
    keyanpifuriqi = models.DateField(u'可研批复日期', )
    shejipifuhao = models.CharField(u'设计批复号', max_length=150)
    shejipifujine = models.FloatField(u'设计批复金额', )
    shejipifuriqi = models.DateField(u'设计批复日期', )
    xiangmuzhuangtai = models.CharField(u'项目状态', max_length=20)
    def __unicode__(self):
        return self.xiangmumingcheng
    class Meta:
        verbose_name = u"项目"
        verbose_name_plural = verbose_name

class Purchase(models.Model):
    caigouxuqiudanmingcheng = models.CharField(u'采购需求单名称', max_length= 100)
    project = models.ForeignKey(Project)
    caigouneirong = models.TextField(u'采购内容')
    caigouriqi = models.DateField(u'采购需求批复日期')
    caigoujine = models.FloatField(u'采购需求批复金额')
    def __unicode__(self):
        return self.caigouxuqiudanmingcheng
    class Meta:
        verbose_name = u"采购"
        verbose_name_plural = verbose_name

class Contract(models.Model):
    purchase = models.ForeignKey(Purchase)    
    biao1riqi = models.DateField(u'表一批复日期')
    biao2riqi = models.DateField(u'表二批复日期')
    hetongriqi = models.DateField(u'合同签订日期')
    hetongmingcheng = models.CharField(u'合同名称', max_length=150)
    hetongbianhao = models.CharField(u'合同编号', max_length=150)
    hetongjine = models.FloatField(u'合同金额')
    changjia = models.ForeignKey(Changjia)
    hetongzhuangtai = models.CharField(u'合同状态', max_length=150)
    def __unicode__(self):
        return self.hetongmingcheng
    class Meta:
        verbose_name = u"合同"
        verbose_name_plural = verbose_name

class Order(models.Model):
    contract = models.ForeignKey(Contract)
    dingdanbianhao = models.CharField(u'订单编号', max_length=150)
    dingdanshejidishi = models.CharField(u'涉及地市', max_length=20)
    shifouruzhang = models.BooleanField(u'是否入账')
    def __unicode__(self):
        return self.dingdanbianhao
    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name
        
class WeeklyReport(models.Model):
    gongzuofenlei = models.CharField(u'工作分类', max_length=20)
    xiangmumingcheng = models.CharField(u'项目名称', max_length=150)
    zixiangmu = models.CharField(u'子项目', max_length=150)
    xiangmujingli = models.ForeignKey(Xiangmujingli, verbose_name='项目经理')
    jinzhan = models.CharField(u'累计进展', max_length=20)
    benzhoujinzhan = models.TextField(u'本周进展')
    xiazhoujihua = models.TextField(u'下周计划')
    cunzaiwenti = models.TextField(u'存在问题')
    jiejuejianyi = models.TextField(u'解决建议')
    jiejueshijian = models.DateField(u'解决时间')
    shuchuwendang = models.FileField(u'输出文档', upload_to='weeklyreport/')
    class Meta:
        verbose_name = u"周报"
        verbose_name_plural = verbose_name