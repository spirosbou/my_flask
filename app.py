from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_conn():
    connex = None
    try:
        connex = sqlite3.connect('motorbikes.sqlite')
    except sqlite3.error as e:
        print(e)
    return connex

@app.route('/moto', methods=['GET', 'POST'])
def moto():
    connex = db_conn()
    cursor = connex.cursor()
    if request.method == 'GET':
        cursor = connex.execute("SELECT * FROM moto")
        motos = [dict(id=row[0], company=row[1], model=row[2], cm3=row[3], price=row[4], year=row[5])
                 for row in cursor.fetchall()
                 ]
        if motos is not None:
            return jsonify(motos)

    if request.method == 'POST':
        new_company = request.form['company']
        new_model = request.form['model']
        new_cm3 = request.form['cm3']
        new_price = request.form['price']
        new_year = request.form['year']
        sql = """INSERT INTO moto (company, model, cm3, price, year) VALUES (?, ?, ?, ?, ?)"""
        cursor = cursor.execute(sql, (new_company, new_model, new_cm3, new_price, new_year))
        connex.commit()
        return f"Moto with the id: {cursor.lastrowid}, created successfully!"

@app.route('/moto/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_moto(id):
    connex = db_conn()
    cursor = connex.cursor()
    moto = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM moto WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            moto = r
        if moto is not None:
            return jsonify(moto), 200
        else:
            return "Something wrong!", 404
    if request.method == 'PUT':
        sql = """UPDATE moto 
                SET company=?,
                    model=?,
                    cm3=?,
                    price=?,
                    year=? WHERE id=?"""

        company = request.form['company']
        model = request.form['model']
        cm3 = request.form['cm3']
        price = request.form['price']
        year = request.form['year']
        updated_moto = {
                "id": id,
                "company": company,
                "model": model,
                "cm3": cm3,
                "price": price,
                "year": year,
                }
        connex.execute(sql, (company, model, cm3, price, year, id))
        connex.commit()
        return jsonify(updated_moto)
    if request.method == 'DELETE':
        sql = """DELETE FROM moto WHERE id=?"""
        connex.execute(sql, (id,))
        connex.commit()
        return "The moto with id: {} has been deleted.".format(id), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
