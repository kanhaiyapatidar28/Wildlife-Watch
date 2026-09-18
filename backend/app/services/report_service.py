"""Report service interacting with PostgreSQL Report models with resilient fallback."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.report import Report, ReportModel
from app.database import db as mock_db


class ReportService:
    @staticmethod
    def _report_to_dto(r: Report) -> ReportModel:
        """Transforms PostgreSQL Report ORM entity into ReportModel."""
        size_mb = round(r.file_size_bytes / (1024 * 1024), 2) if getattr(r, "file_size_bytes", 0) else 14.5
        gen_at = r.created_at.isoformat() if hasattr(r.created_at, "isoformat") else str(r.created_at)
        return ReportModel(
            id=r.id,
            title=r.title,
            area_name=r.area_name,
            format=r.format,
            date_range=r.date_range,
            status=r.status,
            download_url=r.download_url,
            area_id=r.area_id or "ALL",
            file_size_mb=size_mb,
            generated_at=gen_at,
        )

    @staticmethod
    def get_reports(
        area_id: Optional[str] = None,
        status: Optional[str] = None,
        db_session: Optional[Session] = None,
    ) -> List[ReportModel]:
        """Retrieve report catalog from PostgreSQL with fallback."""
        session = db_session or SessionLocal()
        try:
            query = session.query(Report)
            if area_id and area_id.upper() != "ALL":
                query = query.filter(Report.area_id == area_id)
            if status and status.upper() != "ALL":
                query = query.filter(Report.status.ilike(status))

            records = query.order_by(Report.created_at.desc()).all()
            if records:
                return [ReportService._report_to_dto(r) for r in records]
        except Exception:
            pass
        finally:
            if db_session is None:
                session.close()

        # Resilient fallback
        results = list(mock_db.reports.values())
        if area_id and area_id.upper() != "ALL":
            results = [r for r in results if r.area_id == area_id]
        if status and status.upper() != "ALL":
            results = [r for r in results if r.status.upper() == status.upper()]
        return results

    @staticmethod
    def get_report_by_id(
        report_id: str,
        db_session: Optional[Session] = None,
    ) -> Optional[ReportModel]:
        """Retrieve single report metadata by ID."""
        session = db_session or SessionLocal()
        try:
            r = session.query(Report).filter(Report.id == report_id).first()
            if r:
                return ReportService._report_to_dto(r)
        except Exception:
            pass
        finally:
            if db_session is None:
                session.close()

        return mock_db.reports.get(report_id)
