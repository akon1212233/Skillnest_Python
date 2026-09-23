from flask import Flask,render_template,redirect,request

app = Flask(__name__)

productsVar = []


@app.route("/")
def index():
    return render_template("registro.html")


@app.route("/registrar", methods=["POST"])
def createProduct():
    productName = request.form["productName"]
    price = request.form["price"]
    category = request.form["category"]

    print(f"""
    =========================
    Nombre   : {productName}
    Precio   : {price}
    Categoria: {category}
    =========================""")

    productsVar.append({
        "name":productName,
        "price":price,
        "category":category
    })

    return redirect("/resultado")


@app.route("/resultado")
def products():
    return render_template("resultado.html",products=products)

@app.route("/ayuda")
def help():
    return render_template("ayuda.html")

if __name__ == "__main__":
    app.run(debug=True)