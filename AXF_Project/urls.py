from django.contrib import admin
from django.urls import path, include

from mainapp import views
import xadmin

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # path('',views.home),
    path('',include('mainapp.urls'))
]
