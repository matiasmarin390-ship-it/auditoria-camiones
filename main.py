from flask import Flask
from app.routes import app_routes
from app.config import Config
import os


def create_app():
    app = Flask(
        __name__,
        template_folder="app/templates",
        static_folder="app/static"
    )

    app.config.from_object(Config)

    # Crear carpeta uploads si no existe
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Registrar rutas
    app.register_blueprint(app_routes)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
