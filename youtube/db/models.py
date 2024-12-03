from datetime import datetime
from typing import List

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.sql import func


class CustomBase(DeclarativeBase):
    pass


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False, index=True
    )


class Channel(CustomBase, CreatedAtMixin):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    youtube_channel_id: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    handle: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    upload_playlist: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String(512), nullable=True)

    videos: Mapped[List["Video"]] = relationship("Video", back_populates="channel")
    statistics: Mapped["ChannelStats"] = relationship(
        "ChannelStats", back_populates="channel", uselist=False
    )

    def __str__(self):
        return f"<Channel: {self.handle}>"

    @classmethod
    def get_by_handle(cls, session: Session, handle: str):
        result = session.query(cls).filter(cls.handle == handle).first()
        if not result:
            raise ValueError(f"Channel with handle '{handle}' not found.")
        return result


class ChannelStats(CustomBase, CreatedAtMixin):
    __tablename__ = "channel_stats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False)
    subscriber_count: Mapped[int] = mapped_column(Integer, nullable=False)
    video_count: Mapped[int] = mapped_column(Integer, nullable=False)

    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("channel.id"))
    channel: Mapped["Channel"] = relationship("Channel", back_populates="statistics")

    def __str__(self) -> str:
        return f"<Channel Statistics for {self.channel.handle}>"


class Video(CustomBase, CreatedAtMixin):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String(512), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    published_at: Mapped[datetime] = mapped_column(nullable=False)

    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("channel.id"))
    channel: Mapped["Channel"] = relationship("Channel", back_populates="videos")

    def __str__(self) -> str:
        return f"<Video: {self.title}>"
