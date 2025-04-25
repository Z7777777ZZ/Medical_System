from flask import Blueprint

bp = Blueprint('diagnosis', __name__)

# Import routes after blueprint is created to avoid circular imports
from . import diagnosis, prescription, template 