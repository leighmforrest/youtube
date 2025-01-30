from datetime import datetime

from sqlalchemy import TIMESTAMP, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from youtube.db import CustomBase


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False, index=True
    )


class Channel(CustomBase, CreatedAtMixin):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    handle: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    youtube_channel_id: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    uploads_playlist: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    videos: Mapped[list["Video"]] = relationship("Video", back_populates="channel")
    channel_stats: Mapped[list["ChannelStats"]] = relationship(
        "ChannelStats", back_populates="channel"
    )

    def __str__(self) -> str:
        return f"<Channel: {self.handle or 'Unknown'}>"

    @classmethod
    def get_by_handle(cls, session: Session, handle: str) -> "Channel":
        """Find a channel by its handle"""
        result = session.query(cls).filter(cls.handle == handle).first()

        if not result:
            raise ValueError(f"Channel with handle {handle} not found.")
        return result


class Video(CustomBase, CreatedAtMixin):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("channel.id"), nullable=False
    )
    youtube_video_id: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True
    )
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    channel: Mapped["Channel"] = relationship("Channel", back_populates="videos")
    video_stats: Mapped[list["VideoStats"]] = relationship(
        "VideoStats", back_populates="video", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"<Video: {self.title or 'Untitled'}>"

    @classmethod
    def get_by_youtube_video_id(
        cls, session: Session, youtube_video_id: str
    ) -> "Video":
        """Find a video by its youtube_video_id"""
        result = (
            session.query(cls).filter(cls.youtube_video_id == youtube_video_id).first()
        )

        if not result:
            raise ValueError(
                f"Video with youtube_video_id {youtube_video_id} not found."
            )
        return result


class ChannelStats(CustomBase, CreatedAtMixin):
    __tablename__ = "channel_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("channel.id"), nullable=False
    )
    view_count: Mapped[int] = mapped_column(Integer, nullable=False)
    subscriber_count: Mapped[int] = mapped_column(Integer, nullable=False)
    video_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    channel: Mapped["Channel"] = relationship("Channel", back_populates="channel_stats")

    def __str__(self) -> str:
        return f"<ChannelStats: {self.channel.handle if self.channel else 'Unknown'}>"


class VideoStats(CustomBase, CreatedAtMixin):
    __tablename__ = "video_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    video_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("video.id"), nullable=False
    )
    view_count: Mapped[int] = mapped_column(Integer, nullable=False)
    like_count: Mapped[int] = mapped_column(Integer, nullable=False)
    favorite_count: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    video: Mapped["Video"] = relationship("Video", back_populates="video_stats")

    def __str__(self) -> str:
        return f"<VideoStats: {self.video.title if self.video else 'Unknown'}>"
