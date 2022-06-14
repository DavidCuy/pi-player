from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey
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
    start = Column("start", Time, nullable=False)
    end = Column("end", Time, nullable=False)
    date = Column("date", Date)
    days = Column("days", String)
    
    playlist = relationship("Playlist", back_populates="schedules")
    
    filter_columns = ["id_playlist"]
    relationship_names = ["playlist"]
    search_columns = ["name", "days"]
    
    model_path_name = "schedule"
    
    def property_map(self) -> Dict:
        return { }
    
    def display_members(self) -> List[str]:
        return [
            "id", "id_playlist", "name", "start", "end", "date", "days"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "id_playlist": ["required"],
            "start": ["required"],
            "end": ["required"],
            "name": ["required", "string"]
        }
