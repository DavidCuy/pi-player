import json
import os
from flask import current_app
from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.session import Session

from portal.database.DBConnection import AlchemyEncoder
from ...Core.Data.BaseModel import BaseModel
from .ManyToMany.RelVideosPlaylist import videos_playlist_association_table
from .Video import Video

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
    videos = relationship("Video", secondary=videos_playlist_association_table)
    
    model_path_name = "playlist"
    
    filter_columns = []
    relationship_names = ["schedules", "videos"]
    search_columns = ["name"]
    
    def property_map(self) -> Dict:
        return { }
    
    @classmethod
    def display_members(cls_) -> List[str]:
        return [
            "id", "name", "description", "order_file"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "name": ["required", "string"]
        }
    
    def before_save(self, sesion: Session, *args, **kwargs):
        self.order_file = f'order_files/{self.name}.json'
    
    def after_save(self, sesion: Session, *args, **kwargs):
        self.order_file = f'order_files/{self.id}.json'
        if 'videos' in kwargs:
            videos_ids = list(map(lambda id: int(id), kwargs['videos']))
            videos = sesion.query(Video).filter(Video.id.in_(videos_ids)).all()
            self.videos = videos
        sesion.commit()
        
        order_path = os.path.abspath(os.path.join(current_app.root_path, 'static/', self.order_file))
        with open(order_path, 'w') as ofile:
            ofile.write(json.dumps(self.videos, cls=AlchemyEncoder))
    
    def before_delete(self, sesion: Session, *args, **kwargs):
        order_file = os.path.abspath(os.path.join(current_app.root_path, 'static/', self.order_file))
        
        if os.path.exists(order_file):
            os.remove(order_file)
