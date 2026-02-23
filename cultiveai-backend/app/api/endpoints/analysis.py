from fastapi import APIRouter, HTTPException, Body, Depends, Response, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ... import schemas, crud, models
from ...core import security
from ...services import gee_service, ai_service, report_service
from .. import deps

router = APIRouter()

@router.post("/", response_model=schemas.AnalysisResponse)
def create_analysis(
    geojson: schemas.GeoJSONInput = Body(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    try:
        gee_results = gee_service.run_analysis(geojson.dict())

        ai_desc = ai_service.generate_ai_description(
            ndvi_stats=gee_results['ndvi_stats'],
            pixel_counts_dict=gee_results['pixel_counts_for_ai'],
            aoi_area_sqm=gee_results['aoi_area_hectares'] * 10000
        )
        
        del gee_results['pixel_counts_for_ai']
        gee_results['ai_description'] = ai_desc

        html_report = report_service.generate_html_report(gee_results)
        gee_results['report_html'] = html_report
        # Remove thumbnail_urls - only needed for the HTML report, not stored in DB
        gee_results.pop('thumbnail_urls', None)

        db_report = crud.crud_analysis.create_analysis_report(
            db=db, 
            report_data=gee_results,
            owner_id=current_user.id
        )
        
        return db_report

    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"ERRO GERAL na análise: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno: {e}")

@router.get("/{report_id}", response_model=schemas.AnalysisResponse)
def get_report(
    report_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    report = crud.crud_analysis.get_analysis_report(db, report_id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    if report.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a ver este relatório")
    return report

@router.get("/", response_model=List[schemas.AnalysisResponse])
def get_all_user_reports(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    reports = crud.crud_analysis.get_user_reports(db, user_id=current_user.id)
    return reports

@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    token: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db)
):
    """Download report HTML. Regenerates HTML from stored analysis data so template updates are always reflected."""
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    # Verify token from query string
    email = security.verify_token(token, token_type="access")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = crud.crud_user.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    report = crud.crud_analysis.get_analysis_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    if report.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Não autorizado")

    # Build analysis_data dict from stored DB columns for dynamic HTML generation
    analysis_data = {
        'aoi_geojson': report.aoi_geojson,
        'aoi_area_hectares': report.aoi_area_hectares or 0,
        'analysis_period': report.analysis_period or {},
        'satellite_image_info': report.satellite_image_info or {},
        'ndvi_stats': report.ndvi_stats or {},
        'degradation_summary': report.degradation_summary or [],
        'ai_description': report.ai_description or '',
        'map_layers_urls': report.map_layers_urls or {},
        'created_at': report.created_at,
    }

    # Add property name if linked
    if report.property_id and report.property:
        analysis_data['property_name'] = report.property.name

    html_content = report_service.generate_html_report(analysis_data)

    return Response(content=html_content, media_type="text/html", headers={
        "Content-Disposition": f"attachment; filename=relatorio_cultiveai_{report_id}.html"
    })


@router.delete("/{report_id}", status_code=204)
def delete_report(
    report_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Delete an analysis report."""
    report = crud.crud_analysis.get_analysis_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    if report.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a excluir este relatório")
    crud.crud_analysis.delete_analysis_report(db, report)
    return None