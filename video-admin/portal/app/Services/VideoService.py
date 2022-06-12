from portal.app.Core.Services.BaseService import BaseService
from portal.app.Data.Models import Video


class VideoService(BaseService):
    def __init__(self) -> None:
        super().__init__(Video)