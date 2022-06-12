from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from ...Core.Data.BaseModel import BaseModel

class Playlist(BaseModel):
    """ Table playlists Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Playlist: Instance of model
    """
    __tablename__ = 'playlists'
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    order_file = Column("order_file", String, nullable=False)
    description = Column("description", String)
    
    schedules = relationship("Schedule", back_populates="playlist")
    
    model_path_name = "playlist"
    
    filter_columns = []
    relationship_names = ["schedules"]
    search_columns = ["name"]
    
    def property_map(self) -> Dict:
        return { }
    
    def display_members(self) -> List[str]:
        return [
            "id", "name", "description", "order_file"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "name": ["required", "string"],
            "order_file": ["required", "string"]
        }
