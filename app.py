from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

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
    print(f"FAIL_MODE value at runtime: {fail_mode}")

    if fail_mode == "true":
        raise Exception("Simulated production failure")

    return jsonify(
        message="No errors detected",
        fail_mode=fail_mode
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
