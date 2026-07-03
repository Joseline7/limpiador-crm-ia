from pydantic import BaseModel, Field
from typing import List, Optional

class LeadLimpio(BaseModel):
    nombre: Optional[str] = Field(description="Primer nombre capitalizado (Ej: Joseline)")
    apellido: Optional[str] = Field(description="Apellidos capitalizados (Ej: Aguirre)")
    telefono: Optional[str] = Field(description="Teléfono en formato internacional E.164. Si no tiene código de país y es de Perú, asumir +51. Ej: +51987654321")
    email: Optional[str] = Field(description="Email en minúsculas. Corregir errores obvios de dominio como gmail.co a gmail.com")
    empresa_contexto: Optional[str] = Field(description="Nombre de la empresa o notas de contexto encontradas en el texto")

class BaseDatosLimpia(BaseModel):
    leads: List[LeadLimpio]
