

# Create your models here.
#from django.db import models
#from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
     def create_user(self, username, email, password=None):
         if not email:
             raise ValueError('User must have an email address')

         user = self.model(
             email=self.normalize_email(email),
             #name= name,
             #last_name=last_name,
             #phone=phone, 
         )
         user.set_password(password)
         user.save(using=self._db)
         return user

     def create_superuser(self, email, password=None):
        
         user = self.create_user(
              email=self.normalize_email(email),
              password=password,
              #name=name,
              #last_name=last_name,
             # phone=phone,
              )
         user.is_admin = True
         user.is_active = True
         user.is_staff = True
         user.is_superadmin = True
         user.role=1
         user.save(using=self._db)
         return user

class CustomUser(AbstractUser):
    ADMIN = 1
    CUSTOMER = 2
    DELIVERYTEAM = 3
    SELLER = 4

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (DELIVERYTEAM, 'Deliveryteam'),
        (SELLER,'Seller'),
    )

    #username=None
    user_types = models.PositiveSmallIntegerField(choices=USER_TYPES,default='2')
    #name = models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    #last_name = models.CharField(max_length=50)
    #USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
   # phone = models.CharField(max_length=12, blank=True)
    password = models.CharField(max_length=128)
   # confirmPassword = models.CharField(max_length=128)
    #role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')

    #usertype=SELLER starts

    shop_name=models.CharField(max_length=255, null=True)
    user_name=models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=12, blank=True)
    shop_address=models.CharField(max_length=255, null=True)
    tax_id=models.CharField(max_length=20, null=True)
    

    #  #usertype=SELLER ends







    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)


    #REQUIRED_FIELDS = ['first_name','last_name', 'phone']

    objects = UserManager()

    def str(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    # country = models.CharField(max_length=15, default="India", blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)


    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    age = property(calculate_age)


    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender)

    def str(self):
        return self.user.email
    
    def get_role(self): 
        if self.user_type == 2:
            user_role = 'Customer'
        elif self.user_type == 3:
            user_role = 'Deliveryteam'
        elif self.user_type == 4:
            user_role = 'Seller'
        
        return user_role
#cmd  -- python manage.py makemigrations
#        python manage.py migrate

#ADDING PRODUCTS BY ADMIN AND SELLER NECESSITIES



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

