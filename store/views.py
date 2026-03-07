from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Sum, Count, Q
from .models import Category, Product, Order, OrderItem
import json


# ─── CART HELPERS ──────────────────────────────────────────────────────────────

def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


# ─── STORE FRONT ───────────────────────────────────────────────────────────────

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)
    latest_products = Product.objects.all()[:12]
    return render(request, 'store/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'latest_products': latest_products,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    all_categories = Category.objects.all()
    products = category.products.all()
    q = request.GET.get('q', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    return render(request, 'store/category.html', {
        'category': category,
        'products': products,
        'categories': all_categories,
        'q': q,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
        'categories': Category.objects.all(),
    })


# ─── CART ──────────────────────────────────────────────────────────────────────

def cart(request):
    cart_data = get_cart(request)
    cart_items = []
    total = 0
    for product_id, qty in cart_data.items():
        try:
            p = Product.objects.get(pk=int(product_id))
            subtotal = p.price * qty
            total += subtotal
            cart_items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'categories': Category.objects.all(),
    })


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not product.is_in_stock:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Out of stock'}, status=400)
        messages.error(request, 'Product is out of stock.')
        return redirect('product', slug=product.slug)

    cart_data = get_cart(request)
    pid = str(product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart_data[pid] = cart_data.get(pid, 0) + quantity
    save_cart(request, cart_data)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': sum(cart_data.values())})
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@require_POST
def cart_remove(request, product_id):
    cart_data = get_cart(request)
    cart_data.pop(str(product_id), None)
    save_cart(request, cart_data)
    return redirect('cart')


@require_POST
def cart_update(request):
    cart_data = get_cart(request)
    for key, val in request.POST.items():
        if key.startswith('qty_'):
            pid = key.replace('qty_', '')
            try:
                qty = int(val)
                if qty <= 0:
                    cart_data.pop(pid, None)
                else:
                    cart_data[pid] = qty
            except ValueError:
                pass
    save_cart(request, cart_data)
    return redirect('cart')


# ─── CHECKOUT ──────────────────────────────────────────────────────────────────

def checkout(request):
    cart_data = get_cart(request)
    if not cart_data:
        return redirect('cart')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        wilaya = request.POST.get('wilaya', '').strip()
        notes = request.POST.get('notes', '').strip()

        if not name or not phone:
            messages.error(request, 'Name and phone number are required.')
            return redirect('checkout')

        order = Order.objects.create(
            customer_name=name, phone=phone, email=email,
            wilaya=wilaya, notes=notes, total=0
        )
        total = 0
        for product_id, qty in cart_data.items():
            try:
                p = Product.objects.get(pk=int(product_id))
                OrderItem.objects.create(
                    order=order, product=p,
                    product_name=p.name, product_price=p.price, quantity=qty
                )
                total += p.price * qty
            except Product.DoesNotExist:
                pass
        order.total = total
        order.save()
        request.session['cart'] = {}
        return redirect('order_success', order_id=order.pk)

    cart_items = []
    total = 0
    for product_id, qty in cart_data.items():
        try:
            p = Product.objects.get(pk=int(product_id))
            subtotal = p.price * qty
            total += subtotal
            cart_items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass

    wilayas = [
        "Adrar","Chlef","Laghouat","Oum El Bouaghi","Batna","Béjaïa","Biskra","Béchar",
        "Blida","Bouira","Tamanrasset","Tébessa","Tlemcen","Tiaret","Tizi Ouzou","Alger",
        "Djelfa","Jijel","Sétif","Saïda","Skikda","Sidi Bel Abbès","Annaba","Guelma",
        "Constantine","Médéa","Mostaganem","M'Sila","Mascara","Ouargla","Oran","El Bayadh",
        "Illizi","Bordj Bou Arréridj","Boumerdès","El Tarf","Tindouf","Tissemsilt",
        "El Oued","Khenchela","Souk Ahras","Tipaza","Mila","Aïn Defla","Naâma",
        "Aïn Témouchent","Ghardaïa","Relizane","Timimoun","Bordj Badji Mokhtar",
        "Ouled Djellal","Béni Abbès","In Salah","In Guezzam","Touggourt","Djanet",
        "El M'Ghair","El Meniaa"
    ]

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'wilayas': wilayas,
        'categories': Category.objects.all(),
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/order_success.html', {
        'order': order,
        'categories': Category.objects.all(),
    })


# ─── OWNER DASHBOARD ───────────────────────────────────────────────────────────

def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'store/dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/dashboard/login/')
def dashboard(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    confirmed_orders = Order.objects.filter(status='confirmed').count()
    total_revenue = Order.objects.filter(status__in=['confirmed','delivered']).aggregate(
        total=Sum('total'))['total'] or 0
    total_products = Product.objects.count()
    out_of_stock = Product.objects.filter(is_in_stock=False).count()
    recent_orders = Order.objects.all()[:5]
    return render(request, 'store/dashboard/index.html', {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'out_of_stock': out_of_stock,
        'recent_orders': recent_orders,
    })


@login_required(login_url='/dashboard/login/')
def dashboard_orders(request):
    status_filter = request.GET.get('status', '')
    orders = Order.objects.all()
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'store/dashboard/orders.html', {
        'orders': orders,
        'status_filter': status_filter,
        'statuses': Order.STATUS_CHOICES,
    })


@login_required(login_url='/dashboard/login/')
def dashboard_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/dashboard/order_detail.html', {'order': order})


@login_required(login_url='/dashboard/login/')
@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order_id} status updated to {new_status}.')
    return redirect('dashboard_order_detail', order_id=order_id)


@login_required(login_url='/dashboard/login/')
def dashboard_products(request):
    products = Product.objects.select_related('category').all()
    q = request.GET.get('q', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
    return render(request, 'store/dashboard/products.html', {
        'products': products, 'q': q
    })


@login_required(login_url='/dashboard/login/')
def product_add(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        _save_product(request, None)
        messages.success(request, 'Product added successfully!')
        return redirect('dashboard_products')
    return render(request, 'store/dashboard/product_form.html', {
        'categories': categories, 'action': 'Add'
    })


@login_required(login_url='/dashboard/login/')
def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        _save_product(request, product)
        messages.success(request, 'Product updated successfully!')
        return redirect('dashboard_products')
    return render(request, 'store/dashboard/product_form.html', {
        'product': product, 'categories': categories, 'action': 'Edit'
    })


def _save_product(request, product=None):
    from django.utils.text import slugify
    data = request.POST
    image = request.FILES.get('image')
    name = data.get('name', '').strip()
    category = get_object_or_404(Category, pk=data.get('category'))
    price = float(data.get('price', 0))
    description = data.get('description', '')
    is_in_stock = data.get('is_in_stock') == 'on'
    is_featured = data.get('is_featured') == 'on'

    # Build specs from dynamic form
    specs = {}
    spec_keys = data.getlist('spec_key')
    spec_vals = data.getlist('spec_val')
    for k, v in zip(spec_keys, spec_vals):
        if k.strip():
            specs[k.strip()] = v.strip()

    if product is None:
        slug = slugify(name)
        base_slug = slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        product = Product(slug=slug)

    product.name = name
    product.category = category
    product.price = price
    product.description = description
    product.is_in_stock = is_in_stock
    product.is_featured = is_featured
    product.specs = specs
    if image:
        product.image = image
    product.save()
    return product


@login_required(login_url='/dashboard/login/')
@require_POST
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('dashboard_products')


@login_required(login_url='/dashboard/login/')
def toggle_stock(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.is_in_stock = not product.is_in_stock
    product.save()
    status = "in stock" if product.is_in_stock else "out of stock"
    messages.success(request, f'"{product.name}" marked as {status}.')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_products'))


@login_required(login_url='/dashboard/login/')
def dashboard_categories(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'store/dashboard/categories.html', {'categories': categories})


@login_required(login_url='/dashboard/login/')
def category_add(request):
    if request.method == 'POST':
        from django.utils.text import slugify
        name = request.POST.get('name', '').strip()
        icon = request.FILES.get('icon')
        order = request.POST.get('order', 0)
        slug = slugify(name)
        base_slug = slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        cat = Category(name=name, slug=slug, order=order)
        if icon:
            cat.icon = icon
        cat.save()
        messages.success(request, f'Category "{name}" created!')
        return redirect('dashboard_categories')
    return render(request, 'store/dashboard/category_form.html')
