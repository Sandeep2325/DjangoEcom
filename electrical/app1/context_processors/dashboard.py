from app1.models import *
def dashboard(request):
    return {'model1': Product.objects.all()}