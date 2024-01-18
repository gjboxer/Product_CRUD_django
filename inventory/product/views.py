from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the product index.")

def product_list(request):
    if request.method == "GET":
        data = request.GET
        error=""
        try:
            if data.get("id"):
                products = Product.objects.filter(id=data.get("id"))
            elif data.get("name"):
                products = Product.objects.filter(name=data.get("name"))
                
        except Product.DoesNotExist:
            error="Product not found"
        return JsonResponse({"products": list(products.values()),"error":error})

@csrf_exempt
def product_update(request,pk):
    product = get_object_or_404(Product, pk=pk)
    
    data=json.loads(request.body.decode('utf-8'))
    if data=={}:
        return JsonResponse({'message': 'Invalid data'})
    if request.method == "PUT":
        product.name = data.get("name")
        product.price = data.get("price")
        product.desc = data.get("desc")
        product.save()
    elif request.method == "PATCH":
        if data.get("name"):
            product.name = data.get("name")
        if data.get("price"):
            product.price = data.get("price")
        if data.get("desc"):
            product.desc = data.get("desc")
        product.save()
    return JsonResponse({'message': 'Product updated successfully'})


@csrf_exempt
def product_delete(request,name):
    product = get_object_or_404(Product,name=name)
    product.delete()
    return JsonResponse({'message': 'Product deleted successfully'})