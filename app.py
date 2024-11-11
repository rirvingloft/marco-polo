from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Fetch service names from environment variables, with default values
SERVICE2_URL = os.environ.get("SERVICE2_URL", "http://service2:5000/marco")
SERVICE3_URL = os.environ.get("SERVICE3_URL", "http://service3:5000/marco")
HOSTNAME     = os.environ.get("HOSTNAME",     "marco-polo-service")

@app.route('/marco', methods=['POST'])
def marco():
    print("Received 'Marco'")
    
    try:

        svc2_response = requests.post(SERVICE2_URL, timeout=5)
        svc2_json = svc2_response.json() if svc2_response.status_code == 200 else {}
        print(f"Service2 response: {svc2_json}")

        svc3_response = requests.post(SERVICE3_URL, timeout=5)
        svc3_json = svc3_response.json() if svc3_response.status_code == 200 else {}
        print(f"Service3 response: {svc3_json}")

        response = {
         "answer": "POLO!", "service2_response": svc2_json, "service3_response": svc3_json
        }

    except requests.exceptions.RequestException as e:
        print(f"Error sending Marco: {e}")
        return jsonify({"error": "Failed to contact other services"}), 500
    
    return jsonify(response), 200



@app.route('/polo', methods=['GET'])
def polo():
    polo_response =  { "answer": "POLO!",  "hostname": HOSTNAME }
    return app.response_class(
        response=jsonify(polo_response).get_data(as_text=True),
        mimetype='application/json',
        status=200,
        direct_passthrough=True
    )



# Health check route
@app.route('/health', methods=['GET'])
def health():
    response =  { 
                  "status": "healthy", 
                  "hostname": HOSTNAME
    }
    return app.response_class(
        response=jsonify(response).get_data(as_text=True),
        mimetype='application/json',
        status=200,
        direct_passthrough=True
    )



if __name__ == '__main__':
    # Use an environment variable to set the port, with a default of 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

