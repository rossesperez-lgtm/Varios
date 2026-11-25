# Gestor de tareas

Aplicación web sencilla para crear y organizar tareas. Permite asignar una persona, establecer una prioridad, registrar comentarios y consultar las fechas de creación y cierre.

## Funcionalidades

- Crear tareas con título, descripción, persona asignada y prioridad.
- Agregar comentarios al crear una tarea o posteriormente.
- Marcar tareas como completadas o reabrirlas.
- Asignar automáticamente las fechas de creación, comentarios y cierre.
- Consultar todas las tareas en un listado de solo lectura.
- Filtrar el listado por prioridad y estado, y ordenarlo por persona asignada, fecha o prioridad.
- Guardar y cargar los datos desde `tareas.json`.

## Tecnologías

- Python y Flask para la aplicación y sus rutas web.
- HTML con plantillas Jinja para las páginas.
- CSS para la presentación.
- JSON como almacenamiento local.
- Docker y Docker Compose para ejecutarla en un contenedor.

## Requisitos

- Para ejecutar localmente: Python 3.10 o posterior y `uv`.
- Para usar Docker: Docker Desktop con Docker Compose.

## Ejecutar localmente en Windows

Abre PowerShell desde `C:\Cursos\Varios`.

Si todavía no existe el entorno virtual del proyecto, créalo:

```powershell
uv venv .venv --python 3.14
```

Instala Flask en el entorno virtual:

```powershell
uv pip install --python .venv\Scripts\python.exe -r Gestor_tareas\requirements.txt
```

Inicia la aplicación:

```powershell
cd Gestor_tareas
..\.venv\Scripts\python.exe app.py
```

Abre `http://127.0.0.1:5000` en el navegador. Detén el servidor con `Ctrl+C`.

## Ejecutar con Docker

Desde PowerShell, ve a la carpeta de la aplicación y construye e inicia el contenedor:

```powershell
cd C:\Cursos\Varios\Gestor_tareas
docker compose up --build
```

Abre `http://127.0.0.1:5000`. Para detener y retirar el contenedor, presiona `Ctrl+C` y ejecuta:

```powershell
docker compose down
```

También se puede iniciar en segundo plano y consultar sus registros:

```powershell
docker compose up --build -d
docker compose logs -f
```

En este modo, la carpeta del proyecto se monta dentro del contenedor. Por eso `tareas.json` permanece en el equipo y conserva los datos después de detener o recrear el contenedor.

## Rutas principales

- `/`: formulario para crear tareas y gestionar las existentes.
- `/tareas/listado`: listado de solo lectura con filtros y opciones de ordenamiento.

## Almacenamiento y alcance

Las tareas se guardan en `tareas.json`, ubicado junto a `app.py`. El archivo se lee al iniciar la aplicación y antes de atender cada solicitud; las operaciones que modifican tareas lo actualizan.

Este proyecto es un ejemplo de estudio: no utiliza una base de datos ni tiene inicio de sesión. El usuario asignado es texto libre, no una cuenta de usuario. `tareas.json` está incluido en Git, por lo que los cambios en su contenido también aparecerán como cambios versionables.
