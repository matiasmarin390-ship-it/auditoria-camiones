import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename


app_routes = Blueprint("app_routes", __name__)


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


@app_routes.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app_routes.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "message": "Servicio activo"}, 200


@app_routes.route("/audit", methods=["POST"])
def audit():
    if "historico_file" not in request.files or "pdf_file" not in request.files:
        flash("Debés subir ambos archivos: histórico Excel y hoja de ruta PDF.")
        return redirect(url_for("app_routes.index"))

    historico_file = request.files["historico_file"]
    pdf_file = request.files["pdf_file"]

    if historico_file.filename == "" or pdf_file.filename == "":
        flash("Los dos archivos son obligatorios.")
        return redirect(url_for("app_routes.index"))

    if not allowed_file(historico_file.filename, current_app.config["ALLOWED_EXCEL_EXTENSIONS"]):
        flash("El histórico debe ser un archivo Excel .xlsx o .xls")
        return redirect(url_for("app_routes.index"))

    if not allowed_file(pdf_file.filename, current_app.config["ALLOWED_PDF_EXTENSIONS"]):
        flash("La hoja de ruta debe ser un archivo PDF.")
        return redirect(url_for("app_routes.index"))

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    historico_filename = secure_filename(historico_file.filename)
    pdf_filename = secure_filename(pdf_file.filename)

    historico_path = os.path.join(upload_folder, historico_filename)
    pdf_path = os.path.join(upload_folder, pdf_filename)

    historico_file.save(historico_path)
    pdf_file.save(pdf_path)

    # Por ahora mostramos confirmación simple.
    # En el próximo paso acá vamos a llamar al parser del Excel y PDF.
    return render_template(
        "result.html",
        historico_filename=historico_filename,
        pdf_filename=pdf_filename,
        historico_path=historico_path,
        pdf_path=pdf_path
    )
