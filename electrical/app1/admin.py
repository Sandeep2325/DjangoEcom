# import time
# from reportlab.platypus import SimpleDocTemplate,Table
# import pdfkit
# import ast
# from xhtml2pdf import pisa
# from django import forms
# from django.views.generic import View
# from io import BytesIO
# from django.contrib.admin import AdminSite
#from rest_framework.authtoken.models import Token
from re import S
from this import s
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.db import connection

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User
import mailbox
from django.contrib.auth.models import Group
from asyncio.windows_events import NULL
#from email.headerregistry import Group
from logging import exception
#from tokenize import group
from django.contrib import admin
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from . models import *
from django.urls import path
from . forms import *
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.html import format_html
# from django.core.files.images import get_image_dimensions
from math import ceil
# from django.contrib.auth.models import User
from django.contrib import messages
from import_export.admin import ExportActionMixin
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model
from embed_video.admin import AdminVideoMixin, AdminVideoWidget
import pandas as pd
#from .views import serve_pdf_preview
import pdfkit
import tempfile
import zipfile
import csv
from django.urls import reverse_lazy
from django.contrib.auth.admin import UserAdmin
from django.db.models import Avg
from django.core.mail import send_mail
import math
import random
from admin_actions.admin import ActionsModelAdmin
###########################################################################################################################################

class AddressAdmin(ExportActionMixin, admin.ModelAdmin):
   #
    # env\Lib\site-packages\jazzmin\static\jazzmin\js\action_button.js
    js = ('jazzmin/js/action_button.js',)
    list_display = ('id', 'user', 'door_number', 'street', 'city',
                    'country', 'pincode', 'phone_no', 'alternate_phone_no')
    list_filter = ('city', 'user', 'state', 'pincode')
    list_per_page = 10
    search_fields = ('user', 'city', 'state', 'pincode')
    # actions=['downloadCV']
    #autocomplete_fields = ['user']
    save_on_top = True

    class Meta:
        verbose_name_plural = "Customer Address"
#####################################################################################################

class imageAdmin(admin.ModelAdmin):
    try:
        def image_tag(self, obj):
            return format_html('<img src="{}"width="{}" height="{}"/>'.format(obj.image.url, "100", "100"))
        image_tag.short_description = 'Image'
        image_tag.allow_tags = True
        list_display = ['id', 'image_tag', 'action_btn']

        def action_btn(self, obj):
            html = "<div class='field-action_btn d-flex m-8'> "
            try:
                html += "<a class='text-success fa fa-eye ml-2' href='{}'></a><br></br>".format(
                    obj.image.url, "100", "100")
            except:
                html += "<a class='text-success fa fa-eye ml-2' href='https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg'width='100' height='100'></a><br></br>".format(
                    obj.image.url)
            html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/image/" + \
                str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
        action_btn.short_description = "Action"

        def get_urls(self):
            urls = super().get_urls()
            new_urls = [path('upload-csv/', self.upload_csv), ]
            return new_urls + urls

        def upload_csv(self, request):
            try:
                if request.method == "POST":
                    csv_file = request.FILES["csv_upload"]
                    # csvv=pd.read_csv(csv_file)

                    if not csv_file.name.endswith('.csv'):
                        messages.warning(request, 'Please upload csv file')
                        return HttpResponseRedirect(request.path_info)
                    file_data = csv_file.read().decode("utf-8")
                    csv_data = file_data.split("\r\n")
                    for x in csv_data:
                        fields = x.split(",")
                        try:
                            created = image.objects.create(
                                image="product/"+fields[0],)
                            created.save()
                        except IndexError:
                            pass
                        except (ValidationError, IntegrityError):
                            form = CsvImportForm()
                            data = {"form": form}
                            message = messages.warning(
                                request, 'Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
                            return render(request, "admin/csv_upload.html", data)
                    url = reverse('admin:index')
                    return HttpResponseRedirect(url)
                form = CsvImportForm()
                data = {"form": form}
                return render(request, "admin/csv_upload.html", data)
            except:
                pass
    except:
        pass
##################################################################################################################################

class CategoryAdmin(ExportActionMixin, admin.ModelAdmin):
    try:
        def image_tag(self, obj):
            try:
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.category_image.url, "100", "100"))
            except:
                return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
                #message=messages.warning('Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
        image_tag.short_description = 'Brand Thumbnail'
        image_tag.allow_tags = True
        list_display = ['id', 'brands', 'image_tag',
                        'is_active', 'updated_at', 'action_btn']
        #list_editable = ('slug', )
        list_editable = ('is_active',)
        list_filter = ('brands', 'is_active', 'updated_at')
        list_per_page = 10
        search_fields = ('brands', 'description', 'is_active', 'updated_at')
        save_on_top = True

        def action_btn(self, obj):
            html = "<div class='field-action_btn d-flex '> <a class='fa fa-edit ml-2' href='/admin/app1/category/" + \
                str(obj.id)+"/change/'></a><br></br>"
            try:
                html += "<a class='text-success fa fa-eye ml-2' href='{}'></a><br></br>".format(
                    obj.category_image.url, "100", "100")
            except:
                html += "<a class='text-success fa fa-eye ml-2' href='https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg'width='100' height='100'></a><br></br>"
            html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/category/" + \
                str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
        action_btn.short_description = "Action"
        #prepopulated_fields = {"slug": ("title", )}

        def get_urls(self):
            urls = super().get_urls()
            new_urls = [path('upload-csv/', self.upload_csv), ]
            return new_urls + urls

        def upload_csv(self, request):
            try:
                if request.method == "POST":
                    csv_file = request.FILES["csv_upload"]
                    if not csv_file.name.endswith('.csv'):
                        messages.warning(
                            request, 'The wrong file type was uploaded')
                        return HttpResponseRedirect(request.path_info)
                    file_data = csv_file.read().decode("utf-8")
                    csv_data = file_data.split("\r\n")
                    for x in csv_data:
                        fields = x.split(",")
                        try:
                            created = Category.objects.create(
                                brands=fields[0],
                                description=fields[1],
                                category_image="category/"+fields[2],)
                            created.save()
                        except IndexError:
                            pass
                        except (ValidationError, IntegrityError):
                            form = CsvImportForm()
                            data = {"form": form}
                            message = messages.warning(
                                request, 'Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
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
#################################################################################################################################################
class BrandAdmin(ExportActionMixin, admin.ModelAdmin):
    try:
        def image_tag(self, obj):
            try:
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.logo.url, "100", "100"))
            except:
                return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
                #message=messages.warning('Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
        image_tag.short_description = 'Brand Thumbnail'
        image_tag.allow_tags = True
        list_display = ['id','brand_name', 'image_tag','details','date','action_btn']
        #list_editable = ('slug', )
        #list_editable = ('is_active',)
        list_filter = ('brand_name', 'date')
        #list_per_page = 10
        search_fields = ('brand_name', 'details', 'date')
        save_on_top = True

        def action_btn(self, obj):
            html = "<div class='field-action_btn d-flex '> <a class='fa fa-edit ml-2' href='/admin/app1/category/" + \
                str(obj.id)+"/change/'></a><br></br>"
            try:
                html += "<a class='text-success fa fa-eye ml-2' href='{}'></a><br></br>".format(
                    obj.logo.url, "100", "100")
            except:
                html += "<a class='text-success fa fa-eye ml-2' href='https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg'width='100' height='100'></a><br></br>"
            html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/category/" + \
                str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
        action_btn.short_description = "Action"
    except:
        pass
############################################################################
class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    try:
        #inlines = [ProductImageAdmin]
        def imagee(self, obj):
            # a=obj.image.first()
            # print(obj.image.first().image.url)
            try:
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.image.first().image.url, "50", "50"))
            except:
                return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
        imagee.short_description = 'Product Image'

        def image_tag2(self, obj):
            try:
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.product_image.url, "50", "50"))
            except:
                return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
        image_tag2.short_description = 'Product Thumbnail'
        image_tag2.allow_tags = True
        list_display = ['id', 'title', 'category', 'brand','image_tag2', 'imagee', 'price', 'discounted_price', 'is_active',
                        'updated_at', 'average_rating', 'count_review','action_btn']  # ,'is_active','is_featured'
        list_editable = ('category', 'is_active','brand')
        list_filter = ('category', 'is_active', 'updated_at')
        list_per_page = 20
        #inlines = [ImagemInline]
        search_fields = ('title', 'short_description',
                         'is_active', 'updated_at')
        save_on_top = True
        actions = ['sales_discount', 'delete_offers']
        actions_list = ['sales_discount', 'delete_offers']
        actions_row = ['sales_discount', 'delete_offers']
        actions_detail = ['sales_discount', 'delete_offers']

        def action_btn(self, obj):
            html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/product/" + \
                str(obj.id)+"/change/'></a><br></br>"
            try:
                html += "<a class='text-success fa fa-eye ml-2' href='{}'></a><br></br>".format(
                    obj.image.first().image.url, "100", "100")
            except:
                html += "<a class='text-success fa fa-eye ml-2' href='https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg'width='100' height='100'></a><br></br>"
            html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/product/" + \
                str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
        action_btn.short_description = "Action"

        def delete_offers(self, request, queryset):
            """ from django.db import connection
            cursor = connection.cursor()
            cursor.execute("update app1_product set discounted_price =NULL") """
            for product in queryset:
                product.discounted_price = NULL
                product.save(update_fields=['discounted_price'])
                if product.discounted_price == 0:
                    from django.db import connection
                    cursor = connection.cursor()
                    cursor.execute(
                        "update app1_product set discounted_price =NULL where discounted_price=0")

        def sales_discount(self, request, queryset):
            Sales = sales.objects.all()
            # print(Sales)
            for sale in Sales:
                discount = sale.sales_discount  # percentage
                print("##################################", discount)
                if sale.is_active == True:
                    for product in queryset:
                        print("***************************", discount)
                        multiplier = discount / 100  # discount / 100 in python 3
                        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", multiplier)
                        old_price = product.price
                        new_price = ceil(old_price - (old_price * multiplier))
                        product.discounted_price = new_price
                        product.save(update_fields=['discounted_price'])

                elif sale.is_active == False:
                    return messages.warning(request, 'No active Discounts')
                else:
                    print(sale.id)
                    return messages.warning(request, 'No Discounts')
        sales_discount.short_description = format_html(
            "<p class='text-success fa fa-tags'><span class='ml-2'>Apply discount</span></p>")

        def get_urls(self):
            urls = super().get_urls()
            new_urls = [path('upload-csv/', self.upload_csv), ]
            return new_urls + urls

        def upload_csv(self, request):
            try:
                if request.method == "POST":
                    csv_file = request.FILES["csv_upload"]
                    if not csv_file.name.endswith('.csv'):
                        messages.warning(request, 'Please upload csv file')
                        return HttpResponseRedirect(request.path_info)
                    file_data = csv_file.read().decode("utf-8")
                    #import csv
                    #records = csv.reader(csv_file)
                    csv_data = file_data.split("\n")
                    #csv_data = records.split("\n")
                    for x in csv_data:
                        print(x, type(x))
                        fields = x.split(",")
                        # print(fields)
                        try:
                            # print(fields[7])
                            created, k = Product.objects.update_or_create(
                                title=fields[0],
                                sku=fields[1],
                                short_description=fields[2],
                                detail_description=fields[3],
                                product_image="product/"+fields[4],
                                price=fields[6],
                                category=Category.objects.get(pk=(fields[5])),
                                brand=Brand.objects.get(pk=(fields[7])),
                            )
                            n = str(x)
                            l = n.split('"')
                            if len(l) > 1:
                                k = l[1].split('"')

                                images_csv = (k[0].split('"'))
                                splited_image = (images_csv[0].split(','))

                                for i in range(len(splited_image)):
                                    iter_image = splited_image[i]
                                    # print("IM",iter_image)
                                    imagess = image.objects.get(
                                        pk=(int(iter_image)))

                                    created.image.add(imagess)
                                    created.save()

                            else:

                                print(fields[8])
                                imagess = image.objects.get(pk=(fields[7])),
                                created.image.add(imagess)
                                created.save()

                        except IndexError:
                            pass

                        except (ValidationError, IntegrityError):
                            form = CsvImportForm()
                            data = {"form": form}

                            """ if TypeError:
                                message=messages.warning(request,"Check the category ID") """
                            message = messages.warning(
                                request, "Something went wrong! check your file again \n 1.Upload correct file \n 2.Check your data once")
                            return render(request, "admin/csv_upload.html", data)
                        except TypeError as e:
                            form = CsvImportForm()
                            data = {"form": form}
                            message = messages.warning(request, e)
                            #message=messages.warning(request,"Check the category ID")
                            return render(request, "admin/csv_upload.html", data)
                        except:
                            form = CsvImportForm()
                            data = {"form": form}
                            message = messages.warning(
                                request, "category or image query doesnt exist")

                            return render(request, "admin/csv_upload.html", data)
                    url = reverse('admin:index')
                    return HttpResponseRedirect(url)

                form = CsvImportForm()
                data = {"form": form}
                return render(request, "admin/csv_upload.html", data)
            except (IntegrityError) as e:
                messages.error(request, e)

    except exception:
        pass

##################################################################################################################################
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'product', 'quantity', 'pricee','offer_price','Total_amount',
                    'coupon', 'attributes', 'status', 'ordered_date', 'updated_at', 'action_btn')
    list_editable = ('quantity', 'status', 'user', 'product')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    #search_fields = ('user', 'product')
    action = None
    save_on_top = True

    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/order/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/order/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/order/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"

    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("price", )
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        return form
#############################################################################################################################


class AttributesAdmin(admin.ModelAdmin):
    list_display = ('id', 'Product', 'Color', 'Size', 'action_btn')
    list_filter = ('Product', 'Color', 'Size')
    list_per_page = 20
    search_fields = ('Product', 'Color', 'Size')
    save_on_top = True

    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/attributes/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/attributes/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/attributes/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
###############################################################################################################################
class salesAdmin(admin.ModelAdmin):
    list_display = ('id', 'campaign_name', 'startdate', 'enddate',
                    'sales_discount', 'is_active', 'created_at', 'action_btn')
    list_filter = ('campaign_name', 'startdate', 'enddate', 'sales_discount')
    list_editable = ('is_active', )
    list_per_page = 20
    search_fields = ('campaign_name', 'startdate', 'enddate')
    save_on_top = True

    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/sales/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/sales/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/sales/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"

##################################################################################################################################

class CoupenAdmin(admin.ModelAdmin):
    list_display = ['id', 'coupon', 'coupon_discount',
                    'startdate', 'enddate', 'created_at', 'action_btn']
    #list_filter = ['is_active','startdate','enddate']
    search_fields = ['created_at']
    #list_editable = ('is_active', )

    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/coupon/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/coupon/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/coupon/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
##############################################################################################################################


class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'Reviews', 'Rating',
                     'status_', 'created_date', 'action_btn']
    search_fields = ['user']
    actions = ['approved_status', 'rejected_status']

    def has_add_permission(self, request):
        return True

    def action_btn(self, obj):
        html = "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/rating/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Delete"

    @admin.action(description='Approve')
    def approved_status(self, request, queryset):
        queryset.update(Status="Approved")

    @admin.action(description='Reject')
    def rejected_status(self, request, queryset):
        queryset.update(Status='Rejected')

 #####################################################################################


class BlogAdmin(AdminVideoMixin, SummernoteModelAdmin):
    try:
        """ def dummy(self,obj):
            html="<object style='height: 100px; width: 100%'><param name='movie' value='https://youtu.be/HYOvEIimVzI'>"
            html+="<param name='allowFullScreen' value='true'><param name='allowScriptAccess' value='always'>"
            html+="<embed src='https://youtu.be/HYOvEIimVzI' type='application/x-shockwave-flash' allowfullscreen='true' allowScriptAccess='always' width='640' height='390'></object>"
            return format_html(html)         
        dummy.allow_tags=True"""

        def imagee(self, obj):
            # a=obj.image.first()
            # print(obj.image.first().image.url)
            try:
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.image.first().image.url, "100", "100"))
            except:
                return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
        imagee.short_description = 'Image'
        imagee.allow_tags = True

        def image_tag(self, obj):
            try:
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.images.url, "100", "100"))
            except:
                return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
                #message=messages.warning('Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
        image_tag.short_description = 'Thumbnail Image'
        image_tag.allow_tags = True

        def video_url(self, obj):
            return format_html('<a class="fa fa-play fa-1x" href="%s"><span class="ml-2">Play video</span></a>' % (obj.url))
            # return format_html('<a class="fa fa-play fa-2x" href="%s"></a>' % (obj.url))
        video_url.allow_tags = True
        video_url.short_description = 'video'
        list_display = ['id', 'title', 'description', 'image_tag',
                        'imagee', 'video_url', 'author', 'uploaded_date', 'action_btn']
        search_fields = ['title']
        summernote_fields = ('description', )

        def action_btn(self, obj):
            html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/blog/" + \
                str(obj.id)+"/change/'></a><br></br>"
            html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/blog/" + \
                str(obj.id)+"/change/'></a><br></br>"
            html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/blog/" + \
                str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
        action_btn.short_description = "Action"
    except:
        pass
##############################################################################################################################


class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'Question', 'Answer',
                    'status', 'created_date', 'updated_at']
    search_fields = ['Question']
    actions = ['make_published', 'make_withdraw']

    @admin.action(description='Publish')
    def make_published(modeladmin, request, queryset):
        queryset.update(status='p')

    @admin.action(description='Withdraw')
    def make_withdraw(modeladmin, request, queryset):
        queryset.update(status='w')
##############################################################################################################################
# Banner Register


class BannerAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.image.url, "100", "100"))
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
            #message=messages.warning('Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    list_display = ['id', 'title', 'image_tag', 'uploaded_date', 'action_btn']
    search_fields = ['title']

    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/banner/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/banner/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/banner/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
####################################################################################################################


class customer_messageAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'Phone',
                    'Email', 'Message', 'created_date', 'updated_at', 'action_btn']
    actions = ["send_message"]

    def action_btn(self, obj):
        #html="<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/mailtext/"+str(obj.id)+"/change/'></a><br></br>"
        #html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/mailtext/"+str(obj.id)+"/change/'></a><br></br>"
        html = "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/customer_message/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"

    def send_message(self, request, queryset):
        print(queryset)
        try:
            for i in queryset:
                if i.Email and i.first_name:
                    email = i.Email
                    message = "Hi {},\nyour message was recieved\nthank you ".format(
                        i.first_name)
                    a = send_mail('Prakash Electrical', message, 'gowdasandeep8105@gmail.com', [
                                  email], fail_silently=False,), messages.success(request, "Successfully sent to {}".format(email))
                    print(
                        "++++++++++++++++++++++++++++++++++++++email sent+++++++++++++++++++++++++++++++++++")

        except:
            return messages.warning(request, "something went wrong")
    ##################################################################################################################


class mailadmin(admin.ModelAdmin):
    list_display = ['subject', 'message', 'send_it','status',
                    'created_date', 'updated_at', 'action_btnn']
    actions = ['send_message', 'draft_message']
    list_editable = ['send_it']
    # @admin.action(description='send')
    # def send_message(modeladmin, request, queryset):
    #     queryset.update(status='s')
    # @admin.action(description='draft')
    # def draft_message(modeladmin, request, queryset):
    #     queryset.update(status='d')

    def action_btnn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/mailtext/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/mailtext/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/mailtext/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btnn.short_description = "Action"

    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("send_it", )
        form = super(mailadmin, self).get_form(request, obj, **kwargs)
        return form
###################################################################################################################
class cartadmin(admin.ModelAdmin):
    list_display=['id','user','product','attributes','price','offer_price','quantity','Total_amount','amount_saved','date','updated_at']
    list_editable = ['product','attributes','quantity']   
    search_fields = ['user__username','product__title']
class checkoutadmin(admin.ModelAdmin):
    list_display=['id','products',"Shipping_address"]
    # def get_products(self, obj):
        # return "\n".join([p.product for p in obj.cart.all()])     
class ordersadmin(admin.ModelAdmin):
    list_display=['id',"checkout_product","ordered_date","status"]
    list_editable = ['status']
######################################################################################################
admin.site.register(Orders,ordersadmin)
admin.site.register(checkout,checkoutadmin)
admin.site.register(Cart,cartadmin) 
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Attributes, AttributesAdmin)
admin.site.register(sales, salesAdmin)
admin.site.register(image, imageAdmin)
admin.site.register(Coupon, CoupenAdmin)
# admin.site.register(ClaimedCoupon,claimedcouponAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(customer_message, customer_messageAdmin)
admin.site.register(Banner, BannerAdmin)
# admin.site.register(Mail)
admin.site.register(MailText, mailadmin)
admin.site.unregister(get_attachment_model())
admin.site.unregister(Group)
admin.site.register(Brand,BrandAdmin)

class UserAdmin(ExportActionMixin,OriginalUserAdmin):
    list_display = ['id','username', 'email', 'first_name',
                    'last_name', 'is_staff', 'phone_no', 'action_btn']
    #actions = ['action_btn',]

    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/user/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/user/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/user/" + \
            str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"

admin.site.register(User, UserAdmin)
