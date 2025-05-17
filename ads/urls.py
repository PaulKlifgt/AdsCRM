from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('get_all_ads/', views.get_all_ads, name='get_all_ads'),
    path('create_ad/', views.create_ad, name='create_ad'),
    path('edit_ad/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('create_prop/<int:ad_r_id>/', views.create_proposal, name='create_prop'),
    path('accept_prop/<int:prop_id>/', views.accept_proposal, name='accept_prop'),
]