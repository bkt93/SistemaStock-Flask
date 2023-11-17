# routes/__init__.py
from flask import Blueprint

# Importa aquí tus Blueprints
from .hardware import hardware_bp

# Registra tus Blueprints
def init_app(app):
    app.register_blueprint(hardware_bp)
