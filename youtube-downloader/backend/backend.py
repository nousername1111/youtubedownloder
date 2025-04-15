from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import random

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

cryptos = {
    'BTC': {'price': 65000, 'change': 2.5},
    'ETH': {'price': 3200, 'change': 1.2},
    'BNB': {'price': 420, 'change': -0.6},
    'ADA': {'price': 0.58, 'change': 3.1},
    'SOL': {'price': 180, 'change': 2.0},
    'XRP': {'price': 0.75, 'change': -1.3},
    'DOGE': {'price': 0.12, 'change': 4.5},
}

users = {
    'demo_user': {
        'password': 'demo',
        'portfolio': {
            'BTC': 0.05,
            'ETH': 1.2,
            'ADA': 1000
        },
        'usd_balance': 15000
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/trading')
def trading():
    return render_template('trading.html')

@app.route('/buy-sell')
def buy_sell():
    return render_template('buy_sell.html')

@app.route('/lessons')
def lessons():
    return render_template('lessons.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/prices')
def prices():
    return render_template('prices.html', cryptos=cryptos)

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            return redirect(url_for('home'))
        else:
            return render_template('signin.html', error='Invalid credentials')
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error='Username already exists')
        users[username] = {
            'password': password,
            'portfolio': {},
            'usd_balance': 10000
        }
        return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/api/cryptos')
def get_cryptos():
    for symbol in cryptos:
        change = round(random.uniform(-1, 1), 2)
        cryptos[symbol]['price'] += change
        cryptos[symbol]['change'] = change
    return jsonify(cryptos)

@app.route('/api/user/<username>')
def get_user_data(username):
    user = users.get(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    portfolio_value = 0
    for symbol, amount in user['portfolio'].items():
        portfolio_value += amount * cryptos[symbol]['price']

    return jsonify({
        'portfolio': user['portfolio'],
        'usd_balance': user['usd_balance'],
        'portfolio_value': round(portfolio_value, 2)
    })

@app.route('/api/trade', methods=['POST'])
def trade():
    data = request.json
    username = data['username']
    symbol = data['symbol']
    action = data['action']
    amount_usd = float(data['amount'])

    user = users.get(username)
    if not user or symbol not in cryptos:
        return jsonify({'error': 'Invalid user or symbol'}), 400

    price = cryptos[symbol]['price']
    quantity = amount_usd / price

    if action == 'buy':
        if user['usd_balance'] < amount_usd:
            return jsonify({'error': 'Insufficient USD balance'}), 400
        user['usd_balance'] -= amount_usd
        user['portfolio'][symbol] = user['portfolio'].get(symbol, 0) + quantity
    elif action == 'sell':
        if user['portfolio'].get(symbol, 0) < quantity:
            return jsonify({'error': 'Insufficient crypto balance'}), 400
        user['portfolio'][symbol] -= quantity
        user['usd_balance'] += amount_usd
    else:
        return jsonify({'error': 'Invalid action'}), 400

    return jsonify({'message': f'{action.capitalize()} successful'})

if __name__ == '__main__':
    app.run()
