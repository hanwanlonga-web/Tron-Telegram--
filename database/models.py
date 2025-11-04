from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    membership_level = Column(String(20), default='free')  # free, basic, premium, vip
    query_count = Column(Integer, default=0)
    last_query_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    tx_hash = Column(String(100), unique=True)
    amount = Column(Float, nullable=False)
    membership_level = Column(String(20), nullable=False)
    status = Column(String(20), default='pending')  # pending, confirmed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime)

class TransactionMonitor(Base):
    __tablename__ = 'transaction_monitors'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    address = Column(String(34), nullable=False)
    monitor_type = Column(String(20), default='incoming')  # incoming, outgoing, both
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PriceAlert(Base):
    __tablename__ = 'price_alerts'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    symbol = Column(String(10), default='TRX')
    target_price = Column(Float, nullable=False)
    condition = Column(String(10), default='above')  # above, below
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
