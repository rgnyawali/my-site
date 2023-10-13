from django.urls import path, include
from . import views
from .views import CompanyAutocompleteView, CompanyModel
from .models import Company
from dal import autocomplete
app_name='finapp'

urlpatterns = [
    path('', views.mainview, name='main_view'),
    path('stock/',views.StockSelectionView.as_view(), name='stock_selection'),
    path('realestate/',views.RealEstateView.as_view(), name='real_estate'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('privacy/',views.privacy, name='privacy'),
    path('termsofuse/',views.termsofuse, name='termsofuse'),
   
    path('companyautocomplete/',CompanyAutocompleteView.as_view(),name='companyautocomplete'),
    # path('compan/',views.CompanyModel.as_view(),name='finapp/compan')
    # path('companyautocomplete/',autocomplete.Select2QuerySetView.as_view(model=Company),name='companyautocomplete')
    ]
