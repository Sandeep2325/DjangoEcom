import json

# import environ
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
# env = environ.Env()

# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
# environ.Env.read_env()
# authentication_classes = [JWTAuthentication,]
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def start_payment(request):
    # request.data is coming from frontend
    
    product_count=request.data['product_count']
    total_price=request.data['total_price']
    address_id=request.data['address_id']
    cart_id=request.data['cart_id']
    coupon=request.data['coupon']
    user=request.user
    print(user)
    print(product_count)
    print(total_price)
    print(address_id)
    print(cart_id)
    productsss = Cart.objects.filter(id__in=cart_id)
    print(productsss)
    shipping_address=Address.objects.get(id=int(address_id))
    # setup razorpay client
    client=razorpay.Client(auth=('rzp_test_JiD8eNtJ2aNwZr','gtukARkLZ5U4Bjo9EfCSWkMf'))
    # create razorpay order
    payment = client.order.create({"amount": int(total_price) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False
    order = cart_order.objects.create(
                                user=request.user,
                                coupon=coupon,
                                 total_price=total_price, 
                                order_payment_id=payment['id'],
                                 product_count=product_count,
                                 shipping_address=shipping_address,
                                 )
    for i in productsss:
        order.products.add(i.id)
    serializer = cartorderserializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '20 November 2020 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)
@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = cart_order.objects.get(order_payment_id=ord_id)

    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }
    client=razorpay.Client(auth=('rzp_test_JiD8eNtJ2aNwZr','gtukARkLZ5U4Bjo9EfCSWkMf'))

    # client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # checking if the transaction is valid or not if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.is_paid = True
    order.save()
    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)