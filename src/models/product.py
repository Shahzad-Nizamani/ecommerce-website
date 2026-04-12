from src.database.db_config import Base
from sqlalchemy import Column, Integer, String, text, Numeric

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Numeric, nullable=False)
    category = Column(String, nullable=False, index=True)
    image = Column(String)
    description = Column(text)
    stock = Column(Integer, nullable=False)