from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def root():
    return render_template("index.html", current_time=datetime.now(), title="Home Page - 012")


@app.route('/about')
def about():
    return render_template("about.html", current_time=datetime.now(), title="About Page - 012", is_show=False)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", current_time=datetime.now(), title="404 Not Found - 012"), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
