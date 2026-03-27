from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Float, Text, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(255), nullable=True, unique=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    referral_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    __table_args__ = (
        Index('idx_users_telegram_id', 'telegram_id'),
    )


class ProfileModel(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    city = Column(String(255), nullable=True)
    interests = Column(ARRAY(Text), nullable=True, default=[])
    photos_count = Column(Integer, default=0)
    fullness_percent = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_profiles_user_id', 'user_id'),
        Index('idx_profiles_gender_city', 'gender', 'city'),
    )