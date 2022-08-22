from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.recommender import Recommender

#customizing the admin page order
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from cart.cart import Cart

#pdf invoice
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cart = Cart(request)
    html = render_to_string('orders/order/pdf.html', {'order': order, 'cart': cart})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response




@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cart = Cart(request)
    return render(request,
                'admin/orders/order/detail.html',
                {'order': order, 'cart':cart})

# Create your views here.

def order_create(request):
    cart = Cart(request)
    r = Recommender()
    products = [item['product'] for item in cart]
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            r.products_bought(products)
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
                order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
            # return render(request, 'orders/order/created.html', {'order': order})
        else:
            return HttpResponse("Please, fill in form correctly...")    
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})