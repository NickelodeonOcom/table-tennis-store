from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import gpt4free

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# List of products
products = [
    {"id": 1, "name": "Ping Pong Paddle", "price": 29.99, "image": "/paddle.jpg"},
    {"id": 2, "name": "Table Tennis Balls", "price": 9.99, "image": "/balls.jpg"},
    {"id": 3, "name": "Ping Pong Table", "price": 199.99, "image": "/table.jpg"},
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/products')
def get_products():
    return jsonify(products)

@app.route('/recommendations')
def get_recommendations():
    return jsonify(products[:2])

# Chatbot endpoint using gpt4free
@socketio.on('message')
def handle_message(message):
    # Use gpt4free to get a response
    response = gpt4free.ChatCompletion.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": message}]
    )
    answer = response['choices'][0]['message']['content']
    emit('response', {'message': answer})

if __name__ == '__main__':
    socketio.run(app, debug=True)
