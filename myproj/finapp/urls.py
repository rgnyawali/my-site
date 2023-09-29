from django.urls import path, include
from . import views

app_name='finapp'

urlpatterns = [
    path('', views.mainview, name='main_view'),
    path('stock/',views.StockSelectionView.as_view(), name='stock_selection'),
    path('realestate/',views.RealEstateView.as_view(), name='real_estate'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('privacy/',views.privacy, name='privacy'),
    path('termsofuse/',views.termsofuse, name='termsofuse'),

    ]
