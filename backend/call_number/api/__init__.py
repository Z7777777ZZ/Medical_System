from flask import Blueprint

bp = Blueprint('call_number', __name__)

from . import queue, call_log 