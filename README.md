# KILLONZ Store — Django Backend

A full e-commerce store for PC components with owner dashboard.

## Features

**Store Frontend:**
- Homepage with hero slider + category grid + product listings
- Category pages with sidebar navigation and search
- Product detail pages with specs table, quantity selector
- Shopping cart (session-based, no login needed)
- Checkout form (name, phone, email, wilaya) — cash on delivery
- Order confirmation page

**Owner Dashboard:**
- Secure login (staff account required)
- Overview stats: orders, revenue, stock alerts
- Order management — view all orders, update status (Pending → Confirmed → Delivered)
- Product management — add, edit, delete, toggle stock on/off
- Category management — add categories with icons
- Products added in dashboard instantly appear in the store

## Quick Setup

### 1. Install Python (3.10+)
Download from https://python.org

### 2. Install dependencies
```bash
cd killonz_store
pip install -r requirements.txt
```

### 3. Set up the database
```bash
python manage.py migrate
```

### 4. Run setup script (creates admin + sample products)
```bash
python setup.py
```

### 5. Copy your images
- Put your product images in: `media/products/`
- Put category icons in: `media/categories/`
- Put logo in: `store/static/store/images/logo.png`
- Copy GPU images from your original project to: `store/static/store/images/`
  - `rtx5080.webp`, `rtx4090.jpg`, `rtx4080.webp`, `nvidia-logo.png`

### 6. Start the server
```bash
python manage.py runserver
```

### 7. Open in browser
- **Store:** http://127.0.0.1:8000/
- **Dashboard:** http://127.0.0.1:8000/dashboard/
- **Django Admin:** http://127.0.0.1:8000/admin/

**Login credentials:** `admin` / `admin123`

> ⚠️ Change the password before going live!

---

## Adding Products (Dashboard)

1. Go to http://127.0.0.1:8000/dashboard/
2. Click **"Add Product"** in the sidebar
3. Fill in name, category, price, description
4. Upload a product image
5. Add specifications (RAM, Storage, etc.)
6. Check "Featured" to show on homepage
7. Save — product appears instantly in store

## Managing Orders

1. Go to Dashboard → Orders
2. Click any order to see full details
3. Change status: Pending → Confirmed → Delivered
4. Customer phone number is shown for easy calling

## Toggling Stock

From Dashboard → Products:
- Click the green **"In Stock"** badge to mark as Out of Stock
- Click the red **"Out of Stock"** badge to mark as In Stock

Changes take effect immediately on the store.

---

## Project Structure

```
killonz_store/
├── killonz/              # Django project settings
│   ├── settings.py
│   └── urls.py
├── store/                # Main app
│   ├── models.py         # Category, Product, Order, OrderItem
│   ├── views.py          # All views (store + dashboard)
│   ├── urls.py           # URL routing
│   ├── admin.py          # Django admin config
│   ├── templates/
│   │   └── store/
│   │       ├── base.html           # Base template (navbar + footer)
│   │       ├── home.html           # Homepage
│   │       ├── category.html       # Category page
│   │       ├── product_detail.html # Product page
│   │       ├── cart.html           # Shopping cart
│   │       ├── checkout.html       # Order form
│   │       ├── order_success.html  # Order confirmation
│   │       ├── partials/
│   │       │   └── product_card.html
│   │       └── dashboard/
│   │           ├── base.html       # Dashboard layout
│   │           ├── login.html
│   │           ├── index.html      # Overview
│   │           ├── orders.html
│   │           ├── order_detail.html
│   │           ├── products.html
│   │           ├── product_form.html
│   │           ├── categories.html
│   │           └── category_form.html
│   └── static/
│       └── store/
│           └── images/             # Static images
├── media/                          # Uploaded product/category images
├── requirements.txt
├── setup.py                        # One-time setup script
└── manage.py
```

## Deployment Notes

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Change `SECRET_KEY` to a random string
3. Set `ALLOWED_HOSTS` to your domain
4. Run `python manage.py collectstatic`
5. Use a proper web server (Nginx + Gunicorn)
6. Use PostgreSQL instead of SQLite
