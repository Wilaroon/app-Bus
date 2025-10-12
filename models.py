from sqlmodel import SQLModel, Field
from typing import Optional

# 🔹 Modelo base
class RouteBase(SQLModel):
    r_name: str = Field(index=True)
    r_descripcion: Optional[str] = None

# 🔹 Modelo principal (tabla en la BD)
class Route(RouteBase, table=True):
    r_id: str = Field(primary_key=True, max_length=10)
    r_color: Optional[str] = None

# 🔹 Modelo para crear (entrada del cliente)
class RouteCreate(RouteBase):
    r_id: Optional[str] = None
    r_color: Optional[str] = None

# 🔹 Modelo para mostrar (salida pública)
class RoutePublic(RouteBase):
    r_id: str
    r_color: Optional[str] = None

# 🔹 Modelo para actualizar
class RouteUpdate(SQLModel):
    r_name: Optional[str] = None
    r_descripcion: Optional[str] = None
    r_color: Optional[str] = None