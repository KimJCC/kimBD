🤖 Agente IA Text-to-SQL para Gestión de Ventas de Electrónicos
Traducción de Lenguaje Natural (Español) a SQL usando Groq y Flask.

Resumen del Proyecto
Este proyecto es un Agente Inteligente capaz de convertir consultas en Lenguaje Natural (Español) en sentencias SQL válidas para la gestión de ventas de productos electrónicos. Permite a los usuarios interactuar con la base de datos sin escribir código SQL.

El sistema utiliza:

Flask para el servidor web y la interfaz de usuario.

La API de Groq (usando Llama-3.1) como motor de traducción rápida de NL a SQL.

MySQL como base de datos transaccional.

Características Principales
🌐 Interfaz Web Intuitiva: Aplicación web con un diseño simple para facilitar la interacción.

⚡️ Traducción Rápida con Groq: Alta velocidad en la conversión de texto a consultas SQL (SELECT, INSERT, UPDATE, DELETE).

🔒 Seguridad: Lógica de validación implementada para bloquear comandos destructivos como DROP o TRUNCATE.

📦 Enfoque en Ventas: Esquema optimizado para productos electrónicos, inventario y registro de transacciones.

Esquema de Base de Datos
El agente interactúa con el esquema ventas_electronicos, que se centra en dos tablas principales:
Tabla,Descripción,Campos Clave (PK)
productos,"Catálogo de electrónicos, precios e inventario actual.","id, nombre, marca, precio_venta, stock"
transacciones,Registro detallado de cada venta (histórico).,"id, producto_id, cantidad_vendida, fecha_venta, total_venta"
Ejemplos de Funcionalidad (Text-to-SQL)
El agente está diseñado para manejar consultas complejas sobre ventas e inventario:

Categoría,Prompt al Agente,Sentencia SQL Esperada
Inventario,"""Muestra el stock restante de los 'Auriculares Inalámbricos'""",SELECT stock FROM productos WHERE nombre = 'Auriculares Inalámbricos';
Ventas,"""¿Cuál fue el total de ventas generadas el 2025-11-06?""",SELECT SUM(total_venta) FROM transacciones WHERE fecha_venta = '2025-11-06';
Modificación,"""Actualizar el precio de venta del 'Monitor Curvo' a 4500.""",UPDATE productos SET precio_venta = 4500 WHERE nombre = 'Monitor Curvo';
Inserción,"""Registrar una venta de 2 'Smartwatch Pro' a precio de 1500 hoy.""","INSERT INTO transacciones (producto_id, cantidad_vendida, fecha_venta, total_venta) VALUES..."

Instalación y Configuración
Sigue estos pasos para poner en marcha el agente en tu entorno local.

1. Requisitos
Python 3.x

Servidor MySQL activo.

Una clave API de Groq (Obtén la tuya en Groq Console).

2. Estructura del Proyecto
3. Agente_SQL_Electronicos/
├── venv/
├── templates/
│   └── index.html 
├── static/
│   └── style.css
└── app.py # Servidor Flask y Lógica
3. Configuración
Abre el archivo app.py y configura tus credenciales:

# app.py
# --- Configuración Groq y MySQL ---
GROQ_API_KEY = "gsk_TU_CLAVE_GROQ_AQUÍ" 
MYSQL_CONFIG = {
    "database": "ventas_electronicos", # Asegúrate de que esta DB exista
    "user": "root",
    "password": "TU_PASSWORD_MYSQL" 
}
# ---------------------------------

4. Ejecución
Crea y activa el entorno virtual:

python -m venv venv 
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

Instala las dependencias:
pip install Flask mysql-connector-python groq

Inicia la aplicación:
python app.py
El agente estará disponible en tu navegador en http://127.0.0.1:5000.

