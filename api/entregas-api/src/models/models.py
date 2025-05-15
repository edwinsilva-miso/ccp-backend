from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Delivery(db.Model):
    """
    Delivery model representing a delivery from a seller to a customer.
    """
    __tablename__ = 'deliveries'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False, index=True)
    seller_id = db.Column(db.Integer, nullable=False, index=True)
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
            'id': self.id,
            'customer_id': self.customer_id,
            'seller_id': self.seller_id,
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

    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StatusUpdate {self.id} for delivery {self.delivery_id}: {self.status}>'

    def to_dict(self):
        """Convert status update to dictionary."""
        return {
            'id': self.id,
            'delivery_id': self.delivery_id,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }