-- **************************************************
-- SCRIPT DE CREACIÓN DE LA BASE DE DATOS Y TABLAS
-- **************************************************

-- 1. Crear la Base de Datos (Si no existe)
CREATE DATABASE IF NOT EXISTS tienda_inventario;

-- 2. Seleccionar la Base de Datos para trabajar en ella
USE tienda_inventario;

-- 3. Tabla de Productos (Lo que hay en stock)
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL -- Cantidad de productos en almacén
);

-- 4. Tabla de Ventas (Para consultas de histórico, opcional)
CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    cantidad INT, -- Cantidad vendida
    fecha DATE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- 5. Inserción de Datos Iniciales (Para empezar a consultar)
INSERT INTO productos (nombre, categoria, precio, stock) VALUES
('Laptop Pro', 'Electrónica', 1200.00, 15),
('Mouse Inalámbrico', 'Electrónica', 25.50, 50),
('Camiseta Algodón', 'Ropa', 15.00, 120),
('Pantalón Jeans', 'Ropa', 45.99, 80),
('Libro de Python', 'Libros', 30.00, 30);