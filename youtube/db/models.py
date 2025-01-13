from datetime import datetime, timedelta
from sqlalchemy import TIMESTAMP, Integer, DateTime, String, Text, select, exists
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from youtube.db import CustomBase


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False, index=True
    )


class Channel(CustomBase, CreatedAtMixin):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    handle: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    youtube_channel_id: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str] = mapped_column(String(255), nullable=True)
    uploads_playlist: Mapped[str] = mapped_column(String(255), nullable=True)

    def __str__(self):
        return f"<Channel: {self.handle}>"


class Video(CustomBase, CreatedAtMixin):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    youtube_video_id: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=True
    )
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str] = mapped_column(String(255), nullable=True)

    def __str__(self):
        return f"<Video: {self.title}>"


class ChannelStats(CustomBase, CreatedAtMixin):
    __tablename__ = "channel_stats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False)
    subscriber_count: Mapped[int] = mapped_column(Integer, nullable=False)
    video_count: Mapped[int] = mapped_column(Integer, nullable=False)

    def __str__(self):
        return f"<ChannelStats: {self.id}>"


class VideoStats(CustomBase, CreatedAtMixin):
    __tablename__ = "video_stats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False)
    like_count: Mapped[int] = mapped_column(Integer, nullable=False)
    favorite_count: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_count: Mapped[int] = mapped_column(Integer, nullable=False)

    def __str__(self):
        return f"<VideoStats: {self.id}>"
