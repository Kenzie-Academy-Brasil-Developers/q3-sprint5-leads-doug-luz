from turtle import update
from flask import Blueprint

from app.controllers.leads_controller import create_lead, delete, retrieve, update

bp = Blueprint('leads', __name__, url_prefix='/leads')

bp.post('')(create_lead)
bp.get('')(retrieve)
bp.patch('')(update)
bp.delete('')(delete)