from typing import List, Optional
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
import uuid

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

class User(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    configs: Mapped[List["UserConfig"]] = relationship(back_populates='user', cascade="all, delete", passive_deletes=True)
    is_admin: Mapped[bool] = mapped_column(Boolean)
    key: Mapped["UserAccessKey"] = relationship("UserAccessKey", back_populates='user', uselist=False, cascade="all, delete")

class UserAccessKey(Base):
    __tablename__ = 'user_keys'
    key: Mapped[str] = mapped_column(String(255), primary_key=True, unique=True)
    telegram_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey('users.telegram_id', ondelete='CASCADE'), unique=True, nullable=True, default=None)
    user: Mapped["User"] = relationship("User", back_populates='key')

class UserConfig(Base):
    __tablename__ = 'user_configs'
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    config_name: Mapped[str] = mapped_column(String(64))
    server_id: Mapped[int] = mapped_column(Integer, ForeignKey('servers.id', ondelete='CASCADE'))
    telegram_id: Mapped[str] = mapped_column(String, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    expire_date: Mapped[int] = mapped_column(Integer)
    limit: Mapped[int] = mapped_column(Integer)
    server: Mapped["Server"] = relationship(back_populates='configs')
    user: Mapped['User'] = relationship(back_populates='configs')

class Server(Base):
    __tablename__ = 'servers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    server_host: Mapped[str] = mapped_column(String(255))
    server_port: Mapped[int] = mapped_column(Integer)
    server_webpath: Mapped[str] = mapped_column(String(255))
    server_login: Mapped[str] = mapped_column(String(255))
    server_password: Mapped[str] = mapped_column(String(255))
    default_inbound: Mapped[Optional[int]] = mapped_column(Integer)
    # inbound_stream_settings: Mapped[Optional[str]] = mapped_column(String(1024))
    configs: Mapped[List["UserConfig"]] = relationship(back_populates='server', cascade="all, delete", passive_deletes=True)
