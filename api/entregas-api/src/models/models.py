from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Delivery(db.Model):
    """
    Delivery model representing a delivery from a seller to a customer.
    """
    __tablename__ = 'deliveries'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = db.Column(UUID(as_uuid=True), nullable=False, index=True)
    seller_id = db.Column(UUID(as_uuid=True), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    estimated_delivery_date = db.Column(db.DateTime, nullable=True)

    # Relationship with StatusUpdate
    status_updates = db.relationship('StatusUpdate', backref='delivery', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Delivery {self.id} from seller {self.seller_id} to customer {self.customer_id}>'

    def to_dict(self):
        """Convert delivery to dictionary."""
        return {
            'id': str(self.id) if self.id else None,
            'customer_id': str(self.customer_id) if self.customer_id else None,
            'seller_id': str(self.seller_id) if self.seller_id else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'estimated_delivery_date': self.estimated_delivery_date.isoformat() if self.estimated_delivery_date else None,
            'status_updates': [update.to_dict() for update in self.status_updates]
        }

class StatusUpdate(db.Model):
    """
    StatusUpdate model representing a status update for a delivery.
    """
    __tablename__ = 'status_updates'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_id = db.Column(UUID(as_uuid=True), db.ForeignKey('deliveries.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StatusUpdate {self.id} for delivery {self.delivery_id}: {self.status}>'

    def to_dict(self):
        """Convert status update to dictionary."""
        return {
            'id': str(self.id) if self.id else None,
            'delivery_id': str(self.delivery_id) if self.delivery_id else None,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
