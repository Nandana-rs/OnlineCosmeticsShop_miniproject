    
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
from .views import user_profile
from .views import save_profile  # Import your view
from .views import user_details
from .views import order_history

# from .views import checkout
# #proceed to payement -> checkout

# from .views import checkout_success
# from .views import process_checkout
# #proceed to payement -> checkout

from .views import product_list
from .views import product_detail

from .views import admin_dashboard ,user_view
from .views import change_password 
from .views import add_to_cart
from .views import remove_from_cart
from .views import view_cart
from .views import increase_cart_item
from .views import decrease_cart_item
from .views import fetch_cart_count
from .views import create_order
from .views import handle_payment
from .views import checkout

from .views import bill_invoice
from .views import seller_orders

from .views import add_edit_service , view_bridal_packages
from .views import BeauticianCRUD, edit_beautician
from .views import service_detail
from .views import beautician_profile_form , beautician_profile
from .views import chatgpt, generate_response

from .views import upload_video
from .views import display_videos
from .views import beautician_profile_form, submit_profile

from .views import success_page
from .views import beautician_list







urlpatterns =  [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    
    path('logout/', views.logout_view, name='logout'),
    path('home2/', views.home2, name='home2'),
    path('seller_template/',views.seller_template ,name='seller_template'),
    path('adminpanel/', admin_dashboard, name='adminpanel'),

    path('user/', user_view, name='user'),
    path('add_product/', views.add_product, name='add_product'),
  
   #here google starts
    path('auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    #here google ends

    path('sellerRegistration/', views.sellerRegistration, name='sellerRegistration'),
    path('MakeupArtist/', views.MakeupArtist, name='MakeupArtist'),
    path('MakeupArtistTemplate/', views.MakeupArtistTemplate, name='MakeupArtistTemplate'),
    

    #admin adding products
    #prodcut_list.html
    # path('product_list/', views.product_list, name='product_list'),
    path('products/', product_list, name='product_list'),
    path('products/<int:category_id>/', product_list, name='product_list_by_category'),
    path('products/<int:category_id>/<int:subcategory_id>/', product_list, name='product_list_by_subcategory'),
    path('products/<int:pk>/', product_detail, name='product_detail'),

    #seller viewing added products
    path('seller/products/', views.seller_products, name='seller_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('deactivate_product/<int:product_id>/', views.deactivate_product, name='deactivate_product'),
    path('seller-orders/', seller_orders, name='seller_orders'),

    

#page for displaying subcategory serums
    path('serums_products/', views.serums_products, name='serums_products'),
#page for displaying subcategory foundations
    path('foundations_products/', views.foundations_products, name='foundations_products'),
 #page for wishlist and cart   
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Remove product from cart
    #  path('cart/', views.cart, name='cart'),
    
    # path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # # Clear the cart
    # path('clear_cart/', views.clear_cart, name='clear_cart'),
    
    # # Proceed to checkout
    # path('checkout/', views.checkout, name='checkout'),


    # Add the user profile URL
 
    path('user_profile/', user_profile, name='user_profile'),
    path('save_profile/', save_profile, name='save_profile'),
    path('userdetails/', user_details, name='user_details'),
    path('change_password/', change_password, name='change_password'),
    path('order_history/', order_history, name='order_history'),

    

# #proceed to payement -> checkout
#     path('checkout/', checkout, name='checkout'),
#     path('checkout/success/', checkout_success, name='checkout_success'),
#     path('process_checkout/', process_checkout, name='process_checkout'),
#proceed to payement -> checkout




#nandana new cart
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/', view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', decrease_cart_item, name='decrease-cart-item'),    
    path('fetch-cart-count/', fetch_cart_count, name='fetch-cart-count'),
   
    path('create-order/', create_order, name='create-order'),
    path('handle-payment/', handle_payment, name='handle-payment'),
    path('checkout/', checkout, name='checkout'),
    path('billinvoice/', bill_invoice, name='bill_invoice'),
     


    #chatbot
    path('chatbot/', views.chatbot, name='chatbot'),
    path('get_dialogflow_response/', views.get_dialogflow_response, name='get_dialogflow_response'),
  
  
    

   # bridalmakeup booking
    

    path('Brideindex/', views.bride_index_view, name='Brideindex'), 
      # Replace 'bride_index_view' with the actual view function
    path('Bridal_makeup/about.html', views.bride_about_view, name='Brideabout'),  # Replace 'bride_about_view' with the actual view function
    path('Bridal_makeup/contact.html', views.bride_contact_view, name='Bridecontact'),  # Replace 'bride_contact_view' with the actual view function
    path('MakeupArtistTemplate/add_edit_service.html', add_edit_service, name='add_edit_service'),
    path('customer/bridal-packages/', view_bridal_packages, name='customer_bridal_packages'),
  

    path('MakeupArtistTemplate/beautician_crud.html', BeauticianCRUD.as_view(), name='beautician_crud'),
    path('edit_beautician/', edit_beautician, name='edit_beautician'),  # Without service_id
    # path('edit_beautician/<int:service_id>/', edit_beautician, name='edit_beautician_with_id'),  # With service_id
    path('edit_beautician/<int:service_id>/', edit_beautician, name='edit_beautician'),
    path('service_detail/<int:service_id>/', service_detail, name='service_detail'),
    path('MakeupArtistTemplate/beautician_profile_form.html', beautician_profile_form, name='beautician_profile_form'),

    path('beautician-profile-form/', beautician_profile_form, name='beautician_profile_form'),
    path('submit-profile/', submit_profile, name='submit_profile'),

    path('success/', success_page, name='success_page'),



    #chatgpt nrs

    path('chatgpt/', chatgpt, name='chatgpt'),
    path('generate-response/', generate_response, name='generate_response'),

    # videao upload
     path('MakeupArtistTemplate/upload_video.html', upload_video, name='upload_video'),
     path('display_videos/', display_videos, name='display_videos'),
    
    path('beauticians/', beautician_list, name='beautician_list'),
    path('view-profile/', beautician_profile, name='beautician_profile'),
    
    
    
   
    

    

    
  

    

    #forgetpassword
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

