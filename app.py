from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from g4f.client import Client  # Import Client from g4f

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Initialize g4f client
client = Client()

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

# Chatbot endpoint using g4f client
@socketio.on('message')
def handle_message(message):
    try:
        # Use g4f client to get a response
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini as specified
            messages=[{"role": "user", "content": message}],
            web_search=False  # Set web_search to False for a simple chat response
        )
        
        # Extract the chatbot's response from the API response
        answer = response.choices[0].message.content

        # Emit the response back to the client (frontend)
        emit('response', {'message': answer})

    except Exception as e:
        emit('response', {'message': f"Error: {str(e)}"})

if __name__ == '__main__':
    socketio.run(app, debug=True)

