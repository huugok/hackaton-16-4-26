# api/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from api.database import Base

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    texto_usuario = Column(String, index=True)
    resultado_ia = Column(Integer) # 0 o 1
    mensaje_devuelto = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)