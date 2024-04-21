import sqlalchemy as sa
from datetime import datetime

from core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    first_name = sa.Column(sa.String(100))
    last_name = sa.Column(sa.String(100))
    email = sa.Column(sa.String(255), unique=True, index=True)
    password = sa.Column(sa.String(255))
    is_active = sa.Column(sa.Boolean, default=False)
    is_verified = sa.Column(sa.Boolean, default=False)
    verified_at = sa.Column(sa.DateTime, nullable=True, default=None)
    registered_at = sa.Column(sa.DateTime, nullable=True, default=None)
    updated_at = sa.Column(sa.DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())