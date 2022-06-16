from flask import Blueprint
from portal.app.Controllers.VideoController import index, find, delete, upload
from portal.app.Services import VideoService

video_router = Blueprint('video', __name__)
video_service = VideoService()

video_router.route('/', methods=['GET'], defaults={'service': video_service}) (index)
video_router.route('/<id>', methods=['GET'], defaults={'service': video_service}) (find)
video_router.route('/<id>', methods=['DELETE'], defaults={'service': video_service}) (delete)

video_router.route('/upload', methods=['POST'], defaults={'service': video_service}) (upload)