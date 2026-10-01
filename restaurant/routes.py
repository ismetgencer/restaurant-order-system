from flask import Blueprint, abort, redirect, render_template, request, url_for

from restaurant.db import advance_status, delete_order, insert_order, list_orders
from restaurant.menu import price_order

bp = Blueprint('main', __name__)

ORDER_ERROR = 'Lütfen en az bir ürün seçin'


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            total, items, lines = price_order(
                request.form.getlist('urun'),
                request.form.getlist('adet'),
            )
        except ValueError:
            return render_template('index.html', error=ORDER_ERROR)

        table_number = request.form.get('masa')
        insert_order(table_number, items, total)
        return render_template(
            'order_summary.html',
            masa=table_number,
            lines=lines,
            toplam=total,
        )
    return render_template('index.html')


@bp.route('/admin')
def admin():
    return render_template('admin.html', siparisler=list_orders())


@bp.post('/admin/<int:order_id>/status')
def update_status(order_id):
    if not advance_status(order_id):
        abort(404)
    return redirect(url_for('main.admin'))


@bp.post('/admin/<int:order_id>/delete')
def remove_order(order_id):
    if not delete_order(order_id):
        abort(404)
    return redirect(url_for('main.admin'))
