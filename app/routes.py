# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import orion
from .fiware import serialize_store, generate_entity_id

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Get KPI counts
    try:
        stores = len(orion.list_entities('Store'))
        products = len(orion.list_entities('Product'))
        employees = len(orion.list_entities('Employee'))
    except:
        stores = products = employees = 0
    return render_template('home.html', stores=stores, products=products, employees=employees)

@main_bp.route('/products')
def products():
    try:
        products = orion.list_entities('Product')
    except:
        products = []
    return render_template('products.html', products=products)

@main_bp.route('/products/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        # Placeholder for product creation
        flash('Product created (placeholder)')
        return redirect(url_for('main.products'))
    return render_template('product_form.html', product=None)

@main_bp.route('/stores')
def stores():
    try:
        stores = orion.list_entities('Store')
    except:
        stores = []
    return render_template('stores.html', stores=stores)

@main_bp.route('/stores/new', methods=['GET', 'POST'])
def new_store():
    if request.method == 'POST':
        data = request.form.to_dict()
        entity = serialize_store(data)
        try:
            orion.upsert_entity(entity)
            flash('Store created successfully')
            return redirect(url_for('main.stores'))
        except Exception as e:
            flash(f'Error: {e}')
    return render_template('store_form.html', store=None)

@main_bp.route('/employees')
def employees():
    try:
        employees = orion.list_entities('Employee')
    except:
        employees = []
    return render_template('employees.html', employees=employees)

@main_bp.route('/employees/new', methods=['GET', 'POST'])
def new_employee():
    if request.method == 'POST':
        # Placeholder
        flash('Employee created (placeholder)')
        return redirect(url_for('main.employees'))
    return render_template('employee_form.html', employee=None)

@main_bp.route('/stores-map')
def stores_map():
    try:
        stores = orion.list_entities('Store')
    except:
        stores = []
    return render_template('stores_map.html', stores=stores)

# APIs
@main_bp.route('/api/stores/<store_id>/available-shelves')
def available_shelves(store_id):
    # Placeholder
    return jsonify([])

@main_bp.route('/api/shelves/<shelf_id>/available-products')
def available_products(shelf_id):
    # Placeholder
    return jsonify([])

# Purchase
@main_bp.route('/inventory/<id>/buy', methods=['POST'])
def buy_inventory(id):
    # Placeholder
    flash('Purchase completed (placeholder)')
    return redirect(request.referrer or url_for('main.home'))

# Subscription callbacks
@main_bp.route('/subscription/price-change', methods=['POST'])
def price_change_callback():
    # Placeholder
    return '', 200

@main_bp.route('/subscription/low-stock-store001', methods=['POST'])
def low_stock_001():
    return '', 200

# Similar for others
@main_bp.route('/subscription/low-stock-store002', methods=['POST'])
def low_stock_002():
    return '', 200

@main_bp.route('/subscription/low-stock-store003', methods=['POST'])
def low_stock_003():
    return '', 200

@main_bp.route('/subscription/low-stock-store004', methods=['POST'])
def low_stock_004():
    return '', 200