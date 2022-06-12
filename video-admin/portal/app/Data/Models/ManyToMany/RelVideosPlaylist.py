from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from portal.app.Core.Data.BaseModel import BaseModel

videos_playlist_association_table = Table('rel_video_playlist', BaseModel.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_video", Integer, ForeignKey("videos.id")),
    Column("id_playlist", Integer, ForeignKey("playlists.id"))
)