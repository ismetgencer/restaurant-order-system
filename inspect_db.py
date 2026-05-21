import sqlite3, os
print('cwd:', os.getcwd())
db='orders.db'
print('db path:', os.path.abspath(db))
conn=sqlite3.connect(db)
c=conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables=c.fetchall()
print('tables:', tables)
if ('orders',) in tables:
    try:
        c.execute('SELECT * FROM orders')
        rows=c.fetchall()
        print('rows count:', len(rows))
        for r in rows[:10]:
            print(r)
    except Exception as e:
        print('select error:', e)
else:
    print('orders tablosu yok')
conn.close()