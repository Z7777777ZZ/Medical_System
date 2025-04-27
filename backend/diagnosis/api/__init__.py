from flask import Blueprint

bp = Blueprint('diagnosis', __name__)

from diagnosis.api import prescription
