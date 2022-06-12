from typing import Any, Dict, List
from sqlalchemy import Column, Integer, String
from ...Core.Data.BaseModel import BaseModel

class Video(BaseModel):
    """ Table videos Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Video: Instance of model
    """
    __tablename__ = 'videos'
    id = Column("id", Integer, primary_key=True)
    video_file = Column("video_file", String, nullable=False)
    description = Column("description", String)
    size = Column("size", Integer)
    format = Column("format", String)
    
    model_path_name = "video"
    
    def property_map(self) -> Dict:
        return { }
    
    def display_members(self) -> List[str]:
        return [
            "id", "video_file", "description", "size", "format"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "video_file": ["required", "string"]
        }
