from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# Base de datos
engine = create_engine(
    "sqlite:///reportes.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Templates
templates = Jinja2Templates(directory="templates")

# =====================
# MODELO
# =====================

class Reporte(Base):

    __tablename__="reportes"

    id=Column(Integer,primary_key=True,index=True)
    titulo=Column(String(100))
    descripcion=Column(String(250))
    ubicacion=Column(String(100))
    estado=Column(String(30))

Base.metadata.create_all(bind=engine)


# =====================
# INICIO
# =====================

@app.get("/",response_class=HTMLResponse)
def inicio(request:Request):

    db=SessionLocal()

    reportes=db.query(Reporte).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "reportes":reportes
        }
    )


# =====================
# CREAR
# =====================

@app.post("/crear")
def crear(
    titulo:str=Form(...),
    descripcion:str=Form(...),
    ubicacion:str=Form(...)
):

    db=SessionLocal()

    nuevo=Reporte(
        titulo=titulo,
        descripcion=descripcion,
        ubicacion=ubicacion,
        estado="Pendiente"
    )

    db.add(nuevo)
    db.commit()

    db.close()

    return RedirectResponse("/",303)


# =====================
# EDITAR FORMULARIO
# =====================

@app.get("/editar/{id}",response_class=HTMLResponse)
def editar_form(request:Request,id:int):

    db=SessionLocal()

    reporte=db.query(
        Reporte
    ).filter(
        Reporte.id==id
    ).first()

    db.close()

    if not reporte:
        raise HTTPException(
            status_code=404,
            detail="Reporte no encontrado"
        )

    return templates.TemplateResponse(
        request=request,
        name="editar.html",
        context={
            "reporte":reporte
        }
    )


# =====================
# ACTUALIZAR
# =====================

@app.post("/editar/{id}")
def editar(
    id:int,
    titulo:str=Form(...),
    descripcion:str=Form(...),
    ubicacion:str=Form(...),
    estado:str=Form(...)
):

    db=SessionLocal()

    reporte=db.query(
        Reporte
    ).filter(
        Reporte.id==id
    ).first()

    if reporte:

        reporte.titulo=titulo
        reporte.descripcion=descripcion
        reporte.ubicacion=ubicacion
        reporte.estado=estado

        db.commit()

    db.close()

    return RedirectResponse("/",303)


# =====================
# ELIMINAR
# =====================

@app.post("/eliminar/{id}")
def eliminar(id:int):

    db=SessionLocal()

    reporte=db.query(
        Reporte
    ).filter(
        Reporte.id==id
    ).first()

    if reporte:
        db.delete(reporte)
        db.commit()

    db.close()

    return RedirectResponse("/",303)