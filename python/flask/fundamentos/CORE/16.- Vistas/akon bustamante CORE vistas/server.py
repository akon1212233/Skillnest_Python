from flask import Flask, redirect,render_template,request,session,url_for

app = Flask(__name__)
app.secret_key = "SeCrEt_kEy"

@app.route("/")
def index():
    if "views" in session:
        session["views"] +=1
    else:
        session["views"] = 1
    if "resets" not in session:
        session["resets"] = 0
    return render_template("views.html",views=session["views"],resets=session["resets"])

@app.route("/addTwoView")
def addTwoView():
    if "views" not in session:
        session["views"] = 0
    session["views"] += 2
    return redirect(url_for('index'))

@app.route("/reset")
def reset():
    if "views" not in session:
        session["resets"] = 0
    session["resets"] += 1
    session["views"] = 0
    return redirect(url_for('index'))

@app.route("/add", methods=["POST"])
def add():
    amount = int(request.form["amount"])
    if "views" not in session:
        session["views"] = 0
    session["views"] += (amount - 1)
    return redirect(url_for('index'))

@app.route("/destroySession")
def destroySession():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":

    app.run(debug=True)