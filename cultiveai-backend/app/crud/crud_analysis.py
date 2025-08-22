from sqlalchemy.orm import Session
from .. import models, schemas

def get_analysis_report(db: Session, report_id: int):
    return db.query(models.AnalysisReport).filter(models.AnalysisReport.id == report_id).first()

def get_user_reports(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.AnalysisReport).filter(models.AnalysisReport.owner_id == user_id).offset(skip).limit(limit).all()

def create_analysis_report(db: Session, report_data: dict, owner_id: int):
    db_report = models.AnalysisReport(**report_data, owner_id=owner_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report