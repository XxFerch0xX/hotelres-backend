# HotelRes - Sistema de Gestión de Reservas de Hoteles

Backend del sistema HotelRes desarrollado con FastAPI, SQLAlchemy y SQLite.

## Descripción

Sistema que automatiza y centraliza la gestión operativa de un hotel: reservas, habitaciones, clientes, facturación, control financiero y reportes.

## Estructura del Proyecto

```
hotelres-backend/
├── main.py                  # Punto de entrada de la aplicación
├── database.py              # Configuración de base de datos
├── requirements.txt         # Dependencias
├── models/                  # Modelos de datos (SQLAlchemy)
│   ├── usuario.py
│   ├── cliente.py
│   ├── habitacion.py
│   ├── reserva.py
│   ├── facturacion.py
│   ├── finanzas.py
│   └── configuracion.py
├── schemas/                 # Esquemas de validación (Pydantic)
│   ├── usuario.py
│   ├── cliente.py
│   ├── habitacion.py
│   ├── reserva.py
│   ├── facturacion.py
│   ├── finanzas.py
│   └── configuracion.py
├── repositories/            # Capa de acceso a datos
│   ├── usuario.py
│   ├── cliente.py
│   ├── habitacion.py
│   ├── reserva.py
│   ├── facturacion.py
│   ├── finanzas.py
│   └── configuracion.py
├── services/                # Lógica de negocio
│   ├── usuario.py
│   ├── cliente.py
│   ├── habitacion.py
│   ├── reserva.py
│   ├── facturacion.py
│   ├── finanzas.py
│   └── configuracion.py
└── controllers/             # Endpoints/Rutas (API REST)
    ├── usuario.py
    ├── cliente.py
    ├── habitacion.py
    ├── reserva.py
    ├── facturacion.py
    ├── finanzas.py
    └── configuracion.py
```

## Módulos

- **Configuración**: Usuarios, roles, parámetros del sistema, auditoría
- **Clientes**: Registro, consulta e historial de clientes
- **Habitaciones**: Tipos de habitación, catálogo, disponibilidad
- **Reservas**: Creación, modificación, check-in, check-out, cancelación
- **Facturación**: Consumos adicionales, facturas, pagos
- **Finanzas**: Plan de cuentas, libro diario, gastos operativos

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn main:app --reload
```

El servidor se levanta en `http://localhost:8000`.

## Documentación Swagger

Una vez levantado el servidor, acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Tecnologías

- **Python 3.10+**
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **SQLite** - Base de datos
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
# Pruebas con pytest y coverage 
