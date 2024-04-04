from django.contrib import admin

# Register your models here.

from .models import CustomUser
from .models import Category, Subcategory, Brand, Product ,WishlistItem ,Cart1 , CartItem1,ProfileUser ,Order ,OrderItem,MakeupType,Service1

# Register your models here.
#admin.site.register (CustomUser)

# hiding admin

from django.contrib.auth import get_user_model

User = get_user_model()

class SuperuserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return User.objects.filter(is_superuser=False)

# Register the custom admin class
admin.site.register(User, SuperuserAdmin)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(WishlistItem)
admin.site.register(Cart1)
admin.site.register(CartItem1)
admin.site.register(ProfileUser)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(MakeupType)
admin.site.register(Service1)

# In admin.py
from django.contrib import admin
from .models import LogisticsCompany

class LogisticsCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone_number', 'address', 'license')  # Define fields to display in the admin list view
    search_fields = ('company_name', 'contact_person', 'email')  # Add fields for search functionality
    list_filter = ('license',)  # Add filters for the admin list view

# Register the admin class and model
admin.site.register(LogisticsCompany, LogisticsCompanyAdmin)

