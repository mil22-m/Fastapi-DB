from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class ClienteBase(SQLModel):
    nombre: str
    email: str = Field(index=True, unique=True)
    telefono: Optional[str] = None

class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    facturas: List["Factura"] = Relationship(back_populates="cliente")

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id: int

class FacturaBase(SQLModel):
    monto: float
    descripcion: str
    cliente_id: int = Field(foreign_key="cliente.id")

class Factura(FacturaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente: Optional[Cliente] = Relationship(back_populates="facturas")

class FacturaCreate(FacturaBase):
    pass

class FacturaRead(FacturaBase):
    id: int