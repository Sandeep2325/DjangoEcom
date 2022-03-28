from ctypes import BigEndianStructure
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from datetime import datetime
from django.db.models.signals import pre_save
from asyncio.windows_events import NULL
from enum import unique
from pickle import FALSE

from re import VERBOSE
from tabnanny import verbose
from tkinter import CASCADE
from django.db.models import Q

from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from PIL import Image

from math import ceil
from ckeditor.fields import RichTextField
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, BaseUserManager

from datetime import date
from django.db.models import Avg

from embed_video.fields import EmbedVideoField
from django.db.models import Avg, Count


class User(AbstractUser):
    username = models.CharField(
        max_length=50, blank=False, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name=models.CharField(max_length=50,blank=False,null=True)
    last_name=models.CharField(max_length=50,blank=False,null=True)
    #native_name = models.CharField(max_length = 5)
    phone_no = models.CharField(max_length=10, null=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_no']

    def __str__(self):
        return "{}".format(str(self.username))

class my_account(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name=models.CharField(max_length=50,null=True,verbose_name="First Name")
    last_name=models.CharField(max_length=50,null=True,verbose_name="last Name")
    phone_number=models.BigIntegerField(null=True,verbose_name="Phone number")
    email=models.EmailField(max_length=255,null=True,verbose_name="Email")
    address=models.TextField(null=True,verbose_name="Address")
    city=models.CharField(max_length=100,null=True,verbose_name="City")
    state=models.CharField(max_length=50,null=True,verbose_name="State")
    postal_address=models.TextField(null=True,verbose_name="Postal address")
    def __str__(self):
        return self.first_name    

""" class AccountManager(BaseUserManager):
    def create_superuser(self,email,first_name,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('is_staff is set to False')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser is set to False')
        return self.create_user(email,first_name,password,**other_fields)

    def create_user(self,email,first_name,password, **other_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))
     
        email=self.normalize_email(email)
        user=self.model(email=email,first_name=first_name,**other_fields)
        user.is_active=True
        user.set_password(password)
        user.save(using=self._db)
        return user """

""" class User(AbstractUser):
   username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
   email = models.EmailField(('email address'), unique = True)
   native_name = models.CharField(max_length = 5)
   phone_no = models.CharField(max_length = 10)
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
   def __str__(self):
       return "{}".format(self.email) """

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    door_number = models.BigIntegerField(null=True,)
    street = models.CharField(max_length=200, null=True,)
    city = models.CharField(max_length=200, null=True,)
    state = models.CharField(max_length=200, null=True,)
    country = models.CharField(max_length=200, null=True,)
    pincode = models.IntegerField(null=True,)
    phone_no = models.BigIntegerField(null=True, verbose_name="Phone")
    alternate_phone_no = models.BigIntegerField(
        null=True, verbose_name="Alternate Phone", blank=True)

    def __str__(self):
        template = '{0.door_number} {0.street} {0.city} {0.state} {0.country} '
        return template.format(self)

    class Meta:
        verbose_name_plural = "Customer Address"

class sales(models.Model):
    campaign_name = models.CharField(
        verbose_name="Campaign name", max_length=200, null=True)
    startdate = models.DateField(verbose_name="Start Date", null=True)
    enddate = models.DateField(verbose_name="End Date", null=True)
    sales_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Discount(%)', validators=[
        MinValueValidator(1), MaxValueValidator(99)
    ])
    is_active = models.BooleanField(verbose_name="Is Active?", default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", null=True)

    def __str__(self):
        return self.campaign_name

    class Meta:
        verbose_name_plural = "Sales/Discount"

class Category(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        size = 900*900
        megabyte_limit = 2.0
        if filesize > size:
            raise ValidationError(
                "Max file size is 900*900 or should be less than 2MB")
   
    brands = models.CharField(max_length=50, verbose_name="Brands")

    description = models.TextField(
        blank=True, verbose_name="Category Description")
    category_image = models.ImageField(
        upload_to='category', verbose_name="Brand Thumbnail", null=True, blank=True, max_length=500)
    is_active = models.BooleanField(verbose_name="Is Active?", default=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date")

        ##auto resizing##
    """ def save(self,):
        super().save()   # saving image first
        img = Image.open(self.category_image.path) # Open image using self
        if img.height > 500 or img.width > 500:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(self.category_image.path) """

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.brands

    class Meta:
        verbose_name_plural = " Category"

class Brand(models.Model):
    brand_name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='brand', blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_name

class image(models.Model):
    image = models.ImageField(upload_to="images")
    """ def __str__(self):
        return self.image """

    def __str__(self):
        return str(self.image)
    """ def save(self,):
        super().save()   # saving image first

        img = Image.open(self.image.path) # Open image using self

        if img.height > 500 or img.width > 500:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(self.image.path) """

class Product(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        size = 900*900
        megabyte_limit = 2.0
        if filesize > size:
            raise ValidationError(
                "Max file size is 900*900 or should be less than 2mb")
    title = models.CharField(max_length=150, verbose_name="Product Title")
   
    sku = models.CharField(max_length=255, unique=True,
                           verbose_name="Unique Product ID (SKU)")
    short_description = RichTextField(verbose_name="Short Description")
    detail_description = models.TextField(
        blank=True, null=True, verbose_name="Detail Description")
    image = models.ManyToManyField(image, blank=True)
    product_image = models.ImageField(
        upload_to='product', verbose_name="Product Thumbnail", blank=True, null=True, max_length=500)
    
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Price(₹)')
    discounted_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Offer Price(₹)", null=True, blank=True)
    category = models.ForeignKey(
        Category, verbose_name="Product category", on_delete=models.SET_NULL, null=True)

    brand=models.ForeignKey(Brand,verbose_name="Product Brand",on_delete=models.SET_NULL,null=True)
    is_active = models.BooleanField(verbose_name="Is Active?", default=True)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date")

    """ def save(self):
        super().save()  # saving image first

        img = Image.open(self.product_image.path) # Open image using self

        if img.height >500 or img.width > 500:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(self.product_image.path)"""

    @property
    def average_rating(self):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=self)):

            review = Rating.objects.filter(Q(Status="Approved") & Q(
                product=self)).aggregate(average=Avg('Rating'))
            avg = 0
            if review["average"] is not None:
                avg = float(review["average"])
            # return avg
            if avg != 0:
                return "%.1f" % float(avg)
            else:
                return format_html("<p class=text-danger>No ratings!</p>")
        else:
            return format_html("<p class=text-danger>No ratings!</p>")
    # average_review.short_description="Average Rating"

    @property
    def count_review(self):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=self)):
            reviews = Rating.objects.filter(Q(Status="Approved") & Q(
                product=self)).aggregate(count=Count('id'))
            cnt = 0
            if reviews["count"] is not None:
                cnt = int(reviews["count"])
            return cnt
        else:
            return format_html("<p class=text-danger>No ratings!</p>")

    @property
    def reviews(self):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=self)):
            reviews = Rating.objects.filter(
                Q(Status="Approved") & Q(product=self)).values_list("Reviews")
            for review in reviews:
                return review
        else:
            return format_html("<p class=text-danger>No ratings!</p>")

    class Meta:
        # def countt(self):
        verbose_name_plural = '  Products'
        ordering = ('-created_at',)

    def __str__(self):
        template = '{0.title}/{0.category}/{0.brand}'
        return template.format(self)
##
class Attributes(models.Model):
    Product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Product")
    Color = models.CharField(max_length=50, null=True, verbose_name="Color")
    Size = models.CharField(max_length=20, null=True, verbose_name="Size")
    def __str__(self):
        template = 'color: {0.Color}  Size: {0.Size}'
        return template.format(self)
    class Meta:
        verbose_name_plural = "Attributes"

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,verbose_name="User")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,verbose_name="Product")
    attributes = models.ForeignKey(
        Attributes, verbose_name=" Product Attributes", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity",null=True)
    date = models.DateTimeField(auto_now_add=True,verbose_name="Date",null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", null=True)
    coupon=models.CharField(max_length=50,null=True,blank=True)
    coupons=models.ForeignKey("Coupon",on_delete=models.CASCADE,null=True)

    @property
    def price(self):
        try: 
            return self.product.price
        except:
            pass
    @property
    def offer_price(self):
        try:
            return self.product.discounted_price
        except:
            pass
    @property
    def Total_amount_(self): #not in use
        try:
            coupons_list=[]
            coupons_amount=[]
            if self.product.discounted_price is None:
                try:  
                    if self.coupon==coupon_:
                        coupon_price=a.coupon_discount
                        total_amount=(self.quantity*self.product.price)-(self.quantity*int(coupon_price))
                    else:
                        total_amount=(self.quantity*self.product.price)
                except:
                    if self.coupon==coupon_:
                        coupon_price=a.coupon_discount
                        total_amount=(1*self.product.price)-(self.quantity*int(coupon_price))
                    else:
                        total_amount=(1*self.product.price)
                return total_amount
            else:
                for a in Coupon.objects.all():
                        coupon_=a.coupon
                if self.coupon==coupon_:
                    coupon_price=a.coupon_discount
                    total_amount=(self.quantity*self.product.discounted_price)-(self.quantity*int(coupon_price))
                else:
                    total_amount=(self.quantity*self.product.discounted_price)
                return total_amount
        except:
            pass
        
    @property
    def Total_amount(self):
        try:
            coupons_list=[]
            coupons_amount=[]
            if self.product.discounted_price is None:
                # print("222222222222222222222222222",self.product.price)
                for a in Coupon.objects.all():
                        coupon_=a.coupon
                        coupons_list.append(coupon_)
                        coupons_amount.append(a.coupon_discount)
                print(coupons_amount)
                print(coupons_list)
                try:  
                    for i in range(len(coupons_list)): 
                        if self.coupon==coupons_list[i]:
                            coupon_price=coupons_amount[i]
                            total_amount=(self.quantity*self.product.price)-(self.quantity*int(coupon_price))
                    return total_amount
                             
                except:
                    for i in range(len(coupons_list)): 
                        if self.coupon==coupons_list[i]:
                            coupon_price=coupons_amount[i]
                            total_amount=(1*self.product.price)-(self.quantity*int(coupon_price))
                    return total_amount
            else:
                for i in range(len(coupons_list)): 
                        if self.coupon==coupons_list[i]:
                            coupon_price=coupons_amount[i]
                            total_amount=(self.quantity*self.product.discounted_price)-(self.quantity*int(coupon_price))
                return total_amount
        except:
            pass
    @property
    def amount_saved(self):
        try:
            for a in Coupon.objects.all():
                coupon_=a.coupon
            if self.product.discounted_price is not None:
                if self.coupon==coupon_:
                    coupon_price=a.coupon_discount
                    return (self.product.price*self.quantity)-(self.product.discounted_price                                                                                                                                                                                                                                                             *self.quantity)
            else:
                pass
        except:
            pass
       
    class Meta:
        verbose_name_plural = "Carts"
    def __str__(self):
        return str(self.product)

class checkout(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    cart=models.ManyToManyField(Cart)
    Shipping_address=models.ForeignKey(Address,on_delete=models.CASCADE,verbose_name="Shipping Address")
    Coupon=models.CharField(max_length=100,null=True,blank=True)
    def products(self):
        return ",".join([str(p) for p in self.cart.all()])
    def No_of_items_to_checkout(self):
        return self.cart.all().count()

    def __str__(self):
        return str(self.cart.first())
    class Meta:
        verbose_name_plural = "Checkouts"

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)
class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    checkout_product=models.ForeignKey(checkout,on_delete=models.CASCADE,verbose_name="Checked out product")
    ordered_date = models.DateTimeField(
        auto_now_add=True, verbose_name="ordered Date", null=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending")
    class Meta:
        verbose_name_plural = "Orders"

class Coupon(models.Model):
    coupon = models.CharField(
        verbose_name="Coupon_code", max_length=200, null=True, unique=True)
    startdate = models.DateField(verbose_name="Start Date", null=True)
    enddate = models.DateField(verbose_name="End Date", null=True)
    coupon_discount = models.IntegerField(
        null=True, verbose_name="Discount(₹)")
    #is_active = models.BooleanField(verbose_name="Is Active?",default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", null=True)
    def __str__(self):
        return self.coupon
    class Meta:
        verbose_name_plural = "Coupons"
####
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User",
                             on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, verbose_name="Shipping Address", on_delete=models.CASCADE, default=NULL)
    product = models.ForeignKey(
        Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Price(₹)")
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    attributes = models.ForeignKey(
        Attributes, verbose_name=" Product Attributes", on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(
        auto_now_add=True, verbose_name="ordered Date", null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", null=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
    )
    @property
    def pricee(self,):
        return self.product.price
    # pricee.short_description="Price"
    @property
    def offer_price(self):
        return self.product.discounted_price
    @property
    def Total_amount(self):
        if self.product.discounted_price is None:
            # print("222222222222222222222222222",self.product.price)
            try:
                total_amount=self.quantity*self.product.price
            except:
                total_amount=1*self.product.price
            return total_amount
        else:
            total_amount=self.quantity*self.product.discounted_price
            return total_amount
    # def save(self, *args, **kwargs):
    #     try:
    #         if self.product.discounted_price is None:
    #             self.price = self.product.price*self.quantity
    #             if self.coupon:
    #                 self.price = self.price-self.coupon.coupon_discount
    #                 return super(Order, self).save(*args, **kwargs)
    #             return super(Order, self).save(*args, **kwargs)

    #         elif self.product.discounted_price is not None:
    #             self.price = self.product.discounted_price*self.quantity
    #             if self.coupon:
    #                 self.price = self.price-self.coupon.coupon_discount
    #                 return super(Order, self).save(*args, **kwargs)
    #             return super(Order, self).save(*args, **kwargs)
    #         else:
    #             return messages.warning('Something went wrong!')
    #     except:
    #         pass

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = "Order"

##Rating Models##
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Rejected', 'Rejected'),
    ('Approved', 'Approved'),
)

class Rating(models.Model):
    # Product = models.ForeignKey(to, on_delete)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, verbose_name="Product",
                                related_name='ratings', on_delete=models.CASCADE, null=True)
    Reviews = RichTextField(null=True, blank=True)
    Rating = models.DecimalField(default=0.0, max_digits=5, decimal_places=1, validators=[
        MinValueValidator(1), MaxValueValidator(5)
    ], null=True)
    Status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=8,
        default="Pending", null=True
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", null=True)

    def __str__(self):
        try:
            return self.product.title
        except:
            return str(None)

    @property
    def status_(self):
        # if Rating.objects.filter(Status=None):
        #     messages.warning
        if Rating.objects.filter(Q(Status="Approved") & Q(product=self.product) & Q(Reviews=self.Reviews) & Q(user=self.user) & Q(Rating=self.Rating)):
            return format_html('<p class="text-success fa fa-check" aria-hidden="true"><span class="ml-2">Approved</span></p>')
        elif Rating.objects.filter(Q(Status="Rejected") & Q(product=self.product) & Q(Reviews=self.Reviews) & Q(user=self.user) & Q(Rating=self.Rating)):
            return format_html('<p class="text-danger fa fa-ban" aria-hidden="true"><span class="ml-2">Rejected</span></p>')
        elif Rating.objects.filter(Q(Status="Pending") & Q(product=self.product) & Q(Reviews=self.Reviews) & Q(user=self.user) & Q(Rating=self.Rating)):
            return format_html('<p class="text-primary fa fa-clock" aria-hidden="true"><span class="ml-2">Pending</span></p>')

class Blog(models.Model):
    # def validate_image(fieldfile_obj):
    #     filesize = fieldfile_obj.file.size
    #     size=900*900

    #     megabyte_limit = 2.0
    #     if filesize > size:
    #         raise ValidationError("Max file size is 900*900 or should be less than 2MB")
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=100, null=True)
    description = models.TextField()
    url = EmbedVideoField(max_length=200, null=True, blank=True)
    images = models.ImageField(upload_to="blog", null=True)
    image = models.ManyToManyField(image, blank=True)
    #category=models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    uploaded_date = models.DateField(auto_now_add=True)

    ###auto resizing function###
    def save(self):
        super().save()  # saving image first
        try:
            img = Image.open(self.image.path)  # Open image using self
            if img.height > 700 or img.width > 700:
                new_img = (500, 500)
                img.thumbnail(new_img)
                img.save(self.image.path)
        except:
            pass

    def __unicode__(self):
        return self.url

    def __str__(self):
        return self.title

##faq##
STATUS_CHOICES = [
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]
class FAQ(models.Model):
    Question = models.CharField(max_length=100, null=True,)
    Answer = RichTextField(max_length=300, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Ordered Date", null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="d")

    class Meta:
        verbose_name_plural = "FAQs"

    def __str__(self):
        return str(self.Question,)

class customer_message(models.Model):
    first_name = models.CharField(
        max_length=50, null=True, verbose_name="First Name", blank=True)
    last_name = models.CharField(
        max_length=50, null=True, verbose_name="Last Name", blank=True)
    #Name=models.CharField(max_length=50, null=True,)
    Email = models.EmailField(max_length=50, null=True,)
    Phone = models.BigIntegerField(null=True,)
    Message = models.TextField(max_length=200, null=True,)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", null=True)

    def __str__(self):
        return str(self.first_name,)

    class Meta:
        verbose_name_plural = "Customer messages"


class Banner(models.Model):

    title = models.CharField(max_length=50)
    image = models.FileField(upload_to="Banner", blank=True, null=True,)
    uploaded_date = models.DateField(auto_now_add=True)

    def save(self):
        super().save()  # saving image first
        try:
            img = Image.open(self.image.path)  # Open image using self

            if img.height > 700 or img.width > 700:
                new_img = (500, 500)
                img.thumbnail(new_img)
                img.save(self.image.path)
        except:
            pass

    def __str__(self):
        return str(self.title,)

STATUS_CHOICES = [
    ('d', 'Draft'),
    ('s', 'sent'),
]
class MailText(models.Model):
    users = models.ManyToManyField(User)
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True)
    send_it = models.BooleanField(default=False)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="d")
    
    def save(self,*args, **kwargs):

        savee = super(MailText, self).save(*args, **kwargs)

        if self.send_it == True:
 
            user_list = []
            print(self.users.all())
            for u in self.users.all():
                print(u.email)
                user_list.append(u.email)
            # print(user_list)
            send_mail(str(self.subject),
                      strip_tags(str(self.message)),
                      'gowdasandeep8105@gmail.com',
                      user_list,
                      fail_silently=False)
            
        self.status="s"    
        return savee

            
    class Meta:
        verbose_name = "Email marketing"
        verbose_name_plural = "Email marketing"

    def __str__(self):
        return str(self.subject)

