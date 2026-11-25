import json
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
ARCHIVO_TAREAS = Path(__file__).with_name("tareas.json")


def fecha_actual() -> datetime:
    return datetime.now().astimezone()


@dataclass
class Comentario:
    texto: str
    creado_en: datetime = field(default_factory=fecha_actual)


@dataclass
class Tarea:
    titulo: str
    descripcion: str
    asignado_a: str
    prioridad: str
    creada_en: datetime = field(default_factory=fecha_actual)
    completada: bool = False
    completada_en: datetime | None = None
    comentarios: list[Comentario] = field(default_factory=list)


def tarea_a_diccionario(tarea: Tarea) -> dict:
    return {
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "asignado_a": tarea.asignado_a,
        "prioridad": tarea.prioridad,
        "creada_en": tarea.creada_en.isoformat(),
        "completada": tarea.completada,
        "completada_en": (
            tarea.completada_en.isoformat() if tarea.completada_en else None
        ),
        "comentarios": [
            {
                "texto": comentario.texto,
                "creado_en": comentario.creado_en.isoformat(),
            }
            for comentario in tarea.comentarios
        ],
    }


def tarea_desde_diccionario(datos: dict, numero: int) -> Tarea:
    try:
        if not isinstance(datos, dict):
            raise TypeError("El registro debe ser un objeto JSON.")

        comentarios_datos = datos.get("comentarios", [])
        if not isinstance(comentarios_datos, list):
            raise TypeError("Los comentarios deben ser una lista.")

        comentarios = []
        for comentario in comentarios_datos:
            if not isinstance(comentario, dict):
                raise TypeError("Cada comentario debe ser un objeto JSON.")
            comentarios.append(
                Comentario(
                    texto=comentario["texto"],
                    creado_en=datetime.fromisoformat(comentario["creado_en"]),
                )
            )

        if not isinstance(datos["completada"], bool):
            raise TypeError("El estado completada debe ser verdadero o falso.")

        fecha_cierre = datos["completada_en"]
        return Tarea(
            titulo=datos["titulo"],
            descripcion=datos["descripcion"],
            asignado_a=datos["asignado_a"],
            prioridad=datos["prioridad"],
            creada_en=datetime.fromisoformat(datos["creada_en"]),
            completada=datos["completada"],
            completada_en=(
                datetime.fromisoformat(fecha_cierre) if fecha_cierre else None
            ),
            comentarios=comentarios,
        )
    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError(
            f"La tarea {numero} de {ARCHIVO_TAREAS} tiene un formato inválido."
        ) from error


def cargar_tareas() -> list[Tarea]:
    if not ARCHIVO_TAREAS.exists():
        return []

    try:
        with ARCHIVO_TAREAS.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"{ARCHIVO_TAREAS} no contiene JSON válido "
            f"(línea {error.lineno}, columna {error.colno})."
        ) from error

    if not isinstance(datos, list):
        raise RuntimeError(f"{ARCHIVO_TAREAS} debe contener una lista de tareas.")

    return [
        tarea_desde_diccionario(registro, numero)
        for numero, registro in enumerate(datos, start=1)
    ]


def guardar_tareas() -> None:
    archivo_temporal = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=ARCHIVO_TAREAS.parent,
            prefix=".tareas-",
            suffix=".tmp",
            delete=False,
        ) as archivo:
            archivo_temporal = Path(archivo.name)
            json.dump(
                [tarea_a_diccionario(tarea) for tarea in tareas],
                archivo,
                ensure_ascii=False,
                indent=2,
            )
            archivo.write("\n")

        os.replace(archivo_temporal, ARCHIVO_TAREAS)
    finally:
        if archivo_temporal is not None and archivo_temporal.exists():
            archivo_temporal.unlink()


tareas: list[Tarea] = cargar_tareas()


@app.before_request
def recargar_tareas():
    tareas[:] = cargar_tareas()


def obtener_tarea(indice: int) -> Tarea:
    if not 0 <= indice < len(tareas):
        abort(404)
    return tareas[indice]


@app.get("/")
def inicio():
    return render_template("index.html", tareas=tareas)


@app.get("/tareas/listado")
def listar_tareas():
    orden = request.args.get("orden", "fecha")
    direccion = request.args.get("direccion", "desc")
    filtro_prioridad = request.args.get("prioridad", "todas")
    filtro_estado = request.args.get("estado", "todos")
    prioridad_orden = {"Baja": 0, "Media": 1, "Alta": 2}
    claves_orden = {
        "asignado": lambda tarea: tarea.asignado_a.casefold(),
        "fecha": lambda tarea: tarea.creada_en,
        "prioridad": lambda tarea: prioridad_orden[tarea.prioridad],
    }

    if orden not in claves_orden:
        abort(400, description="Criterio de ordenamiento no válido.")
    if direccion not in {"asc", "desc"}:
        abort(400, description="Dirección de ordenamiento no válida.")
    if filtro_prioridad not in {"todas", "Baja", "Media", "Alta"}:
        abort(400, description="Filtro de prioridad no válido.")
    if filtro_estado not in {"todos", "pendientes", "completadas"}:
        abort(400, description="Filtro de estado no válido.")

    tareas_filtradas = tareas
    if filtro_prioridad != "todas":
        tareas_filtradas = [
            tarea
            for tarea in tareas_filtradas
            if tarea.prioridad == filtro_prioridad
        ]
    if filtro_estado == "pendientes":
        tareas_filtradas = [
            tarea for tarea in tareas_filtradas if not tarea.completada
        ]
    elif filtro_estado == "completadas":
        tareas_filtradas = [
            tarea for tarea in tareas_filtradas if tarea.completada
        ]

    tareas_ordenadas = sorted(
        tareas_filtradas,
        key=claves_orden[orden],
        reverse=(direccion == "desc"),
    )
    return render_template(
        "listado.html",
        tareas=tareas_ordenadas,
        total_tareas=len(tareas),
        orden=orden,
        direccion=direccion,
        filtro_prioridad=filtro_prioridad,
        filtro_estado=filtro_estado,
    )


@app.post("/tareas")
def agregar_tarea():
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    asignado_a = request.form.get("asignado_a", "").strip() or "Sin asignar"
    prioridad = request.form.get("prioridad", "Media")
    comentario = request.form.get("comentario", "").strip()

    if not titulo:
        return render_template(
            "index.html",
            tareas=tareas,
            error="Escribe una tarea antes de agregarla.",
        ), 400

    if prioridad not in {"Baja", "Media", "Alta"}:
        return render_template(
            "index.html",
            tareas=tareas,
            error="Selecciona una prioridad válida.",
        ), 400

    nueva_tarea = Tarea(
        titulo=titulo,
        descripcion=descripcion,
        asignado_a=asignado_a,
        prioridad=prioridad,
    )
    if comentario:
        nueva_tarea.comentarios.append(Comentario(texto=comentario))

    tareas.append(nueva_tarea)
    guardar_tareas()
    return redirect(url_for("inicio"))


@app.post("/tareas/<int:indice>/completar")
def completar_tarea(indice):
    tarea = obtener_tarea(indice)
    tarea.completada = not tarea.completada
    tarea.completada_en = fecha_actual() if tarea.completada else None
    guardar_tareas()
    return redirect(url_for("inicio"))


@app.post("/tareas/<int:indice>/comentarios")
def agregar_comentario(indice):
    tarea = obtener_tarea(indice)
    texto = request.form.get("comentario", "").strip()
    if not texto:
        return render_template(
            "index.html",
            tareas=tareas,
            error="Escribe un comentario antes de agregarlo.",
        ), 400

    tarea.comentarios.append(Comentario(texto=texto))
    guardar_tareas()
    return redirect(url_for("inicio"))


@app.post("/tareas/<int:indice>/eliminar")
def eliminar_tarea(indice):
    obtener_tarea(indice)
    tareas.pop(indice)
    guardar_tareas()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
