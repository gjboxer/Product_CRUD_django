from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the product index.")

@csrf_exempt
def product_list(request, name=None):
    if request.method == 'GET':
        data = request.GET.get('name', None)
        if data:
            products = Product.objects.filter(name__icontains=data)
        else:
            products = Product.objects.all()

        product_list = [{'id': product.id, 'name': product.name, 'price': str(product.price), 'desc': product.desc} for product in products]
        return JsonResponse({'products': product_list})

    elif request.method == 'POST':
        data = json.loads(request.body)
        new_product = Product(name=data.get('name'), price=data.get('price'), desc=data.get('desc'))
        new_product.save()
        return JsonResponse({'id': new_product.id, 'name': new_product.name, 'price': str(new_product.price), 'desc': new_product.desc}, status=201)

    else:
        return HttpResponse(status=400)

@csrf_exempt
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found'}, status=404)

    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message': 'Product deleted'})

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)