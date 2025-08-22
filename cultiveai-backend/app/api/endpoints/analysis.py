from fastapi import APIRouter, HTTPException, Body, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from ... import schemas, crud, models
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
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    report = crud.crud_analysis.get_analysis_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    if report.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    
    return Response(content=report.report_html, media_type="text/html", headers={
        "Content-Disposition": f"attachment; filename=relatorio_cultiveai_{report_id}.html"
    })