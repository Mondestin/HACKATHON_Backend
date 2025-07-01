"""
Routers package for Campus Access Management System.
"""

from .health import router as health_router
from .users import router as users_router
from .access_cards import router as access_cards_router
from .access_logs import router as access_logs_router
from .rooms import router as rooms_router
from .reservations import router as reservations_router
from .students import router as students_router
from .professors import router as professors_router

__all__ = [
    "health",
    "users", 
    "access_cards",
    "access_logs",
    "rooms",
    "reservations",
    "students",
    "professors"
] 