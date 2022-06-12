from portal.app.Core.Services.BaseService import BaseService
from portal.app.Data.Models import Schedule


class ScheduleService(BaseService):
    def __init__(self) -> None:
        super().__init__(Schedule)