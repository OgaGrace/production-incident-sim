import time
import os
import logging
from flask import Flask, request, jsonify

# -----------------------
# Logging configuration
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------
# Flask app
# -----------------------
app = Flask(__name__)

# -----------------------
# Request timing
# -----------------------
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    duration = time.time() - request.start_time
    logger.info(
        f"REQUEST {request.method} {request.path} "
        f"STATUS {response.status_code} "
        f"DURATION {round(duration, 3)}s"
    )
    return response

# -----------------------
# Routes
# -----------------------
@app.route("/")
def health():
    return jsonify(
        status="ok",
        service="incident-sim-api"
    )

@app.route("/slow")
def slow():
    time.sleep(5)
    return jsonify(message="This response was slow")

@app.route("/error")
def error():
    fail_mode = os.getenv("FAIL_MODE", "false")

    if fail_mode.strip().lower() == "true":
        raise Exception("Simulated production failure")

    return jsonify(
        message="No errors detected",
        fail_mode=fail_mode
    )

# -----------------------
# Entrypoint
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
