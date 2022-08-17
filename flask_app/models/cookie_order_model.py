from flask_app.config.cookie_orders_connection import MySQLConnection
from flask import flash
import re

db = "cookie_orders"
NAME_REGEX = re.compile(r'^[a-zA-Z.-]+$')
COOKIE_REGEX = re.compile(r'^[a-zA-Z]+$')

class CookieOrders:
    def __init__(self, db_data):
        self.order_id = db_data['order_id']
        self.name = db_data['name']
        self.type = db_data['type']
        self.box_count = db_data['box_count']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cookie_orders (name, type, box_count, created_at, updated_at) VALUES (%(name)s, %(type)s, %(box_count)s, NOW(), NOW());"
        results = MySQLConnection(db).query_db(query, data)
        return results

    @classmethod
    def getOrders(cls):
        query = "SELECT * FROM cookie_orders"
        results = MySQLConnection(db).query_db(query)
        orders = []

        for order in results:
            orders.append(cls(order))

        return orders

    @classmethod
    def showSingleOrder(cls, data):
        query = "SELECT * FROM cookie_orders WHERE order_id = %(order_id)s"
        result = MySQLConnection(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def editOrder(cls, data):
        query = "UPDATE cookie_orders SET name = %(name)s, type = %(type)s, box_count = %(box_count)s, updated_at = NOW() WHERE order_id = %(order_id)s"
        return MySQLConnection(db).query_db(query, data)

    @staticmethod
    def validateOrders(order):
        isValid = True

        if len(order['name']) < 2:
            flash("Name must be longer than 2 characters")
            isValid = False
        if not NAME_REGEX.match(order['name']):
            flash("Name contains invalid characters")
            isValid = False
        if len(order['type']) < 2:
            flash("Cookie Type must be longer than 2 characters")
            isValid = False
        if not COOKIE_REGEX.match(order['type']):
            flash("Cookie Type contains invalid characters")
            isValid = False
        if int(order['box_count']) < 0:
            flash("The order amount cannot be less than zero")
            isValid = False

        return isValid