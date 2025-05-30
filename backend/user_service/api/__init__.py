from flask import Blueprint

bp = Blueprint('user_service', __name__)

from user_service.api import department, doctor, hospital, patient
