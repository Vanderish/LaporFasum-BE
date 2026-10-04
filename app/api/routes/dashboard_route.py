from fastapi import APIRouter, Depends, Query
from app.schemas.dashboard_schema import DashboardWargaResponse, DashboardAdminResponse, HeatmapResponse
from app.api.controllers import dashboard_controller
from app.api.deps import get_current_user, get_current_admin_kecamatan_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard & SIG"])

@router.get("/user", response_model=DashboardWargaResponse)
def dashboard_warga(current_user: dict = Depends(get_current_user)):
    return dashboard_controller.get_dashboard_warga(current_user)

@router.get("/admin", response_model=DashboardAdminResponse)
def dashboard_admin(current_user: dict = Depends(get_current_admin_kecamatan_role)):
    return dashboard_controller.get_dashboard_admin(current_user)

@router.get("/heatmap", response_model=HeatmapResponse)
def get_heatmap(current_user: dict = Depends(get_current_user)):
    return dashboard_controller.get_heatmap_data()

@router.get("/notifikasi")
def get_notifikasi(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return dashboard_controller.get_notifikasi(current_user, page, limit)