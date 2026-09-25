from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from app.database import init_db, get_session
from app.models import (
    Cliente, ClienteCreate, ClienteRead,
    Factura, FacturaCreate, FacturaRead
)

app = FastAPI(
    title="API con AWS EC2 y Amazon RDS"
)

@app.on_event("startup")
def on_startup():
    init_db()

# --- CRUD CLIENTES ---
@app.post("/clientes/", response_model=ClienteRead, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_session)):
    db_cliente = Cliente.from_orm(cliente)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.get("/clientes/", response_model=List[ClienteRead])
def listar_clientes(db: Session = Depends(get_session)):
    return db.exec(select(Cliente)).all()

@app.get("/clientes/{cliente_id}", response_model=ClienteRead)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_session)):
    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.put("/clientes/{cliente_id}", response_model=ClienteRead)
def actualizar_cliente(cliente_id: int, datos: ClienteCreate, db: Session = Depends(get_session)):
    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for key, value in datos.dict().items():
        setattr(cliente, key, value)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_session)):
    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(cliente)
    db.commit()
    return {"message": f"Cliente {cliente_id} eliminado exitosamente"}

# --- CRUD FACTURAS ---
@app.post("/facturas/", response_model=FacturaRead, status_code=201)
def crear_factura(factura: FacturaCreate, db: Session = Depends(get_session)):
    cliente = db.get(Cliente, factura.cliente_id)
    if not cliente:
        raise HTTPException(status_code=400, detail="El cliente especificado no existe")
    db_factura = Factura.from_orm(factura)
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura

@app.get("/facturas/", response_model=List[FacturaRead])
def listar_facturas(db: Session = Depends(get_session)):
    return db.exec(select(Factura)).all()