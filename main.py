from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users_db = {
    'admin': 'password123',
    'user1': '123456'
}

items = [
    {'id': 1, 'name': 'Ноутбук', 'price': 25000, 'category': 'Електроніка'},
    {'id': 2, 'name': 'Книга', 'price': 300, 'category': 'Література'},
    {'id': 3, 'name': 'Кава', 'price': 150, 'category': 'Продукти'}
]

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.now()

@app.route('/')
def home():
    return render_template('index.html', title='Головна', current_time=datetime.now())

@app.route('/about')
def about():
    return '<h1>Про нас</h1><p>Це проста сторінка на Flask</p>'

@app.route('/items')
def show_items():
    category = request.args.get('category')
    filtered_items = items
    if category:
        filtered_items = [item for item in items if item['category'] == category]
    return render_template('items.html', items=filtered_items, category=category)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return render_template('item_detail.html', item=item)
    return 'Товар не знайдено', 404

@app.route('/api/items', methods=['GET'])
def api_items():
    return jsonify(items)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def api_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({'error': 'Not found'}), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if users_db.get(username) == password:
            session['username'] = username
            flash('Ви успішно увійшли в систему!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Невірний логін або пароль', 'error')

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = User(session['username'], f"{session['username']}@example.com")
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('home'))

@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_item = {
            'id': len(items) + 1,
            'name': request.form.get('name'),
            'price': float(request.form.get('price')),
            'category': request.form.get('category')
        }
        items.append(new_item)
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('show_items'))

    return render_template('add_item.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.context_processor
def inject_user():
    return {'current_user': session.get('username')}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
