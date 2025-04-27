from typing import List, Optional, Union, Dict, Any
from uuid import UUID, uuid4
import datetime
import logging

from sqlalchemy import Column, String, Float, ForeignKey, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from ...domain.entities.route import Route
from ...domain.entities.waypoint import Waypoint
from ...domain.repositories.route_repository import RouteRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
        logger.info("Starting `create` method for route: %s", route)

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

        logger.info("Route created in temporary state with ID: %s", db_route.id)

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

        logger.info("Route and all its waypoints committed successfully with ID: %s", db_route.id)

        # Get the newly created route with waypoints
        return self._to_domain(db_route)

    def get_by_id(self, route_id: UUID) -> Optional[Route]:
        logger.info("Fetching route by ID: %s", route_id)

        db_route = self.session.query(SQLAlchemyRoute).filter(SQLAlchemyRoute.id == route_id).first()
        if not db_route:
            logger.warning("Route with ID %s not found.", route_id)
            return None

        logger.info("Route with ID %s found.", route_id)

        return self._to_domain(db_route)

    def get_all(self, user_id: Optional[UUID] = None) -> List[Route]:
        logger.info("Fetching all routes for user_id: %s", user_id)

        query = self.session.query(SQLAlchemyRoute)
        if user_id:
            query = query.filter(SQLAlchemyRoute.user_id == user_id)

        routes = []
        for db_route in query.all():
            routes.append(self._to_domain(db_route))

        logger.info("Fetched %d routes.", len(routes))

        return routes

    def update(self, route_id: UUID, route_data: Union[Route, dict]) -> Optional[Route]:
        logger.info("Starting `update` method for route ID: %s with data: %s", route_id, route_data)

        db_route = self.session.query(SQLAlchemyRoute).filter(SQLAlchemyRoute.id == route_id).first()
        if not db_route:
            logger.warning("Route with ID %s not found for update.", route_id)
            return None

        logger.debug("Current details of db_route: %s", db_route)

        data = route_data
        if isinstance(route_data, Route):
            data = {
                "name": route_data.name,
                "description": route_data.description,
                "updated_at": datetime.datetime.utcnow(),
                "waypoints": route_data.waypoints,
            }

        for key, value in data.items():
            if key != "waypoints" and hasattr(db_route, key):
                logger.debug("Updated attribute `%s` to `%s`.", key, value)
                setattr(db_route, key, value)

        db_route.id = route_id
        logger.debug("route id::`%s`", route_id)

        if "waypoints" in data:
            logger.debug("Handling waypoints update for route ID: %s", route_id)

            new_waypoints = data["waypoints"]

            existing_waypoints = {wp.id: wp for wp in db_route.waypoints}

            updated_waypoints = []
            for i, waypoint in enumerate(new_waypoints):
                waypoint_data = waypoint
                if isinstance(waypoint, Waypoint):
                    waypoint_data = {
                        "id": waypoint.id,
                        "name": waypoint.name,
                        "latitude": waypoint.latitude,
                        "longitude": waypoint.longitude,
                        "address": waypoint.address,
                        "created_at": waypoint.created_at,
                    }

                waypoint_id = waypoint_data.get("id")
                if waypoint_id and waypoint_id in existing_waypoints:
                    existing_wp = existing_waypoints[waypoint_id]
                    existing_wp.name = waypoint_data["name"]
                    existing_wp.latitude = waypoint_data["latitude"]
                    existing_wp.longitude = waypoint_data["longitude"]
                    existing_wp.address = waypoint_data.get("address")
                    existing_wp.order = i
                    updated_waypoints.append(existing_wp)

                    logger.debug("Updated existing waypoint with ID: %s", waypoint_id)
                else:
                    db_waypoint = SQLAlchemyWaypoint(
                        id=waypoint_id if waypoint_id else uuid4(),
                        route_id=route_id,
                        name=waypoint_data["name"],
                        latitude=waypoint_data["latitude"],
                        longitude=waypoint_data["longitude"],
                        address=waypoint_data.get("address"),
                        order=i,
                        created_at=waypoint_data.get("created_at", datetime.datetime.utcnow()),
                    )
                    updated_waypoints.append(db_waypoint)
                    logger.debug("Created new waypoint: %s", db_waypoint)

            db_route.waypoints = updated_waypoints
            logger.info("Waypoints updated successfully: %s", updated_waypoints)

            current_wp_ids = {wp.get("id") if isinstance(wp, dict) else wp.id for wp in new_waypoints}
            for old_wp in existing_waypoints.values():
                if old_wp.id not in current_wp_ids:
                    self.session.delete(old_wp)

        try:
            self.session.commit()
        except Exception as e:
            logger.error("Error updating route: %s", e.__traceback__)
            logger.debug("Exception stack trace:", exc_info=True)

            self.session.rollback()
            raise e

        return self.get_by_id(route_id)

    def delete(self, route_id: UUID) -> bool:
        logger.info("Starting `delete` method for route ID: %s", route_id)

        db_route = self.session.query(SQLAlchemyRoute).filter(SQLAlchemyRoute.id == route_id).first()
        if not db_route:
            logger.warning("Route with ID %s not found.", route_id)

            return False

        self.session.delete(db_route)
        self.session.commit()

        logger.info("Route with ID %s deleted successfully.", route_id)
        return True

    def _to_domain(self, db_route: SQLAlchemyRoute) -> Route:
        """Convert SQLAlchemy model to domain model"""
        logger.debug("Converting SQLAlchemyRoute to Route domain model for ID: %s", db_route.id)

        waypoints = []
        for db_waypoint in sorted(db_route.waypoints, key=lambda wp: wp.order):
            waypoint = Waypoint(
                id=db_waypoint.id,
                name=db_waypoint.name,
                latitude=db_waypoint.latitude,
                longitude=db_waypoint.longitude,
                address=db_waypoint.address,
                created_at=db_waypoint.created_at,
                order=db_waypoint.order,
            )
            waypoints.append(waypoint)

        logger.debug("Converted %d waypoints for route ID: %s", len(waypoints), db_route.id)

        return Route(
            id=db_route.id,
            name=db_route.name,
            description=db_route.description,
            user_id=db_route.user_id,
            created_at=db_route.created_at,
            updated_at=db_route.updated_at,
            waypoints=waypoints,
        )
