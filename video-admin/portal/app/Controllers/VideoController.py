import subprocess
import tempfile
from portal.app.Core.Controllers.BaseController import index, find, delete

import os
import json
import shutil
from typing import cast
from flask import render_template, request, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from portal.app.Data.Enum.http_status_code import HTTPStatusCode

from portal.app.Exceptions.APIException import APIException
from portal.app.Services.VideoService import VideoService
from portal.database.DBConnection import AlchemyEncoder, AlchemyRelationEncoder, get_session
from portal.utils.http_utils import build_response

def __get_temp_file_dir(filename: str) -> str:
    return os.path.abspath(os.path.join(tempfile.gettempdir(), filename))

def upload(service: VideoService):
    session = get_session()
    
    if 'file' not in request.files:
        return build_response(HTTPStatusCode.UNPROCESABLE_ENTITY.value, {"error": True})
    file = cast(FileStorage, request.files['file'])
    filename = secure_filename(file.filename)
    
    temp_filepath = __get_temp_file_dir(filename)
    file.save(temp_filepath)
    
    thumbnail_name =f'{filename.split(".")[0]}_thumbnail.png'
    thumbnail_file = __get_temp_file_dir(thumbnail_name)
    size = os.stat(temp_filepath).st_size
    cmd = f'ffmpeg -i "{temp_filepath}" -ss 00:00:01.000 -vframes 1  -s 640x360  "{thumbnail_file}"'
    subprocess.check_output(cmd, shell=True)
    
    output_videopath = os.path.abspath(os.path.join(current_app.root_path, 'static/videos/', filename))
    output_videothumb = os.path.abspath(os.path.join(current_app.root_path, 'static/thumbnails/', thumbnail_name))
    shutil.copy(thumbnail_file, output_videothumb)
    shutil.copy(temp_filepath, output_videopath)
    
    return build_response(HTTPStatusCode.OK.value, {"error": False})
    
    """
    try:
        body = service.insert_register(session, input_params)
        response = json.dumps(body, cls=AlchemyEncoder)
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
    """
