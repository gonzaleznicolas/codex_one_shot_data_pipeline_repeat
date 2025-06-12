from __future__ import annotations

import datetime as dt
from typing import List

import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, Stock, Position, Price
from .indicators import calculate_indicators


class Pipeline:
    def __init__(self, symbols: List[str], start: str, end: str, db_path: str):
        self.symbols = symbols
        self.start = dt.datetime.fromisoformat(start)
        self.end = dt.datetime.fromisoformat(end)
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self._ensure_positions()
        self._ensure_stocks()

    def _ensure_positions(self):
        with Session(self.engine) as session:
            for name in ['long', 'short', 'cash']:
                if not session.query(Position).filter_by(name=name).first():
                    session.add(Position(name=name))
            session.commit()

    def _ensure_stocks(self):
        with Session(self.engine) as session:
            for symbol in self.symbols:
                if not session.query(Stock).filter_by(symbol=symbol).first():
                    session.add(Stock(symbol=symbol))
            session.commit()

    def run(self):
        fetch_start = self.start - dt.timedelta(days=30)
        fetch_end = self.end + dt.timedelta(days=1)
        for symbol in self.symbols:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=fetch_start, end=fetch_end, auto_adjust=False)
            if df.empty:
                continue
            df.index = df.index.tz_localize(None)
            df = df.reset_index()
            df = df[df['Date'] >= pd.Timestamp(self.start)]
            df = calculate_indicators(df)
            self._write_to_db(symbol, df)

    def _write_to_db(self, symbol: str, df: pd.DataFrame):
        with Session(self.engine) as session:
            stock = session.query(Stock).filter_by(symbol=symbol).one()
            pos_map = {p.name: p for p in session.query(Position).all()}
            for _, row in df.iterrows():
                price = Price(
                    stock_id=stock.id,
                    date=row['Date'].date(),
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=row['Volume'],
                    price_over_sma_30=row['price_over_sma_30'],
                    bb_pct=row['bb_pct'],
                    position_id=pos_map[row['suggested']].id,
                )
                session.add(price)
            session.commit()
