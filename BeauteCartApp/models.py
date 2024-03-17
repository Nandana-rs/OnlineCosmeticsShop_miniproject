

# Create your models here.
#from django.db import models
#from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone





class CustomUser(AbstractUser):
    ADMIN = 1
    CUSTOMER = 2
    DELIVERYTEAM = 3
    SELLER = 4
    

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (DELIVERYTEAM, 'Delivery Team'),
        (SELLER, 'Seller'),
    )

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default=CUSTOMER)

    # Additional fields for the SELLER user type
    shop_name = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=12, blank=True)
    shop_address = models.CharField(max_length=255, null=True)
    tax_id = models.CharField(max_length=20, null=True)

     # Additional fields for the MAKEUP ARTIST user type
    parlour_name = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=12, blank=True)
    parlour_address = models.CharField(max_length=255, null=True)
    tax_id = models.CharField(max_length=20, null=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    # objects = UserManager()

    def __str__(self):
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
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=(("active", "Active"), ("inactive", "Inactive")))
    
    description = models.TextField()
    
    




    def __str__(self):
        return self.name

#models for wishlist

class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
    
#models for cart

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(null=True, default=0)

   
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, choices=(("active", "Active"), ("inactive", "Inactive")))

    def __str__(self):
        return f"{self.user.username}'s Cart"
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s Cart"
    

#model for user profile
CustomUser = get_user_model()

class ProfileUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)  # New field
    state = models.CharField(max_length=50, blank=True, null=True)  # New field

    def __str__(self):
        return self.user.username
    


# razorpay payment
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)  # New field for order cancellation

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    def cancel(self):
        # Add your cancellation logic here
        self.cancelled = True  # Mark the order as cancelled
        self.save()  # Save the changes to the database
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate item total before saving
        self.item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
    




#nandana new cart
class CartItem1(models.Model):
    cart = models.ForeignKey('Cart1', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Cart1(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem1')

    def __str__(self):
        return f"Cart for {self.user.username}"



        #BRIDAL MAKEUP BOOKING
# BRIDAL MAKEUP BOOKING
class Beautician(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    social_media_links = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    certifications = models.TextField(blank=True)
    availability = models.TextField(blank=True)
    # Add any other relevant fields for your Beautician model

    def __str__(self):
        return self.user.username

class Service(models.Model):
    beautician = models.ForeignKey(Beautician, on_delete=models.CASCADE)
    makeup_type = models.CharField(max_length=255)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)
    portfolio_images = models.ImageField(upload_to='portfolio/', blank=True)
    service_offerings = models.TextField()
    # Add any other relevant fields for your Service model

    def __str__(self):
        return f"{self.beautician.user.username}'s {self.makeup_type} Service"

class Booking(models.Model):
    beautician = models.ForeignKey(Beautician, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending')  # 'pending', 'confirmed', 'completed', etc.
    
    # Add any other relevant fields for your Booking model

    def __str__(self):
        return f"{self.customer.username}'s Booking with {self.beautician.user.username} for {self.service.makeup_type} on {self.date}"


#how to upload videao
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  # Add a description field
    video_file = models.FileField(upload_to='videos/')
    # Add any other fields you need, such as tags, etc.

    def __str__(self):
        return self.title
    
#UPDATIONS

class MakeupType(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category
    
# models.py

class Service1(models.Model):
    beautician = models.ForeignKey(Beautician, on_delete=models.CASCADE)
    makeup_type = models.ForeignKey(MakeupType, on_delete=models.CASCADE)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)
    portfolio_images = models.ImageField(upload_to='portfolio/', blank=True)
    service_offerings = models.TextField()

    def __str__(self):
        return f"{self.beautician.user.username}'s {self.makeup_type.category} Service"


#customised bridal makeup booking
    
class CustomizeBooking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    beautician = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    email = models.EmailField()
    makeup_type = models.CharField(max_length=255, choices=[
        ('Bridal Makeup', 'Bridal Makeup'),
        ('Engagement Makeup', 'Engagement Makeup'),
        ('Reception Makeup', 'Reception Makeup'),
        ('Party Makeup', 'Party Makeup'),
        ('Mehndi Makeup', 'Mehndi Makeup'),
        ('Others', 'Others'),
    ])
    budget = models.CharField(max_length=255)
    event_date = models.DateField()
    specific_requirements = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.name}'s Customized Booking for {self.makeup_type} on {self.event_date}"
   

   #booking payments
    
class BeautyServiceBooking(models.Model):
    # Your existing fields for beauty service booking...
    beautician = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_bookings')
    status = models.CharField(max_length=255)  # You might have a field like this to store the booking status
    requires_payment = models.BooleanField(default=False)  # Add this field to indicate if payment is required for the booking

class BeautyServicePayment(models.Model):
    booking = models.ForeignKey(BeautyServiceBooking, on_delete=models.CASCADE)
    razor_pay_order_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # You can adjust the precision as needed
    is_paid = models.BooleanField(default=False)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    # Other fields specific to payment...

    def __str__(self):
        return f"Payment for Beauty Service Booking: {self.booking.id}"
    

class BookingPayment(models.Model):
    order = models.ForeignKey(CustomizeBooking, on_delete=models.CASCADE)
    razor_pay_order_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust as per your requirements
    is_paid = models.BooleanField(default=False)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    # other fields...

    def __str__(self):
        return f"Payment for Booking: {self.order.user.username}'s Customize Booking"
    

#nandana blog
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def _str_(self):
        return self.title
    



    #models for customer review
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.customer} for {self.product.name}'