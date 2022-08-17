from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.cookie_order_model import CookieOrders


@app.route("/")
def index():
    orders = CookieOrders.getOrders()

    return render_template("cookie_orders_index.html", orders=orders)


@app.route("/create_order", methods=['POST'])
def saveOrder():
    order = CookieOrders.save(request.form)
    print(order)

    if not CookieOrders.validateOrders(request.form):
        return redirect("/new_order")

    return redirect("/")

@app.route("/new_order")
def newOrder():
    orders = CookieOrders.getOrders()

    return render_template("cookie_orders_create.html", orders=orders)


@app.route("/edit_order/<int:order_id>")
def editOrder(order_id):
    data = {"order_id": order_id}
    order = CookieOrders.showSingleOrder(data)

    return render_template("cookie_orders_edit.html", order=order)


@app.route("/edit_order/<int:order_id>", methods=['POST'])
def updateOrder(order_id):
    if not CookieOrders.validateOrders(request.form):
        return redirect(f"/edit_order/{order_id}")

    CookieOrders.editOrder(request.form)

    return redirect("/")