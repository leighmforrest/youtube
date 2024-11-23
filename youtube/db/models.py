from datetime import datetime, timezone, timedelta
from typing import List
from sqlalchemy import ForeignKey, String, TIMESTAMP, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


one_day_ago = lambda: datetime.now(timezone.utc) - timedelta(days=1)


class Base(DeclarativeBase):
    pass


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )


class Channel(Base, CreatedAtMixin):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    upload_playlist: Mapped[str] = mapped_column(String, nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String, nullable=True)

    statistics: Mapped[List["ChannelStatistics"]] = relationship(
        "ChannelStatistics", back_populates="channel"
    )

    def __str__(self) -> str:
        return self.channel_id

    def get_fresh_statistics(self, session: Session):
        statistics = (
            session.query(ChannelStatistics)
            .filter(
                ChannelStatistics.channel_id == self.id,
                ChannelStatistics.created_at >= one_day_ago(),
            )
            .all()
        )

        return statistics


class ChannelStatistics(Base, CreatedAtMixin):
    __tablename__ = "channel_statistics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subscriber_count: Mapped[int] = mapped_column(nullable=False)
    video_count: Mapped[int] = mapped_column(nullable=False)
    view_count: Mapped[int] = mapped_column(nullable=False)

    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("channel.id"))
    channel: Mapped["Channel"] = relationship("Channel", back_populates="statistics")


class Video(Base, CreatedAtMixin):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    published_at: Mapped[datetime] = mapped_column(nullable=False)

    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("channel.id"))
    channel: Mapped["Channel"] = relationship("Channel", back_populates="videos")


class VideoStatistics(Base, CreatedAtMixin):
    __tablename__ = "video_statistics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subscriber_count: Mapped[int] = mapped_column(nullable=False)
    like_count: Mapped[int] = mapped_column(nullable=False)
    comment_count: Mapped[int] = mapped_column(nullable=False)
    view_count: Mapped[int] = mapped_column(nullable=False)

    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("video.id"))
    video: Mapped["Video"] = relationship("Video", back_populates="statistics")
