from email.policy import default
from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Time, Date, Boolean, ForeignKey
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
    start = Column("start", Time, nullable=False)
    end = Column("end", Time, nullable=False)
    repeat = Column("repeat", Boolean, default=False)
    date = Column("date", Date)
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
            "id", "id_playlist", "name", "color", "start", "end", "date", "days"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "id_playlist": ["required"],
            "start": ["required"],
            "end": ["required"],
            "name": ["required", "string"]
        }
