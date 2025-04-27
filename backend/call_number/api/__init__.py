from flask import Blueprint

bp = Blueprint('call_number', __name__)

from call_number.api import queue
