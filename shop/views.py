
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language, 
                                     translations__slug=category_slug
                                    )
        products = products.filter(category=category)
    context = {'category': category,
                'categories': categories,
                'products': products}    
    return render(request, 'shop/product/list.html', context)

# def product_detail(request, id, slug):
#     product = get_object_or_404(Product,
#                                 id=id,
#                                 slug=slug,
#                                 available=True)
#     return render(request,
#                 'shop/product/detail.html',
#                 {'product': product})
def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, 
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    
    context = {'product': product, 'cart_product_form': cart_product_form, 'recommended_products': recommended_products}
    return render(request, 'shop/product/detail.html', context)                
