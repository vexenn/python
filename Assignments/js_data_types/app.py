from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # debug=True allows the server to auto-reload when you save changes
    app.run(debug=True)