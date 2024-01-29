from django.contrib import admin
from django.urls import path
from My_Prediction.views import home, register,login_page,results,contact
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),   
    path('register/', register, name='register'),
    path('login/',login_page, name='login'),
    path('results/',results, name='results'),
    path('contact/',contact, name='contact'),
    #path('prected/',prected, name='prected'),
    
    
    
]

