# app/routes.py

from flask import Blueprint, render_template
from app import babel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/products')
def products():
    return render_template('products.html')

@main_bp.route('/stores')
def stores():
    return render_template('stores.html')

@main_bp.route('/employees')
def employees():
    return render_template('employees.html')

@main_bp.route('/stores-map')
def stores_map():
    return render_template('stores_map.html')