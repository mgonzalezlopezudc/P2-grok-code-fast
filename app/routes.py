# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from .fiware import serialize_store, serialize_product, serialize_employee, generate_entity_id

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Get KPI counts
    try:
        stores = len(current_app.orion_client.list_entities('Store'))
        products = len(current_app.orion_client.list_entities('Product'))
        employees = len(current_app.orion_client.list_entities('Employee'))
    except:
        stores = products = employees = 0
    return render_template('home.html', stores=stores, products=products, employees=employees)

@main_bp.route('/products')
def products():
    try:
        products = current_app.orion_client.list_entities('Product')
    except:
        products = []
    return render_template('products.html', products=products)

@main_bp.route('/products/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        data = request.form.to_dict()
        entity = serialize_product(data)
        try:
            current_app.orion_client.upsert_entity(entity)
            flash('Product created successfully')
            return redirect(url_for('main.products'))
        except Exception as e:
            flash(f'Error: {e}')
    return render_template('product_form.html', product=None)

@main_bp.route('/products/<id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    if request.method == 'POST':
        data = request.form.to_dict()
        data['id'] = id
        entity = serialize_product(data)
        try:
            current_app.orion_client.upsert_entity(entity)
            flash('Product updated successfully')
            return redirect(url_for('main.products'))
        except Exception as e:
            flash(f'Error: {e}')
    try:
        product = current_app.orion_client.get_entity(id)
    except:
        flash('Product not found')
        return redirect(url_for('main.products'))
    return render_template('product_form.html', product=product)

@main_bp.route('/products/<id>/delete', methods=['POST'])
def delete_product(id):
    try:
        current_app.orion_client.delete_entity(id)
        flash('Product deleted successfully')
    except Exception as e:
        flash(f'Error: {e}')
    return redirect(url_for('main.products'))

@main_bp.route('/products/<id>')
def product_detail(id):
    try:
        product = current_app.orion_client.get_entity(id)
        inventory = current_app.orion_client.list_entities('InventoryItem')
        stores = current_app.orion_client.list_entities('Store')
        shelves = current_app.orion_client.list_entities('Shelf')
        # Group inventory by store
        inventory_by_store = {}
        for inv in inventory:
            if inv.get('refProduct') == id:
                store_id = inv.get('refStore')
                if store_id not in inventory_by_store:
                    inventory_by_store[store_id] = []
                inventory_by_store[store_id].append(inv)
        return render_template('product_detail.html', product=product, inventory_by_store=inventory_by_store, stores=stores, shelves=shelves)
    except:
        flash('Product not found')
        return redirect(url_for('main.products'))

@main_bp.route('/products/<product_id>/add-inventory/<store_id>', methods=['POST'])
def add_inventory(product_id, store_id):
    data = request.form.to_dict()
    shelf_id = data['shelf_id']
    stock_count = int(data['stock_count'])
    entity = {
        "id": generate_entity_id('InventoryItem'),
        "type": "InventoryItem",
        "refProduct": {"type": "Relationship", "value": product_id},
        "refStore": {"type": "Relationship", "value": store_id},
        "refShelf": {"type": "Relationship", "value": shelf_id},
        "stockCount": {"type": "Integer", "value": stock_count},
        "shelfCount": {"type": "Integer", "value": stock_count}
    }
    try:
        current_app.orion_client.upsert_entity(entity)
        flash('Inventory added successfully')
    except Exception as e:
        flash(f'Error: {e}')
    return redirect(url_for('main.product_detail', id=product_id))

@main_bp.route('/stores')
def stores():
    try:
        stores = current_app.orion_client.list_entities('Store')
    except:
        stores = []
    return render_template('stores.html', stores=stores)

@main_bp.route('/stores/<id>')
def store_detail(id):
    try:
        store = current_app.orion_client.get_entity(id)
        inventory = current_app.orion_client.list_entities('InventoryItem')
        products = current_app.orion_client.list_entities('Product')
        shelves = current_app.orion_client.list_entities('Shelf')
        # Group inventory by shelf
        inventory_by_shelf = {}
        for inv in inventory:
            if inv.get('refStore') == id:
                shelf_id = inv.get('refShelf')
                if shelf_id not in inventory_by_shelf:
                    inventory_by_shelf[shelf_id] = []
                inventory_by_shelf[shelf_id].append(inv)
        return render_template('store_detail.html', store=store, inventory_by_shelf=inventory_by_shelf, products=products, shelves=shelves)
    except:
        flash('Store not found')
        return redirect(url_for('main.stores'))

@main_bp.route('/stores/new', methods=['GET', 'POST'])
def new_store():
    if request.method == 'POST':
        data = request.form.to_dict()
        entity = serialize_store(data)
        try:
            current_app.orion_client.upsert_entity(entity)
            flash('Store created successfully')
            return redirect(url_for('main.stores'))
        except Exception as e:
            flash(f'Error: {e}')
    return render_template('store_form.html', store=None)

@main_bp.route('/stores/<id>/edit', methods=['GET', 'POST'])
def edit_store(id):
    if request.method == 'POST':
        data = request.form.to_dict()
        data['id'] = id
        entity = serialize_store(data)
        try:
            current_app.orion_client.upsert_entity(entity)
            flash('Store updated successfully')
            return redirect(url_for('main.stores'))
        except Exception as e:
            flash(f'Error: {e}')
    try:
        store = current_app.orion_client.get_entity(id)
    except:
        flash('Store not found')
        return redirect(url_for('main.stores'))
    return render_template('store_form.html', store=store)

@main_bp.route('/stores/<id>/delete', methods=['POST'])
def delete_store(id):
    try:
        current_app.orion_client.delete_entity(id)
        flash('Store deleted successfully')
    except Exception as e:
        flash(f'Error: {e}')
    return redirect(url_for('main.stores'))

@main_bp.route('/employees')
def employees():
    try:
        employees = current_app.orion_client.list_entities('Employee')
    except:
        employees = []
    return render_template('employees.html', employees=employees)

@main_bp.route('/employees/new', methods=['GET', 'POST'])
def new_employee():
    if request.method == 'POST':
        data = request.form.to_dict()
        entity = serialize_employee(data)
        try:
            current_app.orion_client.upsert_entity(entity)
            flash('Employee created successfully')
            return redirect(url_for('main.employees'))
        except Exception as e:
            flash(f'Error: {e}')
    stores = current_app.orion_client.list_entities('Store')
    return render_template('employee_form.html', employee=None, stores=stores)

@main_bp.route('/employees/<id>/edit', methods=['GET', 'POST'])
def edit_employee(id):
    if request.method == 'POST':
        data = request.form.to_dict()
        data['id'] = id
        entity = serialize_employee(data)
        try:
            current_app.orion_client.upsert_entity(entity)
            flash('Employee updated successfully')
            return redirect(url_for('main.employees'))
        except Exception as e:
            flash(f'Error: {e}')
    try:
        employee = current_app.orion_client.get_entity(id)
    except:
        flash('Employee not found')
        return redirect(url_for('main.employees'))
    stores = current_app.orion_client.list_entities('Store')
    return render_template('employee_form.html', employee=employee, stores=stores)

@main_bp.route('/employees/<id>/delete', methods=['POST'])
def delete_employee(id):
    try:
        current_app.orion_client.delete_entity(id)
        flash('Employee deleted successfully')
    except Exception as e:
        flash(f'Error: {e}')
    return redirect(url_for('main.employees'))

@main_bp.route('/stores-map')
def stores_map():
    try:
        stores = current_app.orion_client.list_entities('Store')
    except:
        stores = []
    return render_template('stores_map.html', stores=stores)

# APIs
@main_bp.route('/api/stores/<store_id>/available-shelves')
def available_shelves(store_id):
    try:
        shelves = current_app.orion_client.list_entities('Shelf')
        inventory = current_app.orion_client.list_entities('InventoryItem')
        # Available shelves: those in store with maxCapacity > current inventory
        available = []
        for shelf in shelves:
            if shelf.get('refStore') == store_id:
                shelf_id = shelf['id']
                current_count = sum(1 for inv in inventory if inv.get('refShelf') == shelf_id)
                if current_count < shelf.get('maxCapacity', 0):
                    available.append(shelf)
        return jsonify(available)
    except:
        return jsonify([])

@main_bp.route('/api/shelves/<shelf_id>/available-products')
def available_products(shelf_id):
    try:
        products = current_app.orion_client.list_entities('Product')
        inventory = current_app.orion_client.list_entities('InventoryItem')
        # Available products: those not already on this shelf
        assigned_products = {inv['refProduct'] for inv in inventory if inv.get('refShelf') == shelf_id}
        available = [p for p in products if p['id'] not in assigned_products]
        return jsonify(available)
    except:
        return jsonify([])

# Purchase
@main_bp.route('/inventory/<id>/buy', methods=['POST'])
def buy_inventory(id):
    try:
        inv = current_app.orion_client.get_entity(id)
        if inv['shelfCount'] <= 0:
            flash('Out of stock')
            return redirect(request.referrer or url_for('main.home'))
        # Decrement shelfCount and stockCount
        attrs = {
            "shelfCount": {"type": "Integer", "value": inv['shelfCount'] - 1},
            "stockCount": {"type": "Integer", "value": inv['stockCount'] - 1}
        }
        current_app.orion_client.update_entity_attrs(id, attrs)
        flash('Purchase successful')
    except Exception as e:
        flash(f'Error: {e}')
    return redirect(request.referrer or url_for('main.home'))

# Subscription callbacks
@main_bp.route('/subscription/price-change', methods=['POST'])
def price_change_callback():
    data = request.get_json()
    # Normalize and emit
    from app import socketio
    socketio.emit('price_change', data)
    return '', 200

@main_bp.route('/subscription/low-stock-store001', methods=['POST'])
def low_stock_001():
    data = request.get_json()
    from app import socketio
    socketio.emit('low_stock_001', data)
    return '', 200

# Similar for others
@main_bp.route('/subscription/low-stock-store002', methods=['POST'])
def low_stock_002():
    data = request.get_json()
    from app import socketio
    socketio.emit('low_stock_002', data)
    return '', 200

@main_bp.route('/subscription/low-stock-store003', methods=['POST'])
def low_stock_003():
    data = request.get_json()
    from app import socketio
    socketio.emit('low_stock_003', data)
    return '', 200

@main_bp.route('/set-language', methods=['POST'])
def set_language():
    from flask import session
    lang = request.form.get('lang', 'es')
    session['lang'] = lang
    return redirect(request.referrer or url_for('main.home'))