from ctypes import BigEndianStructure
from itertools import product
from logging import exception
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from datetime import datetime
from django.db.models.signals import pre_save
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from PIL import Image
from django.conf import settings
from math import ceil
from ckeditor.fields import RichTextField
from django.http import Http404, HttpResponse
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import date
from django.db.models import Avg
# from embed_video.fields import EmbedVideoField
from django.db.models import Avg, Count
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files import File
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
class User(AbstractUser,PermissionsMixin):
    username = models.CharField(
        max_length=50, blank=False, null=True,verbose_name="Full name")
    email = models.EmailField(_('email address'), unique=True)
    # first_name=models.CharField(max_length=50,blank=False,null=True)
    # last_name=models.CharField(max_length=50,blank=False,null=True)
    #native_name = models.CharField(max_length = 5)
    is_confirmed = models.BooleanField(default=False) #default is True when not using otp email verification
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=10, null=True, unique=True)
    otp = models.IntegerField(default=False)
    is_used = models.BooleanField(default=False)
    # dummy=models.CharField(max_length=200,null=True,blank=True)
    # last_login=models.CharField(max_length=255,blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_no']
     
    def __str__(self):
        return "{}".format(str(self.username))
class userphoto(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    photo=models.ImageField(upload_to='profile',max_length=500, verbose_name="Profle photo", null=True, blank=True,default="https://icon2.cleanpng.com/20180319/xrq/kisspng-neck-sitting-line-male-5ab05067ad9d95.1710165615215043597111.jpg")
    
class my_account(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # photo=models.ImageField(upload_to='profile', verbose_name="Profle photo", null=True, blank=True, max_length=500)
    first_name=models.CharField(max_length=50,null=True,verbose_name="First Name",default="User")
    last_name=models.CharField(max_length=50,null=True,verbose_name="last Name")
    phone_number=models.BigIntegerField(null=True,verbose_name="Phone number")
    email=models.EmailField(max_length=255,null=True,verbose_name="Email")
    address=models.TextField(null=True,verbose_name="Address")
    city=models.CharField(max_length=100,null=True,verbose_name="City")
    state=models.CharField(max_length=50,null=True,verbose_name="State")
    is_confirmed = models.BooleanField(default=False)
    otp = models.IntegerField(default=False,null=True,blank=True)
    postal_pin=models.BigIntegerField(null=True,verbose_name="Postal address")
    
    # def __str__(self):
    #     return self.first_name    

    def save(self,*args, **kwargs):
        super().save()  # saving image first
        try:
            img = Image.open(self.photo.path)  # Open image using self
            if img.height > 700 or img.width > 700:
                new_img = (500, 500)
                img.thumbnail(new_img)
                img.save(self.photo.path)
        except:
            pass
        
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fullname=models.CharField(max_length=150,null=True,blank=True,verbose_name="Full Name")
    phone=models.BigIntegerField(null=True,blank=True,verbose_name="Phone Number")
    locality=models.TextField(null=True,blank=True,verbose_name="locality")
    state=models.CharField(max_length=100,null=True,blank=True,verbose_name="State")
    city=models.CharField(max_length=100,null=True,blank=True,verbose_name="City")
    pincode=models.BigIntegerField(null=True,blank=True,verbose_name="Pin code")
    address=models.TextField(null=True,blank=True,verbose_name="Address")
    home=models.BooleanField(default=False,verbose_name="Home")
    work=models.BooleanField(default=False,verbose_name="Work")
    default=models.BooleanField(default=False,verbose_name="default")

    def __str__(self):
        template = '{0.fullname} {0.phone} {0.locality} {0.city} {0.state} '
        return template.format(self)

    class Meta:
        verbose_name_plural = "Customer Address"
class notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    message=models.TextField(null=True,blank=True)
    # offers=models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", null=True)
    class Meta:
        verbose_name_plural = "Notification"
 
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
    def save(self, *args, **kwargs):
        
        a="{} sale is ON buy any product get {}% discount".format(self.campaign_name,self.sales_discount)
        notification.objects.create(message=a)
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return self.campaign_name

    class Meta:
        verbose_name_plural = "Sales/Discount"

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
##
class Category(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        size = 900*900
        megabyte_limit = 2.0
        if filesize > size:
            raise ValidationError(
                "Max file size is 900*900 or should be less than 2MB")
   
    category = models.CharField(max_length=50, verbose_name="Category",null=True)

    description = models.TextField(
        blank=True, verbose_name="Category Description",null=True)
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
        return self.category

    class Meta:
        verbose_name_plural = " Category"
        
class subcategory(models.Model):
    sub_category=models.CharField(max_length=255,null=True,blank=True)
    category=models.ForeignKey(Category,blank=True,on_delete=models.CASCADE,null=True,related_name="subcategory")
    
    
    def __str__(self):
        template = '{0.sub_category}'
        return template.format(self)
    
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
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(
        blank=True, null=True, verbose_name="Detail Description")
    specification=models.TextField(verbose_name="Specification",null=True,blank=True,)
    image = models.ManyToManyField(image, blank=True)
    product_image = models.ImageField(
        upload_to='product', verbose_name="Product Thumbnail", blank=True, null=True, max_length=500)
    
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Price(₹)')
    discounted_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Offer Price(₹)", null=True, blank=True)
    category = models.ForeignKey(
        Category, verbose_name="Product category", on_delete=models.SET_NULL, null=True,blank=True)
    subcategory=models.ForeignKey(
        subcategory, verbose_name="sub category", on_delete=models.SET_NULL, null=True,blank=True)
    brand=models.ForeignKey(Brand,verbose_name="Product Brand",on_delete=models.SET_NULL,null=True)
    attributes = models.ForeignKey(
        "Attributes", verbose_name=" Product Attributes", on_delete=models.SET_NULL, null=True, blank=True)
    available_stocks=models.CharField(max_length=10,null=True,blank=True)
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
        verbose_name_plural = '  Products'
        ordering = ('-created_at',)

    def __str__(self):
        template = '{0.title}/{0.category}/{0.brand}'
        return template.format(self)

##
class Attributes(models.Model):
    Color = models.CharField(max_length=50, null=True, verbose_name="Color")
    def __str__(self):
        template = 'color: {0.Color}'
        return template.format(self)
    class Meta:
        verbose_name_plural = "Attributes"

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,verbose_name="User")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,verbose_name="Product")
    attributes = models.ForeignKey(
        Attributes, verbose_name=" Product Attributes", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity",default=1)
    date = models.DateTimeField(auto_now_add=True,verbose_name="Date",null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", null=True)
    # p_idd=models.CharField(null=True,blank=True,max_length=5)
    p_id=models.CharField(null=True,blank=True,max_length=5)
    is_active=models.BooleanField(default=True)
    # coupon=models.CharField(max_length=50,null=True,blank=True)
    # coupons=models.ForeignKey("Coupon",on_delete=models.CASCADE,null=True)

    @property
    def price(self):
        try: 
            return self.product.price*self.quantity
        except:
            pass
    @property
    def offer_price(self):
        try:
            return self.product.discounted_price
        except:
            pass
    @property
    def Total_amount(self): 
        try:
            if self.product.discounted_price is None:
                try:  
                    total_amount=(self.quantity*self.product.price)
                except:
                    total_amount=(1*self.product.price)
                return total_amount
            else:
                total_amount=(self.quantity*self.product.discounted_price)
                return total_amount
        except:
            pass
    @property
    def Total_amount_(self): #not in use
        try:
            if self.coupon !=None:
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
                            else:
                                total_amount=(self.quantity*self.product.price)
                        return total_amount
                    except:
                        for i in range(len(coupons_list)): 
                            if self.coupon==coupons_list[i]:
                                coupon_price=coupons_amount[i]
                                total_amount=(1*self.product.price)-(self.quantity*int(coupon_price))
                            else:
                                total_amount=(1*self.product.price)
                        return total_amount
                else:
                    for a in Coupon.objects.all():
                            coupon_=a.coupon
                            coupons_list.append(coupon_)
                            coupons_amount.append(a.coupon_discount)
                    print(coupons_amount)
                    print(coupons_list)
                    
                    for i in range(len(coupons_list)): 
                            if self.coupon==coupons_list[i]:
                                coupon_price=coupons_amount[i]
                                total_amount=(self.quantity*self.product.discounted_price)-(self.quantity*int(coupon_price))
                            else:
                                total_amount=(self.quantity*self.product.discounted_price)
                    return total_amount
        except:
            if self.product.discounted_price is None:
                try:
                    total_amount=(self.quantity*self.product.price)
                except:
                    total_amount=(1*self.product.price)
                return total_amount
            else:
                total_amount=(self.quantity*self.product.discounted_price)
                return total_amount
    @property
    def amount_saved(self):
        try:
            return self.price-self.Total_amount
        except:
            pass
        
    class Meta:
        verbose_name_plural = "Carts"
    def __str__(self):
        return str(self.product)

class Coupon(models.Model):
    coupon = models.CharField(
        verbose_name="Coupon_code", max_length=200, null=True, unique=True)
    startdate = models.DateField(verbose_name="Start Date", null=True)
    enddate = models.DateField(verbose_name="End Date", null=True)
    coupon_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Discount(%)', validators=[
        MinValueValidator(1), MaxValueValidator(99)])
    #is_active = models.BooleanField(verbose_name="Is Active?",default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", null=True)
    def save(self, *args, **kwargs):
        coupons="use {} coupon to get {}% discount".format(self.coupon,self.coupon_discount)
        notification.objects.create(message=coupons)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.coupon
    class Meta:
        verbose_name_plural = "Coupons"

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
    title = models.TextField(null=True, blank=True)
    # author = models.CharField(max_length=100, null=True)
    # description = models.TextField()
    detail_description=models.TextField(null=True, blank=True)
    # url = EmbedVideoField(max_length=200, null=True, blank=True)
    # images = models.ImageField(upload_to="blog", null=True)
    image = models.ManyToManyField(image, blank=True)
    #category=models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    uploaded_date = models.DateField(auto_now_add=True)
    location=models.CharField(max_length=50,null=True,blank=True)
    facebook=models.URLField(null=True)
    instagram=models.URLField(null=True)
    twitter=models.URLField(null=True)
    linkdin=models.URLField(null=True)
    ###auto resizing function###
    # def save(self):
    #     super().save()  # saving image first
    #     try:
    #         img = Image.open(self.image.path)  # Open image using self
    #         if img.height > 700 or img.width > 700:
    #             new_img = (500, 500)
    #             img.thumbnail(new_img)
    #             img.save(self.image.path)
    #     except:
    #         pass

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
    category=models.ForeignKey(Category,null=True,blank=True,on_delete=models.CASCADE)
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
        verbose_name_plural = "Customer msgs/contact us"


class Banner(models.Model):
    title = models.CharField(max_length=50)
    image = models.FileField(upload_to="Banner", blank=True, null=True,)
    is_active = models.BooleanField(default=True)
    uploaded_date = models.DateField(auto_now_add=True)

    # def save(self):
    #     super().save()  # saving image first
    #     try:
    #         img = Image.open(self.image.path)  # Open image using self

    #         if img.height > 700 or img.width > 700:
    #             new_img = (500, 500)
    #             img.thumbnail(new_img)
    #             img.save(self.image.path)
    #     except:
    #         pass
    def save(self):
        # Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((1400, 400))

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=90)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(Banner, self).save()
    
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
                      settings.EMAIL_HOST_USER,
                      user_list,
                      fail_silently=False)
            
        self.status="s"    
        return savee
    class Meta:
        verbose_name = "Email marketing"
        verbose_name_plural = "Email marketing"

    def __str__(self):
        return str(self.subject)

class latest_product(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="created date", null=True)
    class Meta:
        verbose_name_plural = "Latest Products"
        
class most_selled_products(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    # orders=models.ForeignKey(Orders,on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="created date", null=True)
    # @property
    # def sellcount(self):
    #     try:
    #         count=Orders.objects.filter(id=self.orders.id).count()
    #         return count
    #     except:
    #         pass

    class Meta:
        verbose_name_plural = "Most selled products"
class newsletter(models.Model):
    Email=models.EmailField(max_length=255,null=True,blank=True)
    subscribed_date = models.DateTimeField(
        auto_now_add=True, verbose_name="created date", null=True)
    
    class Meta:
        verbose_name_plural="News letter"
        
class enquiryform(models.Model):
    name = models.CharField(
        max_length=50, null=True, verbose_name="Full Name", blank=True)
    #Name=models.CharField(max_length=50, null=True,)
    Email = models.EmailField(max_length=50, null=True,)
    Phone = models.BigIntegerField(null=True,)
    Message = models.TextField(max_length=200, null=True,)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", null=True)
    class Meta:
        verbose_name_plural="FAQ Enquiry"
class socialmedialinks(models.Model):
    social_media=models.CharField(max_length=100,null=True,blank=True,verbose_name="social media")
    links=models.URLField(null=True,blank=True,verbose_name="link")
    def __str__(self):
        return self.social_media
    class Meta:
        verbose_name_plural="Social media links"

STATUS_CHOICES = (
    ('orderpending', 'order Pending'),
    ('Ordered', 'Ordered'),
    ('Packed', 'Packed'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)
class cart_order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date=models.DateField(auto_now_add=True,verbose_name="Ordered Date",null=True)
    product_count=models.CharField(max_length=10,null=True,blank=True)
    total_price=models.IntegerField(null=True,blank=True)
    product=models.ManyToManyField(Product)
    coupon=models.CharField(max_length=10,null=True,blank=True)
    shipping_address=models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
    is_paid=models.BooleanField(default=False)
    order_payment_id = models.CharField(max_length=100,null=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="orderpending")
    def __str__(self):
        return str(self.user.username)
    
    def save(self, *args, **kwargs):
        print(self.user,self.order_payment_id,self.status)
        message="Hello {} your Order({}) is {}".format(str(self.user.username),self.order_payment_id,self.status)
        notification.objects.create(user=self.user,message=message)
        return super().save(*args, **kwargs)
    
class payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order_id=models.CharField(max_length=1000,null=True,blank=True)
    payment_id=models.CharField(max_length=1000,null=True,blank=True)
    signature_id=models.CharField(max_length=1000,null=True,blank=True)
    amount=models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return str(self.order_id)
class cart2(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.CharField(max_length=20,null=True,blank=True)
    price=models.CharField(max_length=1000,null=True,blank=True)
    order_id=models.CharField(max_length=100,null=True,blank=True)
    is_paid=models.BooleanField(default=False)
class refund(models.Model):
    refundId=models.CharField(max_length=100,null=True,blank=True)
    receiptId=models.CharField(max_length=100,null=True,blank=True)
    entity=models.CharField(max_length=100,null=True,blank=True)
    amount=models.CharField(max_length=100,null=True,blank=True)
    currency=models.CharField(max_length=100,null=True,blank=True)
    payment_id=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)
    speed_processed=models.CharField(max_length=100,null=True,blank=True)
    speed_requested=models.CharField(max_length=100,null=True,blank=True)
class redeemedcoupons(models.Model):
    coupon=models.CharField(max_length=100,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True) 
   
