from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

menu = {
    'Hamburger': 80,
    'Pizza': 120,
    'Kola': 20,
    'Salata': 30,
    'Tatlı': 45
}

DB_NAME = os.path.join(os.path.dirname(__file__), 'orders.db')

def create_db():
    # always ensure the database file exists and table is present
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_number TEXT,
                items TEXT,
                total_price INTEGER
            )
        """)
        conn.commit()

create_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        masa = request.form.get('masa')
        urunler = request.form.getlist('urun')
        adetler = request.form.getlist('adet')
        # validation: en az bir ürün seçilmeli
        if not urunler:
            return render_template('index.html', menu=menu, error='Lütfen en az bir ürün seçin')
        toplam = 0
        urun_str = ""

        for urun, adet in zip(urunler, adetler):
            adet = int(adet)
            toplam += menu[urun] * adet
            urun_str += f"{urun} (x{adet}), "

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO orders (table_number, items, total_price) VALUES (?, ?, ?)",
                      (masa, urun_str.strip(', '), toplam))
            conn.commit()

        return render_template('order_summary.html', masa=masa, urunler=urunler, adetler=[int(a) for a in adetler], toplam=toplam, menu=menu)
    return render_template('index.html', menu=menu)

@app.route('/admin')
def admin():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM orders ORDER BY id DESC")
        siparisler = c.fetchall()
    return render_template('admin.html', siparisler=siparisler)

if __name__ == '__main__':
    app.run(debug=True)
