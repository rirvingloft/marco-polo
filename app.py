from flask import Flask, request, jsonify, Response
import json
import requests
import os
import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG)

app = Flask(__name__)

# Fetch service names from environment variables, with default values
SERVICE2_URL = os.environ.get("SERVICE2_URL", "http://localhost:5000/marco")
SERVICE3_URL = os.environ.get("SERVICE3_URL", "http://localhost:5000/marco")
HOSTNAME     = os.environ.get("HOSTNAME",     "localhost")

@app.route('/marco', methods=['GET','POST'])
def marco():
    app.logger.debug('issue contacting svc2 : %s', HOSTNAME)
    
    try:

        svc2_response = requests.get(SERVICE2_URL, timeout=5)
        svc2_json = svc2_response.json() if svc2_response.status_code == 200 else { 
            app.logger.debug('issue contacting svc2 : %s', svc2_response.status_code)
        }

        svc3_response = requests.get(SERVICE3_URL, timeout=5)
        svc3_json = svc3_response.json() if svc3_response.status_code == 200 else {
            app.logger.debug('issue contacting svc3 : %s', svc3_response.status_code)
        }

        payload = {
         'service2_json response': svc2_json,
         'service3_json response': svc3_json
        }
        pretty_payload = json.dumps(payload, indent=2)


    except requests.exceptions.RequestException as e:
        print(f"Error sending Marco: {e}")
        return jsonify({"error": "Failed to contact other services"}), 500
    
    return Response(pretty_payload, mimetype='application/json')




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
    
    payload =  { 
                  "status": "healthy", 
                  "hostname": HOSTNAME
    }
    pretty_payload = json.dumps(payload, indent=2)
    return Response(pretty_payload, mimetype='application/json')




if __name__ == '__main__':
    # Use an environment variable to set the port, with a default of 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

