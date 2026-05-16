from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# BASE DE DATOS
engine = create_engine("sqlite:///reportes.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# TEMPLATES
templates = Jinja2Templates(directory="templates")

# MODELO
class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descripcion = Column(String)
    ubicacion = Column(String)
    estado = Column(String)

Base.metadata.create_all(bind=engine)

# =========================
# VER REPORTES
# =========================
@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):

    db = SessionLocal()
    reportes = db.query(Reporte).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "reportes": reportes
        }
    )

# =========================
# CREAR REPORTE
# =========================
@app.post("/crear")
def crear(
    titulo: str = Form(...),
    descripcion: str = Form(...),
    ubicacion: str = Form(...)
):

    db = SessionLocal()

    nuevo = Reporte(
        titulo=titulo,
        descripcion=descripcion,
        ubicacion=ubicacion,
        estado="Pendiente"
    )

    db.add(nuevo)
    db.commit()

    return RedirectResponse("/", status_code=303)

# =========================
# FORMULARIO EDITAR
# =========================
@app.get("/editar/{id}", response_class=HTMLResponse)
def editar_form(request: Request, id: int):

    db = SessionLocal()

    reporte = db.query(Reporte).filter(Reporte.id == id).first()

    return templates.TemplateResponse(
        request=request,
        name="editar.html",
        context={
            "reporte": reporte
        }
    )

# =========================
# MODIFICAR REPORTE
# =========================
@app.post("/editar/{id}")
def editar(
    id: int,
    titulo: str = Form(...),
    descripcion: str = Form(...),
    ubicacion: str = Form(...),
    estado: str = Form(...)
):

    db = SessionLocal()

    reporte = db.query(Reporte).filter(Reporte.id == id).first()

    reporte.titulo = titulo
    reporte.descripcion = descripcion
    reporte.ubicacion = ubicacion
    reporte.estado = estado

    db.commit()

    return RedirectResponse("/", status_code=303)

# =========================
# ELIMINAR REPORTE
# =========================
@app.get("/eliminar/{id}")
def eliminar(id: int):

    db = SessionLocal()

    reporte = db.query(Reporte).filter(Reporte.id == id).first()

    db.delete(reporte)
    db.commit()

    return RedirectResponse("/", status_code=303)