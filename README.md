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

---

## Ejecución de Pruebas Unitarias y Cobertura

El proyecto está configurado para ejecutar pruebas utilizando `pytest` y medir la cobertura con `coverage`. Las pruebas utilizan de forma automática una base de datos SQLite en memoria para agilizar la ejecución y evitar problemas de configuración en la base de datos MariaDB de desarrollo.

### 1. Ejecutar las pruebas con pytest
Para correr las pruebas unitarias:
```bash
docker compose exec web pytest inventario_reposteria/
```

### 2. Medir la cobertura (Coverage)
Para ejecutar las pruebas y recolectar las estadísticas de cobertura:
```bash
docker compose exec web coverage run -m pytest inventario_reposteria/
```

### 3. Ver el reporte de cobertura en consola
Para mostrar el reporte consolidado directamente en tu terminal:
```bash
docker compose exec web coverage report
```

### 4. Generar reporte interactivo HTML
Para generar un reporte visual e interactivo:
```bash
docker compose exec web coverage html
```
Esto creará una carpeta llamada `htmlcov/` en la raíz de tu proyecto. Puedes abrir el archivo `htmlcov/index.html` en tu navegador web para inspeccionar qué líneas de código han sido probadas.

