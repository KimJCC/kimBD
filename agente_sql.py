# --- agente_sql.py ---

import mysql.connector
from groq import Groq
import os



# CLAVE DE LA API DE GROQ
GROQ_API_KEY = "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"


DB_CONFIG = {
    "user": "root",        
    "password": "1234",    # <-- Tu contraseña de MySQL
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


def conectar_db():
    """Establece la conexión con la base de datos MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print(" Conexión a MySQL exitosa.") # <- Nuevo mensaje de éxito
        return conn
    except mysql.connector.Error as err:
        # <- Este bloque nos dirá el error exacto
        print("\n ERROR GRAVE: FALLO EN LA CONEXIÓN A LA BASE DE DATOS.")
        print(f"   Código de Error: {err.errno}")
        print(f"   Mensaje del Error: {err.msg}")
        print("   Posibles causas: 1. Contraseña '1234' incorrecta, 2. Servidor MySQL no iniciado.")
        return None

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


def ejecutar_sql(sql_query: str):
    conn = conectar_db()
    if not conn:
        return 

    cursor = conn.cursor()
    try:
        query_type = sql_query.split()[0].upper()
        
        cursor.execute(sql_query)
        
        if query_type == "SELECT":
            columnas = [i[0] for i in cursor.description]
            resultados = cursor.fetchall()
            
            print("\n Consulta SQL ejecutada con éxito.")
            print(f" SQL Generado: {sql_query}")
            print(f"** Resultados Obtenidos ({len(resultados)} filas): **")
            
            print("-" * 50)
            print(" | ".join(columnas))
            print("-" * 50)
            for fila in resultados:
                print(" | ".join(map(str, fila)))
            print("-" * 50)
            
        elif query_type in ["INSERT", "UPDATE", "DELETE"]:
            conn.commit()
            if query_type == "INSERT":
                print(f" Producto agregado (INSERT) con éxito. ID: {cursor.lastrowid}")
            else:
                print(f" Operación {query_type} ejecutada con éxito. Filas afectadas: {cursor.rowcount}")
        
    except Exception as e:
        conn.rollback()
        print(f" ERROR al ejecutar SQL: {e}\nSQL intentado: {sql_query}")
        
    finally:
        cursor.close()
        conn.close()


def agente_text_to_sql():
    print("-----------------------------------------------------")
    print("--- Agente Text-to-SQL para Gestión de Inventario ---")
    print("-----------------------------------------------------")
    print("Escribe tu consulta en lenguaje natural (o 'salir' para terminar).")
    
    while True:
        consulta_nl = input("\n Tu pregunta/solicitud: ")
        if consulta_nl.lower() == 'salir':
            print(" Agente finalizado.")
            break
        
        print("\n Analizando intención y generando SQL con Groq...")
        
        sql_generado = generar_sql(consulta_nl)
        
        if sql_generado:
            ejecutar_sql(sql_generado)
        else:
            print(" No se pudo generar una consulta SQL. Inténtalo de nuevo.")

if __name__ == "__main__":
    agente_text_to_sql()