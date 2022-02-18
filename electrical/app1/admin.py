from asyncio.windows_events import NULL
from contextlib import nullcontext
from dataclasses import field
from logging import exception
from msilib.schema import ActionText
from tkinter import ACTIVE, EXCEPTION
from turtle import update
from unicodedata import category
from django.contrib import admin
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from pyparsing import nullDebugAction
from . models import *
from django.urls import path
from . forms import *
from django.shortcuts import redirect, render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View
from django.utils.html import format_html
from xhtml2pdf import pisa
from django import forms
from django.core.files.images import get_image_dimensions
from math import ceil
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.postgres.forms import SplitArrayField
####################################################################################################################################
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')
    save_on_top = True
    class Meta:
        verbose_name_plural = "Address"
#####################################################################################################
# from django.contrib.postgres.forms import SplitArrayField
""" class AlbumForm(forms.ModelForm):
    pictures = SplitArrayField(forms.ImageField(), size=4)
    class Meta:
        model = Category
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    form = AlbumForm """
##################################################################################################################################
class CategoryAdmin(admin.ModelAdmin):
    try:
        def image_tag(self, obj):
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.category_image.url,"100","100"))
        image_tag.short_description = 'Image'
        image_tag.allow_tags = True
        list_display = ['id','title','image_tag','is_active','updated_at']
        #list_editable = ('slug', )
        list_editable=('is_active',)
        list_filter = ('title','is_active','updated_at')
        list_per_page = 10
        search_fields = ('title', 'description','is_active','updated_at')
        save_on_top = True
        #prepopulated_fields = {"slug": ("title", )}
        def get_urls(self):
            urls = super().get_urls()
            new_urls = [path('upload-csv/', self.upload_csv),]
            return new_urls + urls
        def upload_csv(self, request):
            try:
                if request.method == "POST":
                    csv_file = request.FILES["csv_upload"]   
                    if not csv_file.name.endswith('.csv'):
                        messages.warning(request, 'The wrong file type was uploaded')
                        return HttpResponseRedirect(request.path_info) 
                    file_data = csv_file.read().decode("utf-8")
                    csv_data = file_data.split("\r\n")
                    for x in csv_data:
                        fields = x.split(",")
                        try:
                            created = Category.objects.create(
                            title=fields[0],
                            description=fields[1],
                            category_image=fields[2],)
                            created.save()
                        except IndexError:
                            pass
                        except (ValidationError,IntegrityError):
                            form = CsvImportForm()
                            data = {"form": form}
                            message=messages.warning(request,'Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
                            return render(request, "admin/csv_upload.html", data)
                    url = reverse('admin:index')
                    return HttpResponseRedirect(url)
                form = CsvImportForm()
                data = {"form": form} 
                return render(request, "admin/csv_upload.html", data)  
            except TypeError:
                return HttpResponse("Something went wrong")    
    except exception:
        raise Http404  
###################################################################################################################################### 
class ProductAdmin(admin.ModelAdmin):
    try:
        
        def image_tag(self, obj):
                return format_html('<img src="{}"width="{}" height="{}"/>'.format(obj.product_image.url,"100","100"))

        image_tag.short_description = 'Image'
        image_tag.allow_tags = True
        """ def image_tag1(self, obj):
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.product_image1.url,"100","100"))

        image_tag1.short_description = 'Image1'
        image_tag1.allow_tags = True
        def image_tag2(self, obj):
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.product_image2.url,"100","100"))

        image_tag2.short_description = 'Image2'
        image_tag2.allow_tags = True """
        list_display = ['id','title','category','image_tag','price','discounted_price','is_active','updated_at',]#,'is_active','is_featured'
        list_editable = ('category','is_active',)
        list_filter = ('category','is_active','updated_at')
        list_per_page = 20
        #inlines = [ImagemInline]
        search_fields = ('title', 'short_description','is_active','updated_at')
        save_on_top = True
        actions=['sales_discount','delete_offers']
        #discount_.short_description=''
        #prepopulated_fields = {"slug": ("title", )}
        def delete_offers(self,request,queryset):
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("update app1_product set discounted_price =NULL")
            """ for product in queryset:
                product.discounted_price=NULL
                product.save(update_fields=['discounted_price']) """

        def sales_discount(self,request,queryset):
            Sales=sales.objects.all()
            for sale in Sales:
                discount = sale.sales_discount # percentage
                print("##################################",discount)
                if sale.is_active==True:
                    for product in queryset:
                        print("***************************",discount)
                        multiplier = discount / 100  # discount / 100 in python 3
                        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",multiplier)
                        old_price = product.price
                        new_price = ceil(old_price - (old_price * multiplier))
                        product.discounted_price = new_price
                        product.save(update_fields=['discounted_price'])
                #sales_discount.short_description = 'Apply sales discount'  
        def get_urls(self):
            urls = super().get_urls()
            new_urls = [path('upload-csv/', self.upload_csv),]
            return new_urls + urls
        def upload_csv(self, request):
            try:
                if request.method == "POST":
                    csv_file = request.FILES["csv_upload"]
                    if not csv_file.name.endswith('.csv'):
                        messages.warning(request, 'The wrong file type was uploaded')
                        return HttpResponseRedirect(request.path_info)
                    file_data = csv_file.read().decode("utf-8")
                    csv_data = file_data.split("\n")
                    for x in csv_data:
                        fields = x.split(",")
                        try:
                            created = Product.objects.update_or_create(
                                title=fields[0],
                                sku=fields[1],
                                short_description=fields[2],
                                detail_description=fields[3],
                                product_image=fields[4],
                                #product_image1=fields[5],
                                #product_image2=fields[6],
                                price=fields[7],
                                #is_active=fields[7],
                                #is_featured=fields[8],
                                category=Category.objects.get(pk=(fields[8]))
                                #is_active=fields[5],
                                #category=fields[6],
                                )
                        except IndexError:
                            pass
                        except (ValidationError,IntegrityError) as e:
                            form = CsvImportForm()
                            data = {"form": form}
                            #raise Http404
                            #message=messages.warning(request,e)
                            message=messages.warning(request,"Something went wrong! check your file again \t   1.Upload correct file \t   2.Check your data once")
                            return render(request, "admin/csv_upload.html", data)         
                    url = reverse('admin:index')
                    return HttpResponseRedirect(url)
                #image_tag.short_description = 'Image'
                form = CsvImportForm()
                data = {"form": form}
                return render(request, "admin/csv_upload.html", data)
            except exception as e:
                messages.error(request,e)
                #return HttpResponse("Something went wrong")
    except exception as e:
        raise Http404      
##################################################################################################################################
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'product', 'quantity','attributes', 'status', 'ordered_date','created_at')
    list_editable = ('quantity', 'status','user','product')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')
    save_on_top = True
#############################################################################################################################
class AttributesAdmin(admin.ModelAdmin):
    list_display=('Product','Color','Size')
    list_filter=('Product','Color','Size')
    list_per_page = 20
    search_fields = ('Product','Color','Size')
    save_on_top = True
##################################################################################################################################
###############################################################################################################################
class salesAdmin(admin.ModelAdmin):
    #ProductAdmin.discount_()
    list_display=('campaign_name','startdate','enddate','sales_discount','is_active','created_at')
    list_filter=('campaign_name','startdate','enddate','sales_discount')
    list_editable = ('is_active', )
    list_per_page = 20
    search_fields = ('campaign_name','startdate','enddate')
    save_on_top = True
##################################################################################################################################
admin.site.register(Order,OrderAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Attributes,AttributesAdmin)
admin.site.register(sales,salesAdmin)
