from datetime import datetime
import json
import logging
from operator import and_
import os
from typing import cast
from flask import current_app, request
from sqlalchemy import between
from portal.app.Core.Controllers.BaseController import index, find, store, update, delete
from portal.app.Data.Enum.http_status_code import HTTPStatusCode
from portal.app.Exceptions.APIException import APIException
from portal.app.Services.ScheduleService import ScheduleService
from portal.app.Data.Models import Schedule
from portal.database.DBConnection import AlchemyEncoder, get_session
from portal.utils.http_utils import build_response

def current_video(service: ScheduleService):    
    session = get_session()
    
    input_params = request.args.to_dict()
    
    if 'current_datetime' not in input_params:
        return build_response(400, {"error": True, "description": "current_datetime is mandatory in query param"})
    
    if 'current_order' not in input_params:
        return build_response(400, {"error": True, "description": "current_order is mandatory in query param"})
    
    try:
        current_datetime = datetime.strptime(input_params['current_datetime'], '%Y-%m-%d %H:%M')
        current_order = int(input_params['current_order'])
    except Exception as e:
        return build_response(400, {"error": True, "description": "current_datetime does not has a correct format"})

    try:
        cur_date = current_datetime.date()
        cur_time = current_datetime.time()
        
        schedule = session.query(Schedule).filter(
            and_(
                Schedule.date == cur_date,
                between(cur_time, Schedule.start, Schedule.end)
            )).first()
        
        if schedule is None:
            dof = int(cur_date.strftime("%w"))
            schedules = session.query(Schedule).filter(between(cur_time, Schedule.start, Schedule.end)).all()
            schedules = list(filter(lambda s: False if s.days is None else dof in json.loads(s.days), schedules))
            
            if len(schedules) < 1:
                raise APIException("No hay videos configurados para esta hora")
            schedule = schedules[0]
        order_path = os.path.abspath(os.path.join(current_app.root_path, 'static/', schedule.playlist.order_file))
        with open(order_path, 'r') as file:
            order = json.load(file)
        
        order_index = current_order + 1
        if order_index >= len(order):
            order_index = 0
        video = order[order_index]
        
        video['order'] = order_index
        response = json.dumps(video, cls=AlchemyEncoder)
        status_code = HTTPStatusCode.OK.value
    except APIException as e:
        logging.exception("APIException occurred")
        response = json.dumps(e.to_dict())
        status_code = e.status_code
    except Exception:
        logging.exception("No se pudo realizar la consulta")
        body = dict(message="No se pudo realizar la consulta")
        response = json.dumps(body)
        status_code=HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    
    return build_response(status_code, response, is_body_str=True)