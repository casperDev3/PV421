from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Product

main_bp = Blueprint('main', __name__)

# Головна сторінка
@main_bp.route('/')
def index():
    return render_template('index.html')

# ========== CRUD для продуктів ==========

# Список продуктів
@main_bp.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

# API endpoint для отримання продуктів у JSON
@main_bp.route('/api/products')
def api_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

# Створення продукту
@main_bp.route('/products/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form['name'],
                description=request.form.get('description', ''),
                price=float(request.form['price']),
                quantity=int(request.form['quantity'])
            )
            db.session.add(product)
            db.session.commit()
            flash('Продукт успішно створено!', 'success')
            return redirect(url_for('main.list_products'))
        except Exception as e:
            flash(f'Помилка: {str(e)}', 'danger')

    return render_template('products/create.html')

# Перегляд одного продукту
@main_bp.route('/products/<int:id>')
def view_product(id):
    product = Product.query.get_or_404(id)
    return render_template('products/view.html', product=product)

@main_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            product.name = request.form['name']
            product.description = request.form.get('description', '')
            product.price = float(request.form['price'])
            product.quantity = int(request.form['quantity'])
            db.session.commit()
            flash('Продукт успішно оновлено!', 'success')
            return redirect(url_for('main.view_product', id=product.id))
        except Exception as e:
            flash(f'Помилка: {str(e)}', 'danger')

    return render_template('products/edit.html', product=product)

@main_bp.route('/products/<int:id>/delete', methods=['DELETE', 'POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Продукт успішно видалено!', 'success')
        if request.method == 'DELETE':
            return jsonify({'message': 'Product deleted'}), 200
        return redirect(url_for('main.list_products'))
    except Exception as e:
        flash(f'Помилка: {str(e)}', 'danger')
        if request.method == 'DELETE':
            return jsonify({'error': str(e)}), 500
        return redirect(url_for('main.list_products'))


# not found page
@main_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
