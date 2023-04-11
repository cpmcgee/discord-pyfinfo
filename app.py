import main
from flask import Flask, render_template_string
import threading

app = Flask(__name__)
background_thread = threading.Thread(target=main.start)
background_thread.start()

@app.route("/")
def index():
    return render_template_string('pyfinfo running')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)