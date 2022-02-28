from django_filters import FilterSet, NumberFilter
# from django.apps import app1
from .models import *

class CouponFilter(FilterSet):
    """
    An initial basic filter for Coupons.  This could be handled with filter_fields = () until I add in range filtering
    on the discount value, then it is more helpful to do this.
    """

    min_value = NumberFilter(field_name='value', lookup_expr='gte')
    max_value = NumberFilter(field_name='value', lookup_expr='lte')

    class Meta:
        model = Coupon
        fields = [ 'type', 'min_value', 'max_value']