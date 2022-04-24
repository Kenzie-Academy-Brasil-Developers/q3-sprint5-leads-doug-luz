from flask import current_app, request, jsonify
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, ProgrammingError
from app.models.lead_model import LeadModel
from sqlalchemy.orm.session import Session
import re
from datetime import datetime
from sqlalchemy import func, desc

def create_lead():
    data = request.get_json()
    for key, value in data.items():
        if type(value)!=str:
            return {'error':'Entry types must be string'}, 400
    lead = LeadModel(**data)


    phone_format = "\(\d\d\)\d\d\d\d\d-\d\d\d\d"

    if not (re.fullmatch(phone_format, data['phone'])):
        return {'error': 'Phone format must be (xx)xxxxx-xxxx'}, 400
    
    try:
        session:Session = current_app.db.session
        session.add(lead)
        session.commit()
        return jsonify(lead), 201
    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {'error':'email or phone already in our database'}, 400
    

def retrieve():
    
    session:Session = current_app.db.session
    leads = session.query(LeadModel).order_by(desc(LeadModel.visits)).all()

    if not leads:
        return {'error':'There are not leads on database'}

    return jsonify(leads), 200


def update():
    
    data = request.get_json()
    if type(data['email'])!=str:
        return {'error':'Entry type must be string'}, 400     
        
    for key, value in data.items():
        if key != 'email':
            return {'error':'Please insert only email'}, 400
    session:Session = current_app.db.session
    email = data['email'] 
    
    lead = session.query(LeadModel).filter(LeadModel.email==email).first()
    if not lead:
        return {'error':'Id not found'}

       
    lead.last_visit = datetime.now()
    lead.visits += 1
    session.add(lead)
    session.commit()
    print(lead)
        
    return jsonify(lead)


def delete():
    data = request.get_json()
    if type(data['email'])!=str:
        return {'error':'Entry type must be string'}, 400     
        
    for key, value in data.items():
        if key != 'email':
            return {'error':'Please insert only email'}, 400
    email = data['email'] 
    session:Session = current_app.db.session

    lead = session.query(LeadModel).filter(LeadModel.email==email).first()

    if not lead:
        return {'error':'Id not found'}, 404

    session.delete(lead)
    session.commit()

    return '',204
    

