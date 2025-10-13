
from fastapi import FastAPI, Depends, Query, HTTPException

from sqlmodel import  Session,  select, SQLModel, Field, create_engine

from database import engine

from typing import Annotated,List

from contextlib import asynccontextmanager

from models import Route, RouteCreate, RoutePublic, RouteUpdate,BusBase,BusCreate,BusPublic,BusStatus,Bus

from fastapi.middleware.cors import CORSMiddleware

def create_db_and_tables():



    SQLModel.metadata.create_all(engine)





def get_session():


    with Session(engine) as session:


        yield session

session_dep = Annotated[Session, Depends(get_session)]

app = FastAPI()
@app.get('/')
def root():
        return{'message':'Hello World'}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Se ejecuta al iniciar la app
    create_db_and_tables()
    yield
    # 🔚 (Opcional) Aquí puedes poner código que se ejecuta al cerrar la app
    # Por ejemplo: cerrar conexiones o limpiar recursos


app = FastAPI(lifespan=lifespan)

# 🟢 Permitir conexión desde el frontend (por ejemplo, Live Server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes limitarlo a ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Crear una nueva ruta ----------
@app.post("/routes/", response_model=RoutePublic)
def create_route(route: RouteCreate, session: session_dep):
    existing_route = session.exec(
        select(Route).where(Route.r_name == route.r_name)
    ).first()
    
    if existing_route:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe una ruta con el nombre '{route.r_name}'."
        )

    db_route = Route.model_validate(route)
    session.add(db_route)
    session.commit()
    session.refresh(db_route)
    return db_route


# ---------- Obtener todas las rutas ----------
@app.get("/routes/", response_model=list[RoutePublic])
def read_routes(
    session: session_dep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    routes = session.exec(select(Route).offset(offset).limit(limit)).all()
    return routes


# ---------- Obtener una ruta por ID ----------
@app.get("/routes/{r_id}", response_model=RoutePublic)
def read_route(r_id: str, session: session_dep):
    route = session.get(Route, r_id)
    if not route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return route


# ---------- Actualizar una ruta ----------
@app.patch("/routes/{r_id}", response_model=RoutePublic)
def update_route(r_id: str, route: RouteUpdate, session: session_dep):
    route_db = session.get(Route, r_id)
    if not route_db:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    route_data = route.model_dump(exclude_unset=True)
    route_db.sqlmodel_update(route_data)

    session.add(route_db)
    session.commit()
    session.refresh(route_db)
    return route_db


# ---------- Eliminar una ruta ----------
@app.delete("/routes/{r_id}")
def delete_route(r_id: str, session: session_dep):
    route = session.get(Route, r_id)
    if not route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    session.delete(route)
    session.commit()
    return {"ok": True, "message": f"Ruta con id {r_id} eliminada correctamente"}

"""#---------------obtiene buses-------
# --- Endpoint GET para obtener todos los buses ---

@app.get("/buses/", response_model=List[BusPublic])
def read_buses(session: Session = Depends(get_session)):
    statement = select(Bus)
    buses = session.exec(statement).all()
    return buses"""

@app.get("/buses/", response_model=list[BusPublic])
def read_buses(
    session: session_dep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    buses = session.exec(select(Bus).offset(offset).limit(limit)).all()
    return buses

