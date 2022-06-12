from flask import Blueprint
from portal.app.Controllers.PlaylistController import index, find, store, update, delete
from portal.app.Services import PlaylistService

playlist_router = Blueprint('playlist', __name__)
playlist_service = PlaylistService()

playlist_router.route('/', methods=['GET'], defaults={'service': playlist_service}) (index)
playlist_router.route('/', methods=['POST'], defaults={'service': playlist_service}) (store)
playlist_router.route('/<id>', methods=['GET'], defaults={'service': playlist_service}) (find)
playlist_router.route('/<id>', methods=['PUT'], defaults={'service': playlist_service}) (update)
playlist_router.route('/<id>', methods=['DELETE'], defaults={'service': playlist_service}) (delete)