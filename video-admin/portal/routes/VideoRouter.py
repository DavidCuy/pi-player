from flask import Blueprint
from portal.app.Controllers.VideoController import index, find, store, update, delete
from portal.app.Services import VideoService

video_router = Blueprint('video', __name__)
video_service = VideoService()

video_router.route('/', methods=['GET'], defaults={'service': video_service}) (index)
video_router.route('/', methods=['POST'], defaults={'service': video_service}) (store)
video_router.route('/<id>', methods=['GET'], defaults={'service': video_service}) (find)
video_router.route('/<id>', methods=['PUT'], defaults={'service': video_service}) (update)
video_router.route('/<id>', methods=['DELETE'], defaults={'service': video_service}) (delete)