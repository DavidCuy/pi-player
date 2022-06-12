from flask import Blueprint
from portal.app.Controllers.ScheduleController import index, find, store, update, delete
from portal.app.Services import ScheduleService

schedule_router = Blueprint('schedule', __name__)
schedule_service = ScheduleService()

schedule_router.route('/', methods=['GET'], defaults={'service': schedule_service}) (index)
schedule_router.route('/', methods=['POST'], defaults={'service': schedule_service}) (store)
schedule_router.route('/<id>', methods=['GET'], defaults={'service': schedule_service}) (find)
schedule_router.route('/<id>', methods=['PUT'], defaults={'service': schedule_service}) (update)
schedule_router.route('/<id>', methods=['DELETE'], defaults={'service': schedule_service}) (delete)