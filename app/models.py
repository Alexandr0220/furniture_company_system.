from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProductType(Base):
    __tablename__ = "product_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    loss_percent = Column(Float, nullable=False, default=0.0)

class Workshop(Base):
    __tablename__ = "workshops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    workers_count = Column(Integer, nullable=False, default=0)
    time_min = Column(Integer, nullable=False, default=0)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    article = Column(String, nullable=True)
    name = Column(String, nullable=False)
    min_price = Column(Float, nullable=False, default=0.0)

    product_type_id = Column(Integer, ForeignKey("product_types.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)

    product_type = relationship("ProductType")
    material = relationship("Material")

class ProductWorkshop(Base):
    __tablename__ = "product_workshops"
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), primary_key=True)
    time_min = Column(Integer, nullable=False, default=0)

    product = relationship("Product")
    workshop = relationship("Workshop")
