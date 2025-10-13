from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

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


#Models Bus 
# --- 1. Enumeración para el campo 'b_status' ---
# Esto asegura que el valor de 'b_status' sea siempre uno de los permitidos.
class BusStatus(str, Enum):
    """Estatus del bus."""
    EN_RUTA = "En ruta"
    EN_PARADA = "En parada"
    FUERA_DE_SERVICIO = "Fuera de servicio"

# --- 2. Modelo Base (Campos comunes) ---
class BusBase(SQLModel):
    b_asgroute: Optional[str] = Field(default=None, max_length=10) # Ruta asignada
    b_current_stop: Optional[str] = Field(default=None, max_length=10) # Parada actual
    b_next_stop: Optional[str] = Field(default=None, max_length=10) # Próxima parada
    b_status: BusStatus = Field(default=BusStatus.EN_RUTA) # Estatus con el valor por defecto

# --- 3. Modelo de la Tabla (SQLModel) ---
# Este modelo se usa internamente y es la representación "cruda" de la fila de la BD.
class Bus(BusBase, table=True):
    b_id: str = Field(primary_key=True, max_length=10)

# --- 4. Modelo para la Lectura Pública (Pydantic) ---
# Este modelo es lo que verán los clientes de tu API.
class BusPublic(BusBase):
    b_id: str
    # No necesitamos redefinir 'b_status', ya que lo hereda de BusBase.

# --- 5. Modelo para Creación (Input) ---
class BusCreate(BusBase):
    b_id: str = Field(max_length=10) # Debe ser obligatorio al crear
    # El resto de campos hereda los defaults y opcionales.