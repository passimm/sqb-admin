from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		return render_template('hello.html', username = request.form['username'])
	else:
		return render_template('hello.html')

if __name__ == '__main__':
    app.run(debug=True)