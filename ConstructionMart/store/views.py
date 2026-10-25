from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem

def _cart(request):
    return request.session.setdefault("cart", {})

def _cart_details(request):
    cart = request.session.get("cart", {})
    rows, total, count = [], Decimal("0.00"), 0
    ids = [int(k) for k in cart.keys()] if cart else []
    products = {p.id: p for p in Product.objects.filter(id__in=ids)}
    for key, quantity in cart.items():
        product = products.get(int(key))
        if not product:
            continue
        quantity = max(1, int(quantity))
        line_total = product.price * quantity
        rows.append({"product": product, "quantity": quantity, "line_total": line_total})
        total += line_total
        count += quantity
    return rows, total, count

def home(request):
    products = Product.objects.all()
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    if category:
        products = products.filter(category=category)
    _, _, cart_count = _cart_details(request)
    return render(request, "store/home.html", {
        "products": products, "query": query, "selected_category": category,
        "categories": Product.CATEGORY_CHOICES, "cart_count": cart_count,
    })

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        quantity = int(request.POST.get("quantity", "1"))
    except ValueError:
        quantity = 1
    if product.stock <= 0:
        messages.error(request, f"{product.name} is currently out of stock.")
        return redirect(request.META.get("HTTP_REFERER", "home"))
    quantity = max(1, min(quantity, product.stock))
    cart = request.session.get("cart", {})
    existing_quantity = max(0, int(cart.get(str(product.id), 0)))
    cart[str(product.id)] = min(existing_quantity + quantity, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.META.get("HTTP_REFERER", "home"))

def cart_view(request):
    rows, total, count = _cart_details(request)
    return render(request, "store/cart.html", {"rows": rows, "total": total, "cart_count": count})

@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        quantity = int(request.POST.get("quantity", "1"))
    except ValueError:
        quantity = 1
    cart = request.session.get("cart", {})
    if quantity <= 0:
        cart.pop(str(product_id), None)
    elif product.stock <= 0:
        cart.pop(str(product_id), None)
        messages.error(request, f"{product.name} is currently out of stock.")
    else:
        cart[str(product_id)] = min(quantity, product.stock)
    request.session["cart"] = cart
    return redirect("cart")

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")

@transaction.atomic
def checkout(request):
    rows, total, count = _cart_details(request)
    if not rows:
        messages.info(request, "Your cart is empty. Add a product before checkout.")
        return redirect("home")
    if request.method == "POST":
        name = request.POST.get("customer_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("delivery_address", "").strip()
        if not all([name, email, phone, address]):
            messages.error(request, "Please complete all checkout fields.")
            return render(request, "store/checkout.html", {"rows": rows, "total": total, "cart_count": count})
        # Re-check stock before saving an order.
        for row in rows:
            product = Product.objects.select_for_update().get(pk=row["product"].pk)
            if product.stock < row["quantity"]:
                messages.error(request, f"Not enough stock for {product.name}. Please update your cart.")
                return redirect("cart")
        order = Order.objects.create(
            customer_name=name, email=email, phone=phone,
            delivery_address=address, total=total
        )
        for row in rows:
            product = Product.objects.select_for_update().get(pk=row["product"].pk)
            OrderItem.objects.create(order=order, product=product, quantity=row["quantity"], unit_price=product.price)
            product.stock -= row["quantity"]
            product.save(update_fields=["stock"])
        request.session["cart"] = {}
        request.session["last_order_id"] = order.pk
        return redirect("order_success", order_id=order.pk)
    return render(request, "store/checkout.html", {"rows": rows, "total": total, "cart_count": count})

def order_success(request, order_id):
    # Prevent someone from guessing an order ID to view another customer's address.
    if request.session.get("last_order_id") != order_id:
        messages.info(request, "Please place an order to view its confirmation.")
        return redirect("home")
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "store/order_success.html", {"order": order, "cart_count": 0})
