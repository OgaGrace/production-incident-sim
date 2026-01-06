import time
import os
import logging
import requests
from flask import Flask, jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    duration = time.time() - request.start_time
    logger.info(
        f"{request.method} {request.path} "
        f"STATUS={response.status_code} "
        f"DURATION={round(duration, 3)}s"
    )
    return response


@app.route("/")
def health():
    return jsonify(status="ok", service="incident-sim-api")


@app.route("/slow")
def slow():
    time.sleep(5)
    return jsonify(message="This response was slow")


@app.route("/error")
def error():
    fail_mode = os.getenv("FAIL_MODE")

    if fail_mode and fail_mode.strip().lower() == "true":
        raise Exception("Simulated production failure")

    return jsonify(message="No errors detected", fail_mode=fail_mode)


@app.route("/downstream")
def downstream():
    time.sleep(8)
    return jsonify(message="Downstream service response")


@app.route("/aggregate")
def aggregate():
    start = time.time()
    r = requests.get("http://127.0.0.1:5000/downstream")
    downstream_time = time.time() - start

    return jsonify(
        message="Aggregate response",
        downstream_status=r.status_code,
        downstream_time=round(downstream_time, 2)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
