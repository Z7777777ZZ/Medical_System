from flask import Blueprint

bp = Blueprint('diagnosis', __name__)

from . import diagnosis, prescription, template 