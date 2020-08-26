from django.urls import path

from . import views


urlpatterns = [
    path('myprofile/', views.ProfileViewSet.as_view({'get': 'list'})),
    path('transfer/', views.TransferViewSet.as_view({'post': 'create'})),
]