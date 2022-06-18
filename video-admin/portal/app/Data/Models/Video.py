import os
from flask import current_app
from typing import Any, Dict, List
from sqlalchemy.orm.session import Session
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
    thumb_file = Column("thumb_file", String)
    size = Column("size", Integer)
    format = Column("format", String)
    
    model_path_name = "video"
    
    search_columns = ['video_file', 'format']
    
    def property_map(self) -> Dict:
        return { }
    
    @classmethod
    def display_members(cls_) -> List[str]:
        return [
            "id", "video_file", "thumb_file", "description", "size", "format"
        ]
    
    def before_delete(self, sesion: Session, *args, **kwargs):
        output_videopath = os.path.abspath(os.path.join(current_app.root_path, 'static/', self.video_file))
        output_videothumb = os.path.abspath(os.path.join(current_app.root_path, 'static/', self.thumb_file))
        
        if os.path.exists(output_videopath):
            os.remove(output_videopath)
        if os.path.exists(output_videothumb):
            os.remove(output_videothumb)
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "video_file": ["required", "string"]
        }
