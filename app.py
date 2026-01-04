import time
from flask import request
from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.teardown_request
def log_request(error=None):
    if hasattr(request, "start_time"):
        duration = time.time() - request.start_time
        print(
            f"REQUEST {request.method} {request.path} "
            f"STATUS {'500' if error else '200'} "
            f"DURATION {round(duration, 3)}s"
        )



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
    fail_mode = os.getenv("FAIL_MODE")
    print(f"FAIL_MODE value: {fail_mode}")

    if fail_mode and fail_mode.strip().lower() == "true":
        raise Exception("Simulated production failure")

    return jsonify(
        message="No errors detected",
        fail_mode=fail_mode
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
