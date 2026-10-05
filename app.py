from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta_gmq_taller"


def get_db_connection():
    con = sqlite3.connect("taller.db")
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = get_db_connection()
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS servicios(
            id INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            costo REAL NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS ordenes_trabajo(
            id INTEGER PRIMARY KEY,
            fecha TEXT NOT NULL,
            cliente_id INTEGER NOT NULL,
            servicio_id INTEGER NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (servicio_id) REFERENCES servicios(id)
        )
        """
    )
    con.commit()
    con.close()


# --- Inicio ---
@app.route("/")
def index():
    return redirect(url_for("clientes"))


# ===================== CLIENTES =====================
@app.route("/clientes")
def clientes():
    con = get_db_connection()
    datos = con.execute("SELECT * FROM clientes").fetchall()
    con.close()
    return render_template("clientes.html", clientes=datos)


@app.route("/cliente/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        telefono = request.form["telefono"]

        con = get_db_connection()
        con.execute(
            "INSERT INTO clientes (nombre, apellidos, telefono) VALUES (?, ?, ?)",
            (nombre, apellidos, telefono),
        )
        con.commit()
        con.close()
        flash("Cliente agregado correctamente.", "success")
        return redirect(url_for("clientes"))

    return render_template("formulario_cliente.html", cliente=None)


@app.route("/cliente/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    con = get_db_connection()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        telefono = request.form["telefono"]
        con.execute(
            "UPDATE clientes SET nombre = ?, apellidos = ?, telefono = ? WHERE id = ?",
            (nombre, apellidos, telefono, id),
        )
        con.commit()
        con.close()
        flash("Cliente actualizado correctamente.", "success")
        return redirect(url_for("clientes"))

    cliente = con.execute("SELECT * FROM clientes WHERE id = ?", (id,)).fetchone()
    con.close()
    return render_template("formulario_cliente.html", cliente=cliente)


@app.route("/cliente/eliminar/<int:id>")
def eliminar_cliente(id):
    con = get_db_connection()
    con.execute("DELETE FROM clientes WHERE id = ?", (id,))
    con.commit()
    con.close()
    flash("Cliente eliminado.", "success")
    return redirect(url_for("clientes"))


# ===================== SERVICIOS =====================
@app.route("/servicios")
def servicios():
    con = get_db_connection()
    datos = con.execute("SELECT * FROM servicios").fetchall()
    con.close()
    return render_template("servicios.html", servicios=datos)


@app.route("/servicio/nuevo", methods=["GET", "POST"])
def nuevo_servicio():
    if request.method == "POST":
        descripcion = request.form["descripcion"]
        costo = request.form["costo"]

        con = get_db_connection()
        con.execute(
            "INSERT INTO servicios (descripcion, costo) VALUES (?, ?)",
            (descripcion, costo),
        )
        con.commit()
        con.close()
        flash("Servicio agregado correctamente.", "success")
        return redirect(url_for("servicios"))

    return render_template("formulario_servicio.html", servicio=None)


@app.route("/servicio/editar/<int:id>", methods=["GET", "POST"])
def editar_servicio(id):
    con = get_db_connection()

    if request.method == "POST":
        descripcion = request.form["descripcion"]
        costo = request.form["costo"]
        con.execute(
            "UPDATE servicios SET descripcion = ?, costo = ? WHERE id = ?",
            (descripcion, costo, id),
        )
        con.commit()
        con.close()
        flash("Servicio actualizado correctamente.", "success")
        return redirect(url_for("servicios"))

    servicio = con.execute("SELECT * FROM servicios WHERE id = ?", (id,)).fetchone()
    con.close()
    return render_template("formulario_servicio.html", servicio=servicio)


@app.route("/servicio/eliminar/<int:id>")
def eliminar_servicio(id):
    con = get_db_connection()
    con.execute("DELETE FROM servicios WHERE id = ?", (id,))
    con.commit()
    con.close()
    flash("Servicio eliminado.", "success")
    return redirect(url_for("servicios"))


# ===================== ORDENES DE TRABAJO =====================
@app.route("/ordenes")
def ordenes():
    con = get_db_connection()
    datos = con.execute(
        """
        SELECT o.id, o.fecha,
               c.nombre || ' ' || c.apellidos AS cliente,
               s.descripcion AS servicio
        FROM ordenes_trabajo o
        JOIN clientes c ON o.cliente_id = c.id
        JOIN servicios s ON o.servicio_id = s.id
        """
    ).fetchall()
    con.close()
    return render_template("ordenes.html", ordenes=datos)


@app.route("/orden/nueva", methods=["GET", "POST"])
def nueva_orden():
    con = get_db_connection()

    if request.method == "POST":
        fecha = request.form["fecha"]
        cliente_id = request.form["cliente_id"]
        servicio_id = request.form["servicio_id"]

        con.execute(
            "INSERT INTO ordenes_trabajo (fecha, cliente_id, servicio_id) VALUES (?, ?, ?)",
            (fecha, cliente_id, servicio_id),
        )
        con.commit()
        con.close()
        flash("Orden de trabajo registrada correctamente.", "success")
        return redirect(url_for("ordenes"))

    clientes = con.execute("SELECT id, nombre || ' ' || apellidos AS nombre FROM clientes").fetchall()
    servicios = con.execute("SELECT id, descripcion FROM servicios").fetchall()
    con.close()
    return render_template("formulario_orden.html", clientes=clientes, servicios=servicios)


@app.route("/orden/eliminar/<int:id>")
def eliminar_orden(id):
    con = get_db_connection()
    con.execute("DELETE FROM ordenes_trabajo WHERE id = ?", (id,))
    con.commit()
    con.close()
    flash("Orden de trabajo eliminada.", "success")
    return redirect(url_for("ordenes"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)