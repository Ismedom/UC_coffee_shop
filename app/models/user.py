from sqlalchemy.sql import func
from app.database import Base
from app.utils.security import hash_password
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import  relationship

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    _password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    roles = relationship("Role", secondary=user_roles, back_populates="users", lazy="selectin")
    orders = relationship("PurchaseOrder", back_populates="user", lazy="selectin", cascade="all, delete-orphan")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext: str):
        """Automatically hash the password when set"""
        self._password = hash_password(plaintext)

    def to_dict(self):
        """Return a dictionary of user data without password"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at,
        }

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles", lazy="selectin")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    resource = Column(String)
    action = Column(String)
    
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions", lazy="selectin")

