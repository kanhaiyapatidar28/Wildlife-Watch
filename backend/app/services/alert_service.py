from typing import List, Optional
from app.database import db
from app.models.alert import AlertModel


class AlertService:
    @staticmethod
    def get_alerts(
        severity: Optional[str] = None,
        status: Optional[str] = None,
        area_id: Optional[str] = None,
    ) -> List[AlertModel]:
        results = list(db.alerts.values())

        if severity and severity.upper() != "ALL":
            results = [a for a in results if a.severity.upper() == severity.upper()]

        if status and status.upper() != "ALL":
            results = [a for a in results if a.status.upper() == status.upper()]

        if area_id and area_id.upper() != "ALL":
            results = [a for a in results if a.area_id == area_id]

        return results
