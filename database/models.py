from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey, CheckConstraint, Identity
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import types
from sqlalchemy import func

from . import base


class User(base.BaseModel):

    __tablename__ = 'users'

    id: base.Integer = Column(types.BigInteger, nullable=False, primary_key=True)
    username: base.String = Column(types.String, nullable=False)
    balance: base.Float = Column(types.Numeric(7, 2, asdecimal=False), CheckConstraint('balance >= 0'), default=0)
    privilege: base.String = Column(types.String, default='default')
    expires_in: base.String = Column(types.DateTime, default=datetime.min)
    registration: base.DateTime = Column(types.DateTime, default=func.now())
    role: base.String = Column(types.String, default='user')


class Group(base.BaseModel):

    __tablename__ = 'groups'

    id: base.Integer = Column(types.BigInteger, nullable=False, primary_key=True)
    username: base.String = Column(types.String, nullable=False)
    privilege: base.String = Column(types.String, default='default')
    expires_in: base.String = Column(types.DateTime, default=datetime.min)
    registration: base.DateTime = Column(types.DateTime, default=func.now())


class Replenishment(base.BaseModel):

    __tablename__ = 'replenishment'

    id: base.Integer = Column(types.BigInteger, Identity(True, start=1, increment=1), nullable=False, primary_key=True)
    order_id: base.UUID = Column(UUID(as_uuid=True), nullable=False)
    user_id: base.Integer = Column(types.BigInteger, ForeignKey('users.id'), nullable=False)
    amount: base.Float = Column(types.Numeric(7, 2, asdecimal=False), nullable=False)
    status: base.String = Column(types.String, default='wait')
    created_at: base.DateTime = Column(types.DateTime, default=func.now())
