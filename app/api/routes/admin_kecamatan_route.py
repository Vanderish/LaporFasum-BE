from fastapi import APIRouter, Depends
from app.api.controllers import admin_kecamatan_controller
from app.api.deps import get_current_admin_kecamatan_role

router = APIRouter(prefix="/admin-kecamatan", tags=["Admin Kecamatan"])

from fastapi import APIRouter, Depends, Query
from app.api.controllers import admin_kecamatan_controller
from app.api.deps import get_current_admin_kecamatan_role
from typing import Optional

router = APIRouter(prefix="/admin-kecamatan", tags=["Admin Kecamatan"])

@router.get("/dashboard")
def dashboard(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Items per page"),
    current_user: dict = Depends(get_current_admin_kecamatan_role)
):
    return admin_kecamatan_controller.get_dashboard_data(current_user, page, limit)
