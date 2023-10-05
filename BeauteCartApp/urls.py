    
#from django.contrib import admin already existed
#from django.urls import path
#from. import views



#urlpatterns = [
    # path('', views.home,name="home"),
    
    #path('admin/', admin.site.urls) already existed one


   # path('about/', views.about, name='about'),
     #path('registration/', views.registration,name='registration'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout_view, name='logout'),
   

    
         
#]
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('seller_template/',views.seller_template ,name='seller_template'),

    path('auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),

    path('sellerRegistration/', views.sellerRegistration, name='sellerRegistration'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

