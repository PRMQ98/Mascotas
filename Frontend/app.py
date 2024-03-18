from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=3030)
