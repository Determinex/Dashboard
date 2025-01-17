from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET']) # GET request
def get_data(): # GET request
    return jsonify({"message": "Hello from Flask!"}) # Return a JSON response

@app.route('/api/data', methods=['POST']) # POST request
def post_data(): # POST request
    data = request.json # Get the data from the POST request
    return jsonify({"received_data": data}) # Return the received data

if __name__ == '__main__':
    app.run(port=5000)