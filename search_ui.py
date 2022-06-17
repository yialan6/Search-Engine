from flask import Flask, redirect, url_for, render_template, request
import query
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        query = request.form['search']
        return redirect(url_for("results", q=query))

@app.route('/<q>')
def results(q):
    result = query.run(q)

    return render_template("results.html", content=result[0], query = q, time=result[1])
    

if __name__ == "__main__":
    app.run(debug=True)