from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, generate_latest
import time


REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency in seconds', ['method', 'endpoint'])


app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/ingest', methods=['POST'])
def ingest_data():
    data = request.get_json()  # Get JSON data from mobile
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    json.dump(data, sys.stdout, indent=4)



@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/favicon.ico')
def favicon():
    pass

@app.route("/shutdown")
def shutdown():
    # Send SIGINT to the current process to simulate Ctrl+C
    os.kill(PID, signal.SIGINT)
    return "Server shutting down...", 200


    # This simple instrumentation captures request counts and latencies, giving visibility into the service's
    # performance.

# Start timer
    start_time = time.time()
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    response = cityweather(city)

    duration = time.time() - start_time
    REQUEST_LATENCY.labels(method='GET', endpoint='/').observe(duration)
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=200).inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=400).inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=404).inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=500).inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=503).inc()


    return response

if __name__ == "__main__":
#    metrics = PrometheusMetrics(app)
    app.run(debug=False, host='0.0.0.0', port=8777)
