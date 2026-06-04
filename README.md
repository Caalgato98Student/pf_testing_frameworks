# Sistema de inventario para repostería Honeydukes

## Descripción del Proyecto

Sistema web de gestión de inventario desarrollado en Django para una repostería. Permite administrar productos y lotes con control de fechas de elaboración y cantidades, e incluye un sistema de alertas para productos próximos a vencer y funcionalidades CRUD completas.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado en tu computadora:
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

---

## Pasos para Clonar y Levantar el Proyecto

Sigue estos sencillos pasos para levantar el proyecto localmente utilizando Docker:

### 1. Clonar el repositorio
Clona este repositorio en tu máquina local y accede a la carpeta del proyecto:
```bash
git clone <url-del-repositorio>
cd pf_testing_frameworks
```

### 2. Configurar las variables de entorno
Crea una copia del archivo de configuración para Docker:
* **En Windows (CMD):**
  ```cmd
  copy .env.docker.example .env.docker
  ```
* **En Linux / macOS / PowerShell:**
  ```bash
  cp .env.docker.example .env.docker
  ```

### 3. Levantar los contenedores
Construye las imágenes e inicia los servicios del proyecto:
```bash
docker compose up --build
```
*Nota: Este comando descargará las dependencias necesarias de Python mediante uv, configurará la base de datos MariaDB, aplicará las migraciones y cargará los datos iniciales de prueba de forma automática.*

### 4. Acceder al sistema
Una vez que los contenedores terminen de iniciar, abre tu navegador web e ingresa a:
```
http://localhost:8000/
```

---

## Usuarios Demo (Cargados por defecto)

El sistema viene precargado con los siguientes usuarios de prueba para facilitar la navegación y el testeo de las funcionalidades:

### Usuario estándar (Operador de inventario)
* **Usuario:** `Prueba`
* **Contraseña:** `Admin123456789.`

### Usuario administrador (Acceso total al sistema y panel de Django)
* **Usuario:** `test`
* **Contraseña:** `test_admin`
