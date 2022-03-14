import os
import threading

from flask import Flask

app = Flask("")


@app.route("/")
def main():
    return "a"


def run():
    app.run(host="0.0.0.0", port=8080)


server = None


def keep_alive():
    return
    try:
        global server
        server = threading.Thread(target=run, daemon=True)
        server.start()
    except KeyboardInterrupt:
        print("\nInterrupted")
        server.join()
        exit()
