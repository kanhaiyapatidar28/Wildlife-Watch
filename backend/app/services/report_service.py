from typing import List, Optional
from app.database import db
from app.models.report import ReportModel


class ReportService:
    @staticmethod
    def get_reports(
        area_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[ReportModel]:
        results = list(db.reports.values())

        if area_id and area_id.upper() != "ALL":
            results = [r for r in results if r.area_id == area_id]

        if status and status.upper() != "ALL":
            results = [r for r in results if r.status.upper() == status.upper()]

        return results

    @staticmethod
    def get_report_by_id(report_id: str) -> Optional[ReportModel]:
        return db.reports.get(report_id)
