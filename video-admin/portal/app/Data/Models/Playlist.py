from typing import Any, Dict, List
from sqlalchemy import Column, Integer, String
from ...Core.Data.BaseModel import BaseModel

class Playlist(BaseModel):
    """ Table Playlists Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Playlist: Instance of model
    """
    __tablename__ = 'Playlists'
    id = Column("IdPlaylist", Integer, primary_key=True)
    Description = Column("Description", String, nullable=False)
    
    model_path_name = "playlist"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdPlaylist"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Description"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "Description": ["required", "string"]
        }
