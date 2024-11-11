from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Fetch service names from environment variables, with default values
SERVICE2_URL = os.environ.get("SERVICE2_URL", "http://service2:5000/marco")
SERVICE3_URL = os.environ.get("SERVICE3_URL", "http://service3:5000/marco")

@app.route('/marco', methods=['POST'])
def marco():
    print("Received 'Marco'")
    response = jsonify(message="Polo")
    
    try:
        requests.post(SERVICE2_URL, json={}, timeout=5)
        requests.post(SERVICE3_URL, json={}, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Error sending Marco: {e}")
        return jsonify({"error": "Failed to contact other services"}), 500
    
    return response

# Health check route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Use an environment variable to set the port, with a default of 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

