# --- app.py ---

from flask import Flask, render_template, request, jsonify
import mysql.connector
from groq import Groq
import os

app = Flask(__name__)

# ==========================================================
# PARTE A: CONFIGURACIÓN y ESQUEMA (COPIA ESTO DESDE TU VIEJO agente_sql.py)
# ==========================================================

GROQ_API_KEY = "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"

DB_CONFIG = {
    "user": "root",        
    "password": "1234",    
    "host": "127.0.0.1",   
    "database": "tienda_inventario"
}

DB_SCHEMA = """
-- Esquema de la Base de Datos 'tienda_inventario'
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    cantidad INT,
    fecha DATE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
"""

# ==========================================================
# PARTE B: FUNCIÓN DE CONEXIÓN A MYSQL (COPIA ESTO DESDE TU VIEJO agente_sql.py)
# ==========================================================
def conectar_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        # print("✅ Conexión a MySQL exitosa.") # Este print ya no es necesario en Flask
        return conn
    except mysql.connector.Error as err:
        print(f"\n❌ ERROR GRAVE: FALLO EN LA CONEXIÓN A LA BASE DE DATOS.")
        print(f"   Código de Error: {err.errno}")
        print(f"   Mensaje del Error: {err.msg}")
        print("   Posibles causas: 1. Contraseña '1234' incorrecta, 2. Servidor MySQL no iniciado.")
        return None

# ==========================================================
# PARTE C: FUNCIÓN DE GENERACIÓN DE SQL (COPIA ESTO DESDE TU VIEJO agente_sql.py)
# ==========================================================
def generar_sql(pregunta_usuario: str) -> str:
    system_prompt = (
        "Eres un traductor experto de lenguaje natural a consultas SQL. "
        "Tu ÚNICA TAREA es generar la consulta SQL más precisa. "
        "NUNCA, bajo ninguna circunstancia, agregues explicaciones, texto adicional o bloques de código markdown. "
        "Utiliza el siguiente esquema de la base de datos:"
        f"\n\n{DB_SCHEMA}"
        "\n\nInstrucciones clave: Responde solo con el SQL."
    )
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pregunta_usuario},
            ],
            model="llama-3.1-8b-instant",
        )
        sql_generado = chat_completion.choices[0].message.content.strip()
        sql_generado = sql_generado.replace("```sql", "").replace("```", "").strip()
        return sql_generado
    except Exception as e:
        print(f"Error en la API de Groq: {e}")
        return None

# ==========================================================
# PARTE D: FUNCIÓN DE EJECUCIÓN DE SQL (MODIFICADA para Flask)
# ==========================================================
# Esta función ahora devuelve un diccionario con el resultado o el error
def ejecutar_sql(sql_query: str):
    conn = conectar_db()
    if not conn:
        return {"error": "No se pudo conectar a la base de datos."}

    cursor = conn.cursor(dictionary=True) # <- Importante: devuelve filas como diccionarios
    try:
        query_type = sql_query.split()[0].upper()
        cursor.execute(sql_query)
        
        if query_type == "SELECT":
            resultados = cursor.fetchall()
            return {"result": resultados} # Devuelve la lista de diccionarios
            
        elif query_type in ["INSERT", "UPDATE", "DELETE"]:
            conn.commit()
            msg = f"Operación {query_type} exitosa. Filas afectadas: {cursor.rowcount}"
            if query_type == "INSERT":
                msg += f". Nuevo ID: {cursor.lastrowid}"
            return {"result": msg}
        
        else:
            conn.commit()
            return {"result": "Comando SQL ejecutado sin retorno visible."}

    except Exception as e:
        conn.rollback()
        return {"error": f"ERROR al ejecutar SQL: {e}"}
        
    finally:
        cursor.close()
        conn.close()

# ==========================================================
# PARTE E: RUTAS DE FLASK (¡NUEVO!)
# ==========================================================

# Ruta principal que sirve la página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar las consultas del usuario (recibe datos del JavaScript)
@app.route('/query', methods=['POST'])
def handle_query():
    user_query = request.json.get('query')
    
    if not user_query:
        return jsonify({"error": "No se proporcionó ninguna consulta."}), 400

    sql_generated = generar_sql(user_query)
    
    if not sql_generated:
        return jsonify({"sql_generated": "No se pudo generar.", "error": "Fallo al generar SQL con Groq."})
    
    # Ejecutar el SQL y obtener el resultado o error
    execution_result = ejecutar_sql(sql_generated)
    
    # Combinar el SQL generado con el resultado de la ejecución
    response_data = {
        "sql_generated": sql_generated,
        **execution_result # Agrega 'result' o 'error' del diccionario de ejecución
    }
    
    return jsonify(response_data)

# ==========================================================
# INICIO DEL SERVIDOR FLASK
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True) # debug=True recarga el servidor automáticamente con cambios