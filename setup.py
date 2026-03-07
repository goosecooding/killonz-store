#!/usr/bin/env python
"""
KILLONZ Store - One-time setup script
Run this after installing dependencies to set up the database with sample data.

Usage:
    python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'killonz.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product

def run():
    print("🚀 Setting up KILLONZ Store...")

    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@killonz.dz', 'admin123')
        print("✅ Created admin user: admin / admin123")
    else:
        print("ℹ️  Admin user already exists")

    # Create categories
    cats_data = [
        ('CPUs / Processors', 'cpus', 0),
        ('GPUs & Video Cards', 'gpus', 1),
        ('Motherboards', 'motherboards', 2),
        ('Memory / RAM', 'memory', 3),
        ('SSDs & Storage', 'ssds', 4),
        ('Monitors', 'monitors', 5),
        ('Laptops / Notebooks', 'laptops', 6),
        ('Gaming Accessories', 'accessories', 7),
        ('Game Controllers', 'controllers', 8),
        ('PC Cases', 'cases', 9),
        ('Power Supplies', 'power-supplies', 10),
        ('Cooling', 'cooling', 11),
    ]

    cats = {}
    for name, slug, order in cats_data:
        cat, created = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'order': order})
        cats[slug] = cat
        if created:
            print(f"  📁 Created category: {name}")

    # Create sample products
    products_data = [
        # (name, slug, category_slug, price, is_in_stock, is_featured, description, specs)
        ('Intel Core i9-13900K', 'intel-i9-13900k', 'cpus', 89000, True, True,
         'Flagship Intel 13th Gen processor. 24 cores (8P+16E), 5.8GHz boost, perfect for gaming and content creation.',
         {'Cores': '24 (8P+16E)', 'Threads': '32', 'Base Clock': '3.0 GHz', 'Boost Clock': '5.8 GHz', 'TDP': '125W', 'Socket': 'LGA1700', 'Cache': '36MB L3'}),

        ('Intel Core i7-13700K', 'intel-i7-13700k', 'cpus', 62000, True, False,
         'High performance Intel 13th Gen processor for gaming and creative workloads.',
         {'Cores': '16 (8P+8E)', 'Threads': '24', 'Boost Clock': '5.4 GHz', 'Socket': 'LGA1700', 'TDP': '125W'}),

        ('AMD Ryzen 9 7950X', 'amd-ryzen-9-7950x', 'cpus', 95000, True, True,
         'AMD flagship processor with 16 cores and 32 threads. Exceptional for professional workloads.',
         {'Cores': '16', 'Threads': '32', 'Boost Clock': '5.7 GHz', 'Socket': 'AM5', 'TDP': '170W', 'Cache': '64MB L3'}),

        ('AMD Ryzen 5 7600X', 'amd-ryzen-5-7600x', 'cpus', 38000, True, False,
         'Great mid-range AM5 processor for gaming. 6 cores, excellent single-core performance.',
         {'Cores': '6', 'Threads': '12', 'Boost Clock': '5.3 GHz', 'Socket': 'AM5', 'TDP': '105W'}),

        ('NVIDIA RTX 4090 24GB', 'nvidia-rtx-4090', 'gpus', 420000, True, True,
         'The most powerful consumer GPU ever made. 24GB GDDR6X, 4K gaming at max settings, AI acceleration.',
         {'Memory': '24GB GDDR6X', 'Memory Bus': '384-bit', 'CUDA Cores': '16384', 'Boost Clock': '2.52 GHz', 'TDP': '450W', 'Ports': 'HDMI 2.1, 3x DP 1.4'}),

        ('NVIDIA RTX 4080 16GB', 'nvidia-rtx-4080', 'gpus', 295000, True, True,
         'High-end GPU for 4K gaming. 16GB GDDR6X memory, DLSS 3, excellent ray tracing.',
         {'Memory': '16GB GDDR6X', 'Memory Bus': '256-bit', 'CUDA Cores': '9728', 'Boost Clock': '2.51 GHz', 'TDP': '320W'}),

        ('NVIDIA RTX 4070 Ti', 'nvidia-rtx-4070-ti', 'gpus', 195000, True, False,
         'The sweet spot for 1440p and 4K gaming. Great performance per watt.',
         {'Memory': '12GB GDDR6X', 'Memory Bus': '192-bit', 'CUDA Cores': '7680', 'Boost Clock': '2.61 GHz', 'TDP': '285W'}),

        ('AMD RX 7900 XTX', 'amd-rx-7900-xtx', 'gpus', 265000, False, False,
         'AMD flagship GPU with 24GB GDDR6. Incredible 4K gaming performance.',
         {'Memory': '24GB GDDR6', 'Memory Bus': '384-bit', 'Compute Units': '96', 'Boost Clock': '2.5 GHz', 'TDP': '355W'}),

        ('ASUS ROG STRIX Z790-E', 'asus-rog-z790-e', 'motherboards', 78000, True, False,
         'Premium Intel Z790 motherboard. PCIe 5.0, DDR5, WiFi 6E, multiple M.2 slots.',
         {'Socket': 'LGA1700', 'Chipset': 'Z790', 'Memory': 'DDR5, 4 slots, up to 128GB', 'M.2 Slots': '5', 'WiFi': 'WiFi 6E', 'USB': 'USB 3.2 Gen 2x2'}),

        ('MSI MAG B650M Mortar', 'msi-b650m-mortar', 'motherboards', 32000, True, False,
         'Solid mid-range AM5 motherboard. Good VRM, DDR5, WiFi, great value.',
         {'Socket': 'AM5', 'Chipset': 'B650', 'Memory': 'DDR5, 4 slots', 'M.2 Slots': '2', 'WiFi': 'WiFi 6E'}),

        ('Corsair Vengeance DDR5 32GB', 'corsair-vengeance-ddr5-32gb', 'memory', 28000, True, False,
         'High-performance DDR5 kit. 2x16GB, 5600MHz, optimized for Intel and AMD platforms.',
         {'Capacity': '32GB (2x16GB)', 'Type': 'DDR5', 'Speed': '5600MHz', 'CAS Latency': 'CL36', 'Voltage': '1.25V'}),

        ('G.Skill Trident Z5 RGB 64GB', 'gskill-trident-z5-64gb', 'memory', 52000, True, False,
         'Flagship DDR5 kit with RGB lighting. Ultra-fast 6000MHz for maximum performance.',
         {'Capacity': '64GB (2x32GB)', 'Type': 'DDR5', 'Speed': '6000MHz', 'CAS Latency': 'CL30'}),

        ('Samsung 990 Pro 2TB NVMe', 'samsung-990-pro-2tb', 'ssds', 35000, True, False,
         'Top-tier PCIe 4.0 NVMe SSD. Blazing 7450MB/s read speeds, 2TB capacity.',
         {'Capacity': '2TB', 'Interface': 'PCIe 4.0 NVMe', 'Read Speed': '7450 MB/s', 'Write Speed': '6900 MB/s', 'Form Factor': 'M.2 2280'}),

        ('WD Black SN850X 1TB', 'wd-black-sn850x-1tb', 'ssds', 22000, True, False,
         'Gaming-optimized NVMe SSD with predictive loading technology.',
         {'Capacity': '1TB', 'Interface': 'PCIe 4.0 NVMe', 'Read Speed': '7300 MB/s', 'Write Speed': '6300 MB/s'}),

        ('LG 27GP850-B 27" 180Hz', 'lg-27gp850-27-180hz', 'monitors', 65000, True, True,
         '27-inch QHD gaming monitor. 2560x1440, 180Hz, 1ms GtG, Nano IPS panel.',
         {'Size': '27 inch', 'Resolution': '2560x1440 (QHD)', 'Refresh Rate': '180Hz', 'Response Time': '1ms GtG', 'Panel': 'Nano IPS', 'HDR': 'HDR400'}),

        ('Samsung 32" Odyssey G7', 'samsung-32-odyssey-g7', 'monitors', 95000, False, False,
         '32-inch curved QHD gaming monitor. 240Hz, 1000R curve, QLED.',
         {'Size': '32 inch', 'Resolution': '2560x1440', 'Refresh Rate': '240Hz', 'Curvature': '1000R', 'Panel': 'QLED VA'}),

        ('ASUS ROG Zephyrus G14', 'asus-rog-zephyrus-g14', 'laptops', 245000, True, True,
         'Compact 14-inch gaming laptop. AMD Ryzen 9 + RTX 4060, incredible portability and performance.',
         {'CPU': 'AMD Ryzen 9 7940HS', 'GPU': 'NVIDIA RTX 4060 8GB', 'RAM': '16GB DDR5', 'Storage': '1TB NVMe', 'Display': '14" 2560x1600 165Hz', 'Battery': '76Wh'}),

        ('Lenovo Legion 5 Pro', 'lenovo-legion-5-pro', 'laptops', 195000, True, False,
         '16-inch gaming beast. Ryzen 7 + RTX 4070, stunning 165Hz QHD display.',
         {'CPU': 'AMD Ryzen 7 7745HX', 'GPU': 'NVIDIA RTX 4070 8GB', 'RAM': '16GB DDR5', 'Storage': '512GB NVMe', 'Display': '16" 2560x1600 165Hz'}),

        ('Logitech G Pro X Superlight 2', 'logitech-g-pro-x-superlight-2', 'accessories', 22000, True, False,
         'Ultra-lightweight wireless gaming mouse. 60g, HERO 2 sensor, 95 hours battery.',
         {'Weight': '60g', 'Sensor': 'HERO 2', 'DPI': 'Up to 32000', 'Connectivity': 'Wireless 2.4GHz', 'Battery': '95 hours', 'Buttons': '5'}),

        ('HyperX Alloy FPS Pro', 'hyperx-alloy-fps-pro', 'accessories', 14000, True, False,
         'Compact tenkeyless mechanical keyboard for gaming. Cherry MX switches, RGB.',
         {'Switches': 'Cherry MX Red', 'Layout': 'Tenkeyless', 'RGB': 'Yes', 'Connection': 'USB', 'Backlighting': 'Red LED'}),

        ('Sony DualSense PS5 Controller', 'sony-dualsense-ps5', 'controllers', 16000, True, False,
         'Official PS5 controller. Haptic feedback, adaptive triggers, 12 hours battery.',
         {'Compatibility': 'PS5, PC', 'Battery': '12 hours', 'Connectivity': 'Bluetooth 5.1 / USB-C', 'Vibration': 'Haptic feedback', 'Triggers': 'Adaptive'}),

        ('Xbox Series X Controller', 'xbox-series-x-controller', 'controllers', 12000, True, False,
         'Official Xbox wireless controller. Works with Xbox and PC.',
         {'Compatibility': 'Xbox Series X/S, PC', 'Battery': 'AA batteries / USB-C', 'Connectivity': 'Bluetooth / USB', 'Bumpers': 'Textured grip'}),

        ('PS5 DualSense Edge', 'ps5-dualsense-edge', 'controllers', 32000, False, False,
         'Pro PS5 controller with customizable buttons, swappable sticks and paddles.',
         {'Compatibility': 'PS5, PC', 'Back Buttons': '2 swappable', 'Sticks': 'Swappable', 'Trigger': 'Adjustable travel', 'Battery': '40Wh'}),

        ('NZXT H510 Flow', 'nzxt-h510-flow', 'cases', 18000, True, False,
         'Mid-tower ATX case with mesh front panel for excellent airflow.',
         {'Form Factor': 'Mid-Tower', 'Motherboard': 'ATX, mATX, ITX', 'Drive Bays': '2x 2.5", 2x 3.5"', 'Fan Support': 'Up to 6 fans', 'Window': 'Tempered Glass'}),

        ('Corsair RM850x 850W', 'corsair-rm850x-850w', 'power-supplies', 26000, True, False,
         'Fully modular 850W PSU. 80+ Gold certified, zero RPM mode.',
         {'Wattage': '850W', 'Efficiency': '80+ Gold', 'Modular': 'Fully Modular', 'Fan': '135mm', 'Warranty': '10 years'}),

        ('Noctua NH-D15 CPU Cooler', 'noctua-nh-d15', 'cooling', 19000, True, False,
         'Premium dual-tower CPU cooler. Extremely quiet and powerful, industry-leading thermal performance.',
         {'Type': 'Air Cooler', 'Height': '165mm', 'Fans': '2x 140mm NF-A15', 'Noise': '24.6 dB(A)', 'TDP': '250W+', 'Socket': 'AM4/AM5/LGA1700+'}),
    ]

    created_count = 0
    for name, slug, cat_slug, price, in_stock, featured, desc, specs in products_data:
        if not Product.objects.filter(slug=slug).exists():
            Product.objects.create(
                name=name, slug=slug,
                category=cats[cat_slug],
                price=price, is_in_stock=in_stock,
                is_featured=featured,
                description=desc, specs=specs
            )
            created_count += 1

    print(f"✅ Created {created_count} sample products")

    print()
    print("=" * 50)
    print("✅ SETUP COMPLETE!")
    print("=" * 50)
    print()
    print("Run the server:")
    print("  python manage.py runserver")
    print()
    print("Store:     http://127.0.0.1:8000/")
    print("Dashboard: http://127.0.0.1:8000/dashboard/")
    print("Login:     admin / admin123")
    print()
    print("⚠️  IMPORTANT: Change the admin password before going live!")

if __name__ == '__main__':
    run()
