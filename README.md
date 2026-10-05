# Taller Mecánico - CRUD con Flask

Aplicación web con Flask y SQLite para gestionar un taller mecánico, reproduciendo la
estructura del video "Centro de Capacitación" pero aplicada a un problema diferente.

**Estudiante:** Gustavo Mamani Quisberth (GMQ) — Código: 11097581

## Tablas

- `clientes` — datos de los clientes del taller.
- `servicios` — catálogo de servicios ofrecidos y su costo.
- `ordenes_trabajo` — relaciona un cliente con un servicio en una fecha (FK a `clientes` y `servicios`).

## Funcionalidades

- CRUD completo (crear, listar, editar, eliminar) para **clientes** y **servicios**.
- Registro y eliminación de **órdenes de trabajo**, con selección dinámica de cliente y servicio.
- Plantillas con herencia Jinja2 (`base.html`) y Bootstrap.

## Cómo ejecutar

```bash
python -m venv venv
venv\Scripts\activate
pip install flask
python app.py
```

Abrir `http://127.0.0.1:5000/` en el navegador.