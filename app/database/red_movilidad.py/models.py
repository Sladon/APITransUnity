from typing import List, Optional, Set
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime, Bool
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from ...database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    direction: Mapped[int]
    from_to: Mapped[str]
    start_time: Mapped[DateTime]
    end_time: Mapped[DateTime]
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))


class RoutePath(Base):
    __tablename__ = "route_paths"

    id: Mapped[int] = mapped_column(primary_key=True)
    step: Mapped[int]
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="route", cascade="all, delete-orphan")
    path: Mapped[List["RoutePath"]] = relationship(back_populates="route", cascade="all, delete-orphan")


class Bus(Base):
    __tablename__ = "buses"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str]
    url: Mapped[str]
    has_arrival: Mapped[bool] = mapped_column(Bool, default=False)
    routes: Mapped[List["Route"]] = relationship(back_populates="bus", cascade="all, delete-orphan")


class Stop(Base):
    __tablename__ = "stops"

    cod: Mapped[str] = mapped_column(primary_key=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    name: Mapped[str]
    commune: Mapped[str]
    buses: Mapped[List["BusStop"]] = relationship(back_populates="stop", cascade="all, delete-orphan")


class BusStop(Base):
    __tablename__ = "bus_stops"

    id: Mapped[int] = mapped_column(primary_key=True)
    bus_id: Mapped[int] = mapped_column(ForeignKey("buses.id"))
    stop_cod: Mapped[str] = mapped_column(ForeignKey("stops.cod"))

    bus: Mapped["Bus"] = relationship(back_populates="buses")
    stop: Mapped["Stop"] = relationship(back_populates="stops")
