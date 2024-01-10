# import math
#
# from flask import render_template, request, redirect, session, jsonify, flash, url_for
# from app import dao, utils
# from app import app, login, db
# from flask_login import login_user, logout_user
# from app.models import NhanVien, UserRoleEnum, BenhNhan
# from datetime import datetime
# from app.admin import current_user
#
#
#
# @app.route('/api/lapphieukham', methods=['post'])
# def add_thuoc():
#     thuocs = session.get('thuocs')
#     if thuocs is None:
#         thuocs = {}
#     data = request.json
#     maThuoc_id = str(data.get("maThuoc_id"))
#
#     if id in thuocs:  # san pham da co trong gio
#         thuocs[maThuoc_id]["quantity"] = thuocs[maThuoc_id]["quantity"]+1
#     else:  # san pham chua co trong gio
#         thuocs[maThuoc_id] = {
#             "maThuoc_id": maThuoc_id,
#             "lieuDung": data.get("lieuDung"),
#
#
#             "price": data.get("price"),
#             "quantity": 1
#         }
#     session['maThuoc_id'] = maThuoc_id
#
#     return jsonify(utils.count_cart(maThuoc_id))
#
#
# @app.route('/api/lapphieukham/<product_id>', methods=['put'])
# def updata_thuoc(product_id):
#     thuocs = session.get('thuocs')
#     if thuocs and product_id in thuocs:
#         quantity = request.json.get('quantity')
#         thuocs[product_id]['quantity'] = int(quantity)
#
#     session['cart'] = thuocs
#
#     return jsonify(utils.count_cart(thuocs))
#
#
# @app.route('/api/lapphieukham/<product_id>', methods=['delete'])
# def delete_thuoc(product_id):
#     cart = session.get('cart')
#     if cart and product_id in cart:
#         del cart[product_id]
#
#     session['cart'] = cart
#
#     return jsonify(utils.count_cart(cart))
#
#
# @app.route('/api/pay', methods=['post'])
# def xacnhan():
#     try:
#         dao.add_receipt(session.get('cart'))
#     except:
#         return jsonify({'status': 500, 'err_msg': 'he thong dang co loi'})
#     else:
#         del session['cart']
#         return jsonify({'status': 200})
