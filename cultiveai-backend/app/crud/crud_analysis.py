from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas


def get_analysis_report(db: Session, report_id: int):
    return db.query(models.AnalysisReport).filter(models.AnalysisReport.id == report_id).first()


def get_user_reports(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.AnalysisReport).filter(
        models.AnalysisReport.owner_id == user_id
    ).order_by(models.AnalysisReport.created_at.desc()).offset(skip).limit(limit).all()


def get_user_reports_count(db: Session, user_id: int) -> int:
    return db.query(func.count(models.AnalysisReport.id)).filter(
        models.AnalysisReport.owner_id == user_id
    ).scalar()


def create_analysis_report(db: Session, report_data: dict, owner_id: int):
    db_report = models.AnalysisReport(**report_data, owner_id=owner_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def delete_analysis_report(db: Session, report: models.AnalysisReport) -> None:
    db.delete(report)
    db.commit()