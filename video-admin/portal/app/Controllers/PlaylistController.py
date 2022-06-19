from portal.app.Core.Controllers.BaseController import index, find, store, delete

import os
import json
import logging
from typing import cast

from portal.app.Data.Models.Playlist import Playlist
from portal.app.Services.PlaylistService import PlaylistService
from portal.database.DBConnection import AlchemyEncoder, get_session
from flask import current_app, request
from portal.app.Data.Enum.http_status_code import HTTPStatusCode

from portal.app.Exceptions.APIException import APIException
from portal.utils.http_utils import build_response

def update_orderFile(service: PlaylistService, id: int):    
    session = get_session()
    
    input_params = request.get_json()

    try:
        playlist = cast(Playlist, service.get_one(session, id))
        order_path = os.path.abspath(os.path.join(current_app.root_path, 'static/', playlist.order_file))
        with open(order_path, 'w') as ofile:
            ofile.write(json.dumps(input_params, cls=AlchemyEncoder))
        
        response = json.dumps({"update": True, "id": id}, cls=AlchemyEncoder)
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
