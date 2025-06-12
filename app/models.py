from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)

    prices = relationship('Price', back_populates='stock')

class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    prices = relationship('Price', back_populates='position')

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    price_over_sma_30 = Column(Float)
    bb_pct = Column(Float)
    position_id = Column(Integer, ForeignKey('positions.id'))

    stock = relationship('Stock', back_populates='prices')
    position = relationship('Position', back_populates='prices')
