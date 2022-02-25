from asyncio.windows_events import NULL
from logging import exception
from django.contrib import admin
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
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
# from django.core.files.images import get_image_dimensions
from math import ceil
from django.contrib.auth.models import User
from django.contrib import messages
from import_export.admin import ExportActionMixin
import time
from reportlab.platypus import SimpleDocTemplate,Table
import pdfkit
import ast
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model
#################################################################################################################################### 
def count(request):
    user = User.objects.all().count()
    product=Product.objects.all().count()
    order=Order.objects.all().count()
    print(user,product,order)
    context={
        'user_count':user,
        'product_count':product,
        'order_count':order,
    }
    return render(request,"admin/index.html",context)
###########################################################################################################################################
class AddressAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('id','user','door_number','street','city','country','pincode')
    list_filter = ('city','user','state','pincode')
    list_per_page = 10
    search_fields = ('user', 'city', 'state','pincode')
    save_on_top = True
    class Meta:
        verbose_name_plural = "Customer Address"
#####################################################################################################
class imageAdmin(admin.ModelAdmin):
    try:
        def image_tag(self, obj):
            return format_html('<img src="{}"width="{}" height="{}"/>'.format(obj.image.url,"100","100"))
        image_tag.short_description = 'Image'
        image_tag.allow_tags = True
        list_display=['id','image_tag']
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
                            created = image.objects.create(
                            image="product/"+fields[0],)
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
            except:
                pass
    except:
        pass
##################################################################################################################################

class CategoryAdmin(ExportActionMixin,admin.ModelAdmin):
    try:
        def image_tag(self, obj):
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.category_image.url,"100","100"))
        image_tag.short_description = 'Image'
        image_tag.allow_tags = True
        list_display = ['id','title','image_tag','is_active','updated_at','action_btn']
        #list_editable = ('slug', )
        list_editable=('is_active',)
        list_filter = ('title','is_active','updated_at')
        list_per_page = 10
        search_fields = ('title', 'description','is_active','updated_at')
        save_on_top = True
        def action_btn(self,obj):
            html="<div class='field-action_btn d-flex '> <a class='fa fa-edit ml-2' href='/admin/app1/category/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/category/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-danger fa fa-trash ml-2' href='/admin/app1/category/"+str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
        action_btn.short_description="Action"
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
                            category_image="category/"+fields[2],)
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
##########################################################################################################################################
""" class userAdmin(ExportActionMixin,admin.ModelAdmin):
    pass
admin.site.register(User,userAdmin) """
###################################################################################################################################### 
class ProductImageAdmin(ExportActionMixin,admin.StackedInline):
    model = ProductImage
#admin.site.register(Product,ProductImageAdmin)
class ProductAdmin(ExportActionMixin,admin.ModelAdmin):
    try:
        #inlines = [ProductImageAdmin]
        def imagee(self,obj):
            a=Product.objects.all()
            #print(a)
            for product in a:
                ids=product.image   
                p=Product.objects.get(pk=ids)
                k=p.image.first()
                print(ids)
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(k.image.url,"100","100"))
        def image_tag2(self, obj):
                return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.product_image.url,"100","100"))
        image_tag2.short_description = 'Image2'
        image_tag2.allow_tags = True  
        list_display = ['id','title','category','image_tag2','price','discounted_price','is_active','updated_at','action_btn']#,'is_active','is_featured'
        list_editable = ('category','is_active',)
        list_filter = ('category','is_active','updated_at')
        list_per_page = 20
        #inlines = [ImagemInline]
        search_fields = ('title', 'short_description','is_active','updated_at')
        save_on_top = True
        actions=['sales_discount','delete_offers']
        def action_btn(self,obj):
            html="<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/product/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/product/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-danger fa fa-trash ml-2' href='/admin/app1/product/"+str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
        action_btn.short_description="Action"
        #discount_.short_description=''
        #prepopulated_fields = {"slug": ("title", )}
        """ def delete(self, obj):
            view_name = "admin:{}_{}_delete".format(obj._meta.app_label, obj._meta.model_name)
            link = reverse(view_name,args=[Product.pk])
            html = '<input type="button" class="btn btn-danger", onclick="location.href=\'{}\'" value="Delete" />'.format(link)
            return format_html(html) """
        def delete_offers(self,request,queryset):
            """ from django.db import connection
            cursor = connection.cursor()
            cursor.execute("update app1_product set discounted_price =NULL") """
            for product in queryset:
                product.discounted_price=NULL
                product.save(update_fields=['discounted_price'])
                if product.discounted_price==0:
                    from django.db import connection
                    cursor = connection.cursor()
                    cursor.execute("update app1_product set discounted_price =NULL where discounted_price=0")
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
                            print(fields[7])
                            created = Product.objects.update_or_create(
                                title=fields[0],
                                sku=fields[1],
                                short_description=fields[2],
                                detail_description=fields[3],
                                product_image="product/"+fields[4], 
                                #image=image.objects.get(pk=(fields[5])),
                                #is_active=fields[5],
                                #product_image1="product/"+fields[5],
                                #product_image2="product/"+fields[6],
                                #images=image.objects.get(pk=(fields[4])),
                                #image=fields[5],
                                price=fields[6],
                                #is_active=fields[7],
                                #is_featured=fields[8],
                                category=Category.objects.get(pk=(fields[7])),
                                #is_active=fields[5],
                                #category=fields[6],
                                )
                            #print(created)
                            #for i in fields[5]:
                                #print(i) 
                            imagess=image.objects.get(pk=(fields[5]))
                            #print(imagess)
                            #for i in imagess:
                            #a=[0,1,2,3,4,5,6,7,8]
                            #for i in len(fields[5]):
                            #print(i)  
                            created[0].image.add(imagess)
                            created[0].save()
                            #print(created)
                        except IndexError:
                            pass
                        except (ValidationError,IntegrityError):
                            form = CsvImportForm()
                            data = {"form": form}
                            #raise Http404
                            #message=messages.warning(request,e)
                            """ if TypeError:
                                message=messages.warning(request,"Check the category ID") """
                            message=messages.warning(request,"Something went wrong! check your file again \t   1.Upload correct file \t   2.Check your data once")
                            return render(request, "admin/csv_upload.html", data)
                        except TypeError as e:
                            form = CsvImportForm()
                            data = {"form": form}
                            message=messages.warning(request,e)
                            #message=messages.warning(request,"Check the category ID")
                            return render(request, "admin/csv_upload.html", data)
                    url = reverse('admin:index')
                    return HttpResponseRedirect(url)
                #image_tag.short_description = 'Image'
                form = CsvImportForm()
                data = {"form": form}
                return render(request, "admin/csv_upload.html", data)
            except (TypeError,IntegrityError) as e:
                #raise Http404
                messages.error(request,e)
                #return HttpResponse("Something went wrong")
    except exception:
        pass
        #print(e)      
##################################################################################################################################
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','address', 'product', 'quantity','price','attributes', 'status', 'ordered_date','created_at','action_btn')
    list_editable = ('quantity', 'status','user','product')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    #search_fields = ('user', 'product')
    action=None
    save_on_top = True
    def action_btn(self,obj):
            html="<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/order/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/order/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-danger fa fa-trash ml-2' href='/admin/app1/order/"+str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
    action_btn.short_description="Action"
#############################################################################################################################
class AttributesAdmin(admin.ModelAdmin):
    list_display=('id','Product','Color','Size','action_btn')
    list_filter=('Product','Color','Size')
    list_per_page = 20
    search_fields = ('Product','Color','Size')
    save_on_top = True
    def action_btn(self,obj):
            html="<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/attributes/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/attributes/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-danger fa fa-trash ml-2' href='/admin/app1/attributes/"+str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
    action_btn.short_description="Action"
###############################################################################################################################
class salesAdmin(admin.ModelAdmin):
    list_display=('id','campaign_name','startdate','enddate','sales_discount','is_active','created_at','action_btn')
    list_filter=('campaign_name','startdate','enddate','sales_discount')
    list_editable = ('is_active', )
    list_per_page = 20
    search_fields = ('campaign_name','startdate','enddate')
    save_on_top = True
    def action_btn(self,obj):
            html="<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/sales/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/sales/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-danger fa fa-trash ml-2' href='/admin/app1/sales/"+str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
    action_btn.short_description="Action"
##################################################################################################################################
class CoupenAdmin(admin.ModelAdmin):
    list_display = ['id','created','updated','code','type','expires','value','repeat','action_btn']
    # list_filter = ['active','valid_from','valid_to']
    search_fields = ['created']
    def action_btn(self,obj):
            html="<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/coupon/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/coupon/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-danger fa fa-trash ml-2' href='/admin/app1/coupon/"+str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
    action_btn.short_description="Action"
##############################################################################################################################
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','Message','Rating','Status','action_btn']
    search_fields = ['user']
    list_editable = ('Status','Rating' )
    def action_btn(self,obj):
            #html="<input class='text-danger fa fa-check' type='submit' value='Reject' name='form-0-Status'> <input class='text-success fa fa-ban' type='submit' value='Approve' name='form-0-Status'> <input type='hidden' name='id' value=form-0-Status>"
            html="<button class='text-success fa fa-check'></button>"
            html+="<button class='text-danger fa fa-ban'></button>"
            return format_html(html)
    action_btn.short_description="Action"
##############################################################################################################################
class BlogAdmin(SummernoteModelAdmin):
    try:
        """ def dummy(self,obj):
            
            html="<object style='height: 100px; width: 100%'><param name='movie' value='%s'>"
            html+="<param name='allowFullScreen' value='true'><param name='allowScriptAccess' value='always'>"
            html+="<embed src='%s' type='application/x-shockwave-flash' allowfullscreen='true' allowScriptAccess='always' width='640' height='390'></object>"%(obj.url)
            return format_html(html)        
        dummy.allow_tags=True """
        def imagee(self,obj):
            return format_html('<img src="{}" width="{}" height="{}" />'.format(obj.image.url,"100","100"))
        imagee.short_description='image'
        def video_url(self, obj):
            return format_html('<a class="fa fa-play" href="%s"></a>' % (obj.url))
        video_url.allow_tags = True
        video_url.short_description='video'
        list_display=['id','title','description','imagee','video_url','author','uploaded_date','action_btn']
        search_fields=['title']
        summernote_fields = ('description', )
        def action_btn(self,obj):
            html="<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/blog/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/blog/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-danger fa fa-trash ml-2' href='/admin/app1/blog/"+str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
        action_btn.short_description="Action"
    except:
        pass
    #summernote_fields = ('content', )
##############################################################################################################################
class FAQAdmin(admin.ModelAdmin):
    list_display=['id','Question','Answer']
    search_fields=['Question']
##############################################################################################################################
#Banner Register 
class BannerAdmin(admin.ModelAdmin):
    def imagee(self,obj):
            return format_html('<img src="{}" width="{}" height="{}" />'.format(obj.image.url,"100","100"))
    imagee.short_description='image'
    list_display=['id','title','imagee','uploaded_date','action_btn']
    search_fields=['title']
    def action_btn(self,obj):
            html="<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/banner/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-success fa fa-eye ml-2' href='/admin/app1/banner/"+str(obj.id)+"/change/'></a><br></br>"
            html+="<a class='text-danger fa fa-trash ml-2' href='/admin/app1/banner/"+str(obj.id)+"/delete/'></a></div>"
            return format_html(html)
    action_btn.short_description="Action"
###############################################################################################################################
class claimedcouponAdmin(admin.ModelAdmin):
    list_display=['id','user','coupon','redeemed']
    search_fields=['user','coupon','redeemed']
####################################################################################################################
class customer_messageAdmin(admin.ModelAdmin):
    list_display=['id','Name','Phone','Email','Message']
###################################################################################################################
admin.site.register(Order,OrderAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Attributes,AttributesAdmin)
admin.site.register(sales,salesAdmin)
admin.site.register(image,imageAdmin)
admin.site.register(Coupon,CoupenAdmin)
admin.site.register(ClaimedCoupon,claimedcouponAdmin)
admin.site.register(Rating,RatingAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(customer_message,customer_messageAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.unregister(get_attachment_model())
