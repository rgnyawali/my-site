from django.db import models
from django.conf import settings
from datetime import datetime


# Create your models here.
class Industry(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Company(models.Model):
    name=models.CharField(max_length=100)
    longticker=models.CharField(max_length=20, null=True, blank=True)
    ticker=models.CharField(max_length=15)
    # industry=models.ForeignKey('Industry',related_name='industry',on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}:{self.ticker}'

class HousePrice(models.Model):
    ref_date = models.DateField()
    symbol=models.CharField(max_length=250)
    vector = models.CharField(max_length=250)
    coordinate = models.FloatField(null=True)
    value = models.FloatField(null=True)
    status=models.CharField(max_length=250)

    def __str__(self):
    	return self.symbol

class Contact(models.Model):
    comment = models.TextField()
    return_email=models.EmailField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.comment) < 15: return self.comment
        return self.comment[:11] + " ..."

class BasicData(models.Model):
    date=models.DateField()
    rf_rate=models.FloatField(null=True)
    erp=models.FloatField(null=True)
    gdp=models.FloatField(null=True)

    def __str__(self):
        return datetime.strftime(self.date,'%m,%d,%Y')


class CompanyBeta(models.Model):
    symbol=models.CharField(max_length=10)
    beta=models.FloatField(null=True)

    def __str__(self):
        return '{}:{}'.format(self.symbol,self.beta)

class GlobalData(models.Model):
    qend=models.DateField(null=True)
    longticker=models.CharField(max_length=25,null=True)
    revenue=models.FloatField(null=True)
    ebitda=models.FloatField(null=True)
    ecos=models.FloatField(null=True)
    ev=models.FloatField(null=True)
    mcap=models.FloatField(null=True)
    period=models.CharField(max_length=10, null=True)
    annlrev=models.FloatField(null=True)
    annlebitda=models.FloatField(null=True)
    annlecos=models.FloatField(null=True)
    pp1mcap=models.FloatField(null=True)
    pp2mcap=models.FloatField(null=True)
    pp1annlrev=models.FloatField(null=True)
    pp2annlrev=models.FloatField(null=True)
    revg6m=models.FloatField(null=True)
    revg3m=models.FloatField(null=True)
    ecosmgn=models.FloatField(null=True)
    pp1annlecos=models.FloatField(null=True)
    pp2annlecos=models.FloatField(null=True)
    conmgn3m=models.FloatField(null=True)
    conmgn6m=models.FloatField(null=True)
    mcapg3m=models.FloatField(null=True)
    mcapg6m=models.FloatField(null=True)
    exch=models.CharField(max_length=15, null=True)
    tick=models.CharField(max_length=10, null=True)
    beta=models.FloatField(null=True)
    industry=models.CharField(max_length=100, null=True)
    indrev=models.FloatField(null=True)
    indecos=models.FloatField(null=True)
    indmgm=models.FloatField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.tick, self.period)


class BackTestData(models.Model):
    period=models.CharField(max_length=10)
    ticker=models.CharField(max_length=25)
    mcap=models.FloatField(null=True,blank=True)
    mcapg3m=models.FloatField(null=True,blank=True)
    mcapg6m=models.FloatField(null=True,blank=True)
    flag_val=models.CharField(max_length=20,null=True,blank=True)
    flag_revg=models.CharField(max_length=20,null=True,blank=True)
    flag_revga3y=models.CharField(max_length=20,null=True,blank=True)
    flag_igr=models.CharField(max_length=20,null=True,blank=True)
    flag_mgn=models.CharField(max_length=20,null=True,blank=True)
    flag_disc_prem=models.CharField(max_length=20, null=True,blank=True)
    flag_disc_prem_cy=models.CharField(max_length=20,null=True,blank=True)
    flag_mcap=models.CharField(max_length=20,null=True,blank=True)
    flag_spread_yoy=models.CharField(max_length=20,null=True,blank=True)
    flag_spread_3ya=models.CharField(max_length=20,null=True,blank=True)

    #flag_debt=models.CharField(max_length=20,null=True,blank=True)
    #flag_strategy=models.CharField(max_length=20,null=True,blank=True)

    class Meta:
        unique_together = ('period','ticker')

