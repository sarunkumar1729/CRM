from django.urls import path,include
from . import views

urlpatterns = [
   path('Home/',views.Home,name='Staff_Home')
]