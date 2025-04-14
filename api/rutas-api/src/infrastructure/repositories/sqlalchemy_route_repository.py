from typing import List, Optional, Union, Dict, Any
from uuid import UUID
import datetime

from sqlalchemy import Column, String, Float, ForeignKey, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from src.domain.models.route import Route, Waypoint
from src.domain.repositories.route_repository import RouteRepository

Base = declarative_base()


class SQLAlchemyWaypoint(Base):
    __tablename__ = "waypoints"

    id = Column(PgUUID(as_uuid=True), primary_key=True)
    route_id = Column(
        PgUUID(as_uuid=True),
        ForeignKey("routes.id", ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class SQLAlchemyRoute(Base):
    __tablename__ = "routes"

    id = Column(PgUUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(PgUUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    waypoints = relationship("SQLAlchemyWaypoint", cascade="all, delete-orphan", backref="route",
                             order_by="SQLAlchemyWaypoint.order")


class SQLAlchemyRouteRepository(RouteRepository):
    """
    SQLAlchemy implementation of the RouteRepository interface.
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, route: Route) -> Route:
        # Convert domain model to SQLAlchemy model
        db_route = SQLAlchemyRoute(
            id=route.id,
            name=route.name,
            description=route.description,
            user_id=route.user_id,
            created_at=route.created_at,
            updated_at=route.updated_at,
        )

        # Add and commit the route to get its ID
        self.session.add(db_route)
        self.session.flush()  # Flush to get the ID without committing yet

        # Now add the waypoints with the route ID
        for i, waypoint in enumerate(route.waypoints):
            db_waypoint = SQLAlchemyWaypoint(
                id=waypoint.id,
                route_id=db_route.id,
                name=waypoint.name,
                latitude=waypoint.latitude,
                longitude=waypoint.longitude,
                address=waypoint.address,
                order=i,
                created_at=waypoint.created_at,
            )
            self.session.add(db_waypoint)

        # Commit all changes
        self.session.commit()

        # Get the newly created route with waypoints
        return self._to_domain(db_route)

    def get_by_id(self, route_id: UUID) -> Optional[Route]:
        db_route = self.session.query(SQLAlchemyRoute).filter(SQLAlchemyRoute.id == route_id).first()
        if not db_route:
            return None
        return self._to_domain(db_route)

    def get_all(self, user_id: Optional[UUID] = None) -> List[Route]:
        query = self.session.query(SQLAlchemyRoute)
        if user_id:
            query = query.filter(SQLAlchemyRoute.user_id == user_id)

        routes = []
        for db_route in query.all():
            routes.append(self._to_domain(db_route))

        return routes

    def update(self, route_id: UUID, route_data: Union[Route, dict]) -> Optional[Route]:
        db_route = self.session.query(SQLAlchemyRoute).filter(SQLAlchemyRoute.id == route_id).first()
        if not db_route:
            return None

        data = route_data
        if isinstance(route_data, Route):
            # Convert domain model to dict
            data = {
                "name": route_data.name,
                "description": route_data.description,
                "updated_at": datetime.datetime.utcnow(),
            }

        # Update route attributes
        for key, value in data.items():
            if key != "waypoints" and hasattr(db_route, key):
                setattr(db_route, key, value)

        # Handle waypoints separately
        if "waypoints" in data:
            # Delete existing waypoints
            self.session.query(SQLAlchemyWaypoint).filter(
                SQLAlchemyWaypoint.route_id == route_id
            ).delete()

            # Add new waypoints
            waypoints = data["waypoints"]
            for i, wp in enumerate(waypoints):
                waypoint_data = wp
                if isinstance(wp, Waypoint):
                    waypoint_data = {
                        "id": wp.id,
                        "name": wp.name,
                        "latitude": wp.latitude,
                        "longitude": wp.longitude,
                        "address": wp.address,
                        "created_at": wp.created_at,
                    }

                db_waypoint = SQLAlchemyWaypoint(
                    id=waypoint_data.get("id", UUID()),
                    route_id=route_id,
                    name=waypoint_data["name"],
                    latitude=waypoint_data["latitude"],
                    longitude=waypoint_data["longitude"],
                    address=waypoint_data.get("address"),
                    order=i,
                    created_at=waypoint_data.get("created_at", datetime.datetime.utcnow()),
                )
                self.session.add(db_waypoint)

        self.session.commit()
        return self.get_by_id(route_id)

    def delete(self, route_id: UUID) -> bool:
        db_route = self.session.query(SQLAlchemyRoute).filter(SQLAlchemyRoute.id == route_id).first()
        if not db_route:
            return False

        self.session.delete(db_route)
        self.session.commit()
        return True

    def _to_domain(self, db_route: SQLAlchemyRoute) -> Route:
        """Convert SQLAlchemy model to domain model"""
        waypoints = []
        for db_waypoint in sorted(db_route.waypoints, key=lambda wp: wp.order):
            waypoint = Waypoint(
                id=db_waypoint.id,
                name=db_waypoint.name,
                latitude=db_waypoint.latitude,
                longitude=db_waypoint.longitude,
                address=db_waypoint.address,
                created_at=db_waypoint.created_at,
            )
            waypoints.append(waypoint)

        return Route(
            id=db_route.id,
            name=db_route.name,
            description=db_route.description,
            user_id=db_route.user_id,
            created_at=db_route.created_at,
            updated_at=db_route.updated_at,
            waypoints=waypoints,
        )
