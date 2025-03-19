from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import gpt4free  # Ensure you are using the correct gpt4free package

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
    try:
        # Initialize the GPT-4 client from gpt4free
        client = gpt4free.Client()

        # Use the gpt4free client to get a response (adjust this as per gpt4free API usage)
        response = client.chat(message)

        # Extract the chatbot's response
        answer = response['choices'][0]['message']['content']

        # Emit the response back to the client
        emit('response', {'message': answer})
    except Exception as e:
        emit('response', {'message': f"Error: {str(e)}"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
