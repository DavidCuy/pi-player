from datetime import datetime
from email.policy import default
from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.dialects.sqlite import DATE, TIME
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from ...Core.Data.BaseModel import BaseModel

class Schedule(BaseModel):
    """ Table schedules Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Schedule: Instance of model
    """
    __tablename__ = 'schedules'
    id = Column("id", Integer, primary_key=True)
    id_playlist = Column("id_playlist", Integer, ForeignKey("playlists.id"), nullable=False)
    name = Column("name", String, nullable=False)
    color = Column("color", String, default="#CCCCCC")
    start = Column("start", TIME, nullable=False)
    end = Column("end", TIME, nullable=False)
    repeat = Column("repeat", Boolean, default=False)
    date = Column("date", DATE)
    days = Column("days", String)
    
    playlist = relationship("Playlist", back_populates="schedules")
    
    filter_columns = ["id_playlist"]
    relationship_names = ["playlist"]
    search_columns = ["name", "days", "color"]
    
    model_path_name = "schedule"
    
    def property_map(self) -> Dict:
        return { }
    
    @classmethod
    def display_members(cls_) -> List[str]:
        return [
            "id", "id_playlist", "name", "color", "start", "end", "repeat", "date", "days"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "id_playlist": ["required"],
            "start": ["required"],
            "end": ["required"],
            "name": ["required", "string"]
        }
    
    def before_save(self, sesion: Session, *args, **kwargs):
        self.start = datetime.strptime(self.start, '%H:%M').time()
        self.end = datetime.strptime(self.end, '%H:%M').time()
        if self.repeat is True:
            self.date = None
            if type(self.days) is list:
                self.days = str(list(map(lambda d: int(d), self.days)))
        else:
            self.days = None
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
        
