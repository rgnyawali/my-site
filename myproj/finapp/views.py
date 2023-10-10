from django.shortcuts import render, redirect
from django.views import View
from .forms import LocationForm, TickerInput, ContactForm
#from .scripts import stock_calculation, main_calculation
# from .newscript import main_calculation
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.forms import formset_factory
from .models import HousePrice, BasicData, CompanyBeta

from django.forms import modelformset_factory
# from .forms import Ticker
# from .alphascript import alpha_calc

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io, base64
from matplotlib.ticker import LinearLocator
import seaborn as sns
import datetime as dt
sns.set_theme(style='darkgrid')
import yfinance as yf
from django import forms
from dal import autocomplete
from .models import Company
#import yahooquery as yq

#===========================================================
# Landing Page View
#===========================================================
def mainview(request):
    try:
        tickers=yf.download(tickers=['^IXIC','^GSPTSE','CADUSD=X','^DJI','^GSPC'], period='1d')['Close'].values.flatten().tolist()
    except:
        tickers=['Data Unavailable'] * 4

    context = {'tickers':tickers, 'is_auth':'user.is_authenticated'}
    return render(request, 'finapp/main.html', context)

#===========================================================
# Privacy Policy Page View
#===========================================================
def privacy(request):
    context = {}
    return render(request, 'finapp/privacy.html', context)

#===========================================================
# Terms of Use Page View
#===========================================================
def termsofuse(request):
    context = {}
    return render(request, 'finapp/termsofuse.html', context)

#==================================================================
# Stock Selection View with company selection.
#==================================================================
class StockSelectionView(LoginRequiredMixin, View):
    # model=Company
    # form_class = TickerInput
    # template_name = "finapp/stockselection.html"
    # formset_class = modelformset_factory(
    #     model=Company,
    #     form=TickerInput,
    #     extra=1,
    #     fields=('name', 'ticker')
    #     )
    def get(self, request):
        #  Company=TickerInput()
         tick_form = Company.objects.all()
        #  print(tick_form)
         context={'tick_form':tick_form}
         return render(request, 'finapp/stockselection.html', context)
        # return Company.objects.first()
    def post(self,request):
        print(request.POST)
        tick_form=TickerInput(request.POST)
        
        if tick_form.is_valid():
            print("im here")
            ticker=tick_form.cleaned_data['ticker']
            comparative_table,tick_detail, new_result,plot1, plot2, waterfallchart=alpha_calc(ticker)
            context={'comparative':comparative_table, 'is_data':True, 'tick_detail':tick_detail, 'new_result':new_result,'plot1':plot1,'plot2':plot2,'waterfallchart':waterfallchart}
            return render(request, 'finapp/stockresult2.html',context)
        context={'tick_form':tick_form}
        return render(request, 'finapp/stockselection.html', context)

#===============================================================
# Real Estate View
#===============================================================
class RealEstateView(View):
    def get(self,request):
        form=LocationForm()
        context={'form':form,'msg':'get'}
        return render(request,'finapp/realestate.html',context)

    def post(self,request):
        form=LocationForm(request.POST)

        if form.is_valid():
            percentile=[]
            symbol=form.cleaned_data['location']

            #Getting data into table
            #--------------------------
            a = HousePrice.objects.only('value').filter(symbol=symbol).values()
            data=pd.DataFrame(a)
            data.columns=['Prg_Index','Ref_Date','Symbol','Vector','Coordinate','Value','Status']
            data['MA5Y']=data['Value'].rolling(20).mean()
            data['MA3Y']=data['Value'].rolling(12).mean()
            data['QReturn']=round(((data.Value/data.Value.shift(1))-1)*100,4)
            data['5YPrice']=data['Value'].shift(20).ffill()
            data['Five_YRet']=round(((data['Value']/data['5YPrice'])**(1/5)-1)*100,4)
            data=data.dropna()
            for Perc in (5,10,15,20,25,30,35,50,60,75,80,85):
                w =round(np.percentile(data.QReturn, Perc),3)
                y =round(np.percentile(data.Five_YRet, Perc),3)
                percentile.append((Perc,w,y))
                cols4=["Percentile","Quarterly Return (%)","5 Year Return (%)"]
                stat=pd.DataFrame(percentile,columns=cols4)
                #stat=stat.to_html()

            msg_1='There is more than {}% probability of getting an annual positive return.'.format(100-stat.iloc[stat.abs()['5 Year Return (%)'].idxmin()]['Percentile'])
            msg_2='You are likely to get an annual return of greater than {}% in 5 years.'.format(stat[stat['Percentile']==50].iloc[0]['5 Year Return (%)'])
            msg_3='There is 90% probability of getting an annual return greater than {}%.'.format(stat[stat['Percentile']==10].iloc[0]['5 Year Return (%)'])
            result_msg=[msg_1, msg_2, msg_3]
            #Making Chart
            #-------------
            b=HousePrice.objects.filter(symbol=symbol).values()
            df=pd.DataFrame(b)
            df.columns=['Prg_Index','Ref_Date','Symbol','Vector','Coordinate','Value','Status']
            df['Ref_Date']=pd.to_datetime(df['Ref_Date'])



            fig, ax = plt.subplots(figsize=(12,5))
            fig.autofmt_xdate()

            ax.xaxis.set_major_locator(mdates.YearLocator(base=2,month=12,day=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            ax.set_xlabel('Year',labelpad=8.0,color='Blue',size=14,alpha=0.65)
            ax.set_ylabel('Value (%)',labelpad=8.0,color='Blue',size=14,alpha=0.65)
            ax.set_title('Real Estate Trend from 1980-2022\n(Indexed 2016 = 100%)',size=18,alpha=0.8,color='blue',pad=10)
            ax.tick_params(colors='b',labelsize=11)


            sns.lineplot(ax=ax,data=df,x='Ref_Date',y='Value',label=symbol)
            ax.legend()


            flike = io.BytesIO()
            fig.savefig(flike)
            b64 = base64.b64encode(flike.getvalue()).decode()
            chart = b64


            return render(request, 'finapp/realestate.html',{'stat':stat.to_html(border=0,justify="center",index=False), 'form':form, 'chart':chart,'msg':'post','result_msg':result_msg})
        context={'form':form,'msg':'get'}
        return render(request, 'finapp/realestate.html',context)



#===============================================================
# Contact Form View
#===============================================================
class ContactView(LoginRequiredMixin, View):
    def get(self, request):
        form = ContactForm()
        context={'form':form}
        return render(request, 'finapp/contact.html',context)

    def post(self,request):
        form=ContactForm(request.POST)
        if form.is_valid():
            contact=form.save(commit=False)
            contact.owner=request.user
            contact.save()
            #print(form.cleaned_data['comment'])
            msg='Thank You'
            context={'msg':msg}
            return render(request,'finapp/main.html',context)
        context={'form':form}
        return render(request, 'finapp/contact.html',context)
    
class CompanyAutocompleteView(autocomplete.Select2ListView, View):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Company.objects.none()
            # return Ticker

        qs = Company.objects.all()
        # qs = Ticker

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
    
class CompanyModel(View):
    # def get_queryset(self):
    #     if not self.request.user.is_authenticated:
    #         return Company.objects.none()
        
    Company.objects.all()


