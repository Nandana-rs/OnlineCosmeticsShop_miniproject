    
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
from django.contrib.auth.views import LogoutView


urlpatterns =  [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    
    path('logout/', views.logout_view, name='logout'),
    path('home2/', views.home2, name='home2'),
    path('seller_template/',views.seller_template ,name='seller_template'),
    path('add_product/', views.add_product, name='add_product'),
  
   #here google starts
    path('auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    #here google ends

    path('sellerRegistration/', views.sellerRegistration, name='sellerRegistration'),

    #admin adding products
    path('product_list/', views.product_list, name='product_list'),
    #seller viewing added products
    path('seller/products/', views.seller_products, name='seller_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('deactivate_product/<int:product_id>/', views.deactivate_product, name='deactivate_product'),
#customers profile view in home2.html
    path('user_profile/', views.user_profile, name='user_profile'),
#customer changing passwird
    path('change_password/', views.change_password, name='change_password'),
#seller viewing profile 
    path('seller_template/seller_profile', views.seller_profile, name='seller_profile'),
    

    
  

    

    #forgetpassword
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

