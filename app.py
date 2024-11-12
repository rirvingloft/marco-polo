from flask import Flask, request, jsonify
import requests
import os
import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG)

app = Flask(__name__)

# Fetch service names from environment variables, with default values
SERVICE2_URL = os.environ.get("SERVICE2_URL", "http://service2:5000/marco")
SERVICE3_URL = os.environ.get("SERVICE3_URL", "http://service3:5000/marco")
HOSTNAME     = os.environ.get("HOSTNAME",     "marco-polo-service")

@app.route('/marco', methods=['POST'])
def marco():
    app.logger.debug('issue contacting svc2 : %s', HOSTNAME)
    
    try:

        svc2_response = requests.post(SERVICE2_URL, timeout=5)
        svc2_json = svc2_response.json() if svc2_response.status_code == 200 else { 
            app.logger.debug('issue contacting svc2 : %s', svc2_response.status_code)
        }

        svc3_response = requests.post(SERVICE3_URL, timeout=5)
        svc3_json = svc3_response.json() if svc3_response.status_code == 200 else {
            app.logger.debug('issue contacting svc3 : %s', svc3_response.status_code)
        }

        response = {
         "answer": "POLO!", "service2_response": svc2_response.status_code, "service3_response": svc3_response.status_code
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
    app.logger.info('health check requested for : %s', HOSTNAME)
    
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

