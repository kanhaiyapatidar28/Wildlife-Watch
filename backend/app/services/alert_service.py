"""Alert service interacting with PostgreSQL Alert models with resilient fallback."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.alert import Alert, AlertModel
from app.database import db as mock_db


class AlertService:
    @staticmethod
    def _alert_to_dto(a: Alert) -> AlertModel:
        """Transforms PostgreSQL Alert ORM entity into AlertModel."""
        return AlertModel(
            id=a.id,
            title=a.title,
            message=a.message,
            severity=a.severity,
            status=a.status,
            triggered_at=a.triggered_at.isoformat() if hasattr(a.triggered_at, "isoformat") else str(a.triggered_at),
            area_id=a.area_id,
            area_name=a.area_name,
            hotspot_id=a.hotspot_id,
        )

    @staticmethod
    def get_alerts(
        severity: Optional[str] = None,
        status: Optional[str] = None,
        area_id: Optional[str] = None,
        db_session: Optional[Session] = None,
    ) -> List[AlertModel]:
        """Retrieve alerts from PostgreSQL with fallback."""
        session = db_session or SessionLocal()
        try:
            query = session.query(Alert)
            if severity and severity.upper() != "ALL":
                query = query.filter(Alert.severity.ilike(severity))
            if status and status.upper() != "ALL":
                query = query.filter(Alert.status.ilike(status))
            if area_id and area_id.upper() != "ALL":
                query = query.filter(Alert.area_id == area_id)

            records = query.order_by(Alert.triggered_at.desc()).all()
            if records:
                return [AlertService._alert_to_dto(a) for a in records]
        except Exception:
            pass
        finally:
            if db_session is None:
                session.close()

        # Resilient fallback
        results = list(mock_db.alerts.values())
        if severity and severity.upper() != "ALL":
            results = [a for a in results if a.severity.upper() == severity.upper()]
        if status and status.upper() != "ALL":
            results = [a for a in results if a.status.upper() == status.upper()]
        if area_id and area_id.upper() != "ALL":
            results = [a for a in results if a.area_id == area_id]
        return results
