from django.urls import path, include
from . import views


urlpatterns = [
    path('get_ads/<int:page_n>/', views.get_ads, name='get_all_ads'),
    path('create_ad/', views.create_ad, name='create_ad'),
    path('edit_ad/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('delete_ad/<int:ad_id>/', views.delete_ad, name='delete_ad'),
    path('create_prop/<int:ad_r_id>/', views.create_proposal, name='create_prop'),
    path('accept_prop/<int:prop_id>/', views.accept_proposal, name='accept_prop'),
    path('reject_prop/<int:prop_id>/', views.reject_proposal, name='reject_prop'),
    path('get_props/', views.get_proposals, name='get_all_props'),
]