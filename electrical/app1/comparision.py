
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.forms import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from app1.paginations import PaginationHandlerMixin
class MyPaginator(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'page_size'
    max_page_size = 1000
class comparisionview(APIView,PaginationHandlerMixin):
    pagination_class = MyPaginator
    permission_classes = (AllowAny,)
    serializer_class = comparisionSerializer
    def post(self, request):
        print(request.data)
        attribute_id=request.data["attribute_id"]
        print(attribute_id)
        print(bool(attribute_id))
        brand_id=request.data["brand_id"]
        print(brand_id)
        print(bool(brand_id))
        type_id=request.data["type_id"]
        print(type_id)
        print(bool(type_id))
        subcategory_key=request.data["subcategory_key"]
        print(subcategory_key)
        print(bool(subcategory_key))
        product_amps=request.data["product_amps"]
        product_volts=request.data["product_volts"]
        if bool(subcategory_key)==True and bool(product_amps)==True and bool(product_volts)==True and  bool(type_id)==False and bool(brand_id)==False and bool(attribute_id)==False:
            data=Product.objects.filter(subcategory__sub_category=subcategory_key,amps__in=product_amps,volts__in=product_volts)
            product_serializer=productSerializer(data,many=True)
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = self.get_paginated_response(productSerializer(page,many=True).data)
                return Response(serializer.data)
            else:
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
            
            
        elif bool(subcategory_key)==True and bool(product_amps)==True and bool(product_volts)==True and bool(attribute_id)==True and bool(type_id)==False and bool(brand_id)==False:
            data=Product.objects.filter(subcategory__sub_category=subcategory_key,attributes_id__in=attribute_id,amps__in=product_amps,volts__in=product_volts),
            # data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-created_at')
            product_serializer=productSerializer(data,many=True)
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = self.get_paginated_response(productSerializer(page,many=True).data)
                return Response(serializer.data)
            else:
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
            
            
            
        elif bool(subcategory_key)==True and  bool(product_amps)==True and bool(product_volts)==True and bool(attribute_id)==False and bool(type_id)==True and bool(brand_id)==False:
            data=Product.objects.filter(subcategory__sub_category=subcategory_key,type_id__in=type_id,amps__in=product_amps,volts__in=product_volts)
            # data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-created_at')
            product_serializer=productSerializer(data,many=True)
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = self.get_paginated_response(productSerializer(page,many=True).data)
                return Response(serializer.data)
            else:
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
            
            
        elif bool(subcategory_key)==True and bool(product_amps)==True and bool(product_volts)==True and bool(attribute_id)==False and bool(type_id)==False and bool(brand_id)==True:
            data=Product.objects.filter(subcategory__sub_category=subcategory_key,brand_id__in=brand_id,amps__in=product_amps,volts__in=product_volts)
            # data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-created_at')
            product_serializer=productSerializer(data,many=True)
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = self.get_paginated_response(productSerializer(page,many=True).data)
                return Response(serializer.data)
            else:
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
            
            
            
        elif bool(subcategory_key)==True and bool(product_amps)==True and bool(product_volts)==True and bool(attribute_id)==True and bool(type_id)==False and bool(brand_id)==True:
            data=Product.objects.filter(subcategory__sub_category=subcategory_key,brand_id__in=brand_id,attributes_id__in=attribute_id,amps__in=product_amps,volts__in=product_volts)
            # data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-created_at')
            product_serializer=productSerializer(data,many=True)
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = self.get_paginated_response(productSerializer(page,many=True).data)
                return Response(serializer.data)
            else:
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
            
            
        elif bool(subcategory_key)==True and bool(product_amps)==True and bool(product_volts)==True and bool(attribute_id)==True and bool(type_id)==True and bool(brand_id)==False:
            data=Product.objects.filter(subcategory__sub_category=subcategory_key,type_id__in=type_id,attributes_id__in=attribute_id,amps__in=product_amps,volts__in=product_volts)
            # data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-created_at')
            product_serializer=productSerializer(data,many=True)
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = self.get_paginated_response(productSerializer(page,many=True).data)
                return Response(serializer.data)
            else:
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
            
            
        elif bool(subcategory_key)==True and bool(product_amps)==True and bool(product_volts)==True and bool(attribute_id)==False and bool(type_id)==True and bool(brand_id)==True:
            data=Product.objects.filter(subcategory__sub_category=subcategory_key,type_id__in=type_id,brand_id__in=brand_id,amps__in=product_amps,volts__in=product_volts)
            # data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-created_at')
            product_serializer=productSerializer(data,many=True)
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = self.get_paginated_response(productSerializer(page,many=True).data)
                return Response(serializer.data)
            else:
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
            
            
        elif bool(subcategory_key)==True and bool(product_amps)==True and bool(product_volts)==True and bool(attribute_id)==True and bool(type_id)==True and bool(brand_id)==True:
            data=Product.objects.filter(subcategory__sub_category=subcategory_key,type_id__in=type_id,brand_id__in=brand_id,attributes_id__in=attribute_id,amps__in=product_amps,volts__in=product_volts)
            # data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-created_at')
            product_serializer=productSerializer(data,many=True)
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = self.get_paginated_response(productSerializer(page,many=True).data)
                return Response(serializer.data)
            else:
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
            
