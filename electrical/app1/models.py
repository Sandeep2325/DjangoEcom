from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
from django.contrib.postgres.fields import ArrayField
from math import ceil
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Nearest Location")
    city = models.CharField(max_length=150, verbose_name="City")
    state = models.CharField(max_length=150, verbose_name="State")
    pincode=models.BigIntegerField(null=True)
    def __str__(self):
        return self.locality
    class Meta:
        verbose_name_plural = "Address"  
##########################################################################################################################]
class sales(models.Model):
    campaign_name=models.CharField(verbose_name="Campaign name",max_length=200,null=True)
    startdate=models.DateField(verbose_name="Start Date",null=True)
    enddate=models.DateField(verbose_name="End Date",null=True)
    sales_discount=models.DecimalField(max_digits=5, decimal_places=2,null=True,verbose_name='Discount(%)')
    is_active = models.BooleanField(verbose_name="Is Active?",default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date" ,null=True)
    def __str__(self):
        return self.campaign_name
    class Meta:
        verbose_name_plural = "Sales"  

    
####################################################################################################################################
class Category(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        size=900*900
        
        megabyte_limit = 2.0
        if filesize > size:
            raise ValidationError("Max file size is 900*900 or should be less than 2MB")
    #def get_family_tree(self):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    #slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image =models.ImageField(upload_to='category',verbose_name="Category Image",null=True, blank=True,max_length=500)#,validators=[validate_image], null=True,help_text='Maximum file size allowed 900*900 or 2 MB'
    is_active = models.BooleanField(verbose_name="Is Active?",default=True)
    #is_featured = models.BooleanField(verbose_name="Is Featured?",default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
     #################auto resizing function#########################################
    """ def save(self,):
        super().save()   # saving image first

        img = Image.open(self.category_image.path) # Open image using self

        if img.height > 500 or img.width > 500:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(self.category_image.path) """
     ##############################################################################################
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Category"
#########################################################################################################################################        
class Product(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        size=900*900
        megabyte_limit = 2.0
        if filesize > size :
            raise ValidationError("Max file size is 900*900 or should be less than 2mb")
    title = models.CharField(max_length=150, verbose_name="Product Title")
    #slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to='product', verbose_name="Product Image", blank=True, null=True,max_length=500)
    #product_image1 = models.ImageField(upload_to='product', verbose_name="Product Image 1", blank=True, null=True,max_length=500)
    #product_image2 = models.ImageField(upload_to='product', verbose_name="Product Image 2", blank=True, null=True,max_length=500)#,validators=[validate_image],help_text='Maximum file size allowed 900*900 or 2 MB'
    """ images = ArrayField(
        models.ImageField(upload_to='product', blank=True, null=True),
        size=8,
        null=True,
        blank=True 
    )"""
    
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price=models.DecimalField(max_digits=8, decimal_places=2,verbose_name="Offer price",null=True ,blank=True)
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(verbose_name="Is Active?",default=True)
    #is_featured = models.BooleanField(verbose_name="Is Featured?",default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
                            #################auto resizing function#########################################

    """ def save(self):
        super().save()  # saving image first

        img = Image.open(self.product_image.path) # Open image using self

        if img.height >500 or img.width > 500:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(self.product_image.path) """
    
                        ##############################################################################################
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)
    def __str__(self):
        template = '{0.title}'
        return template.format(self)

##################################################################################################################################
class Attributes(models.Model):
    Product=models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name="Product")
    Color=models.CharField(max_length=50,null=True,verbose_name="Color")
    Size=models.CharField(max_length=20,null=True,verbose_name="Size")
    def __str__(self):
        template = 'color: {0.Color}  Size: {0.Size}'
        return template.format(self)
    class Meta:
        verbose_name_plural = "Attributes"
#################################################################################################################################
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    attributes=models.ForeignKey(Attributes,verbose_name=" Product Attributes",on_delete=models.CASCADE,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date" ,null=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )
    class Meta:
        verbose_name_plural = "Order"
###############################################################################################################################


