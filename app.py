from flask import Flask , request ,render_template, redirect, url_for 
import sqlite3

app = Flask(__name__)

def init_database():
    conn = sqlite3.connect('kardex.db')
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha_nac DATE NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    
init_database()

@app.route('/')
def index():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('kardex.db')
    # Permite manejar registros como diccionarios (para acceder por nombre de columna)
    conn.row_factory = sqlite3.Row
    
    # Obtener un cursor para ejecutar consultas
    cursor = conn.cursor()
    # Realizar una consulta para obtener todas las personas
    cursor.execute("SELECT * FROM personas")
    # Almacenar los resultados en una variable
    personas = cursor.fetchall()
    
    return render_template('index.html', personas=personas)


@app.route("/create")
def create():
    return render_template('create.html')


@app.route("/save", methods=["POST"])
def save():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']
    conn = sqlite3.connect('kardex.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO personas (nombre, telefono, fecha_nac) VALUES (?, ?, ?)", (nombre, telefono, fecha_nac)) # Inserción de datos en la tabla personas con parámetros
    conn.commit()
    conn.close()
    return redirect("/")

# Editar registro
@app.route("/edit/<int:id>")
def persona_edit(id):
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id = ?", (id,))
    persona = cursor.fetchone()
    conn.close()
    return render_template("edit.html", persona = persona)

# Guardar actualización de registro
@app.route("/update", methods=['POST'])
def personas_update():
    id = request.form['id']
    nombre= request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE personas SET nombre=?, telefono=?, fecha_nac=? WHERE id=?""", (nombre, telefono, fecha_nac, id))
    conn.commit()
    conn.close()
    return redirect("/")

# Eliminar registro
@app.route("/delete/<int:id>")
def personas_delete(id):
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id=?", (id,))
    conn.commit()
    conn.close()    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5003) # Ejecución de la aplicación en el puerto 5001 