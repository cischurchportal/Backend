"""
Base repository using SQLAlchemy ORM for Azure SQL Database.
All repositories inherit from this class.
"""
from typing import Any, Dict, List, Optional, Type, TypeVar
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import get_session_factory
from app.db.models import Base

ModelType = TypeVar("ModelType", bound=Base)


def _row_to_dict(obj) -> Dict[str, Any]:
    """Convert a SQLAlchemy model instance to a plain dict."""
    d = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        if isinstance(val, datetime):
            val = val.isoformat() + "Z"
        d[col.name] = val
    return d


class BaseRepository:
    def __init__(self):
        self._SessionLocal = get_session_factory()

    def _session(self) -> Session:
        return self._SessionLocal()

    # ------------------------------------------------------------------ #
    #  Generic CRUD helpers                                                #
    # ------------------------------------------------------------------ #

    def _get_model_class(self, table_name: str):
        """Resolve SQLAlchemy model class from table name."""
        for mapper in Base.registry.mappers:
            if mapper.class_.__tablename__ == table_name:
                return mapper.class_
        raise ValueError(f"No model found for table '{table_name}'")

    def get_all(self, table_name: str) -> List[Dict[str, Any]]:
        model = self._get_model_class(table_name)
        with self._session() as db:
            rows = db.query(model).all()
            return [_row_to_dict(r) for r in rows]

    def get_by_id(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        model = self._get_model_class(table_name)
        with self._session() as db:
            row = db.query(model).filter(model.id == record_id).first()
            return _row_to_dict(row) if row else None

    def get_by_field(self, table_name: str, field: str, value: Any) -> List[Dict[str, Any]]:
        model = self._get_model_class(table_name)
        with self._session() as db:
            col = getattr(model, field)
            rows = db.query(model).filter(col == value).all()
            return [_row_to_dict(r) for r in rows]

    def insert(self, table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        model = self._get_model_class(table_name)
        # Remove 'id' if None so DB auto-generates it
        data = {k: v for k, v in record.items() if not (k == "id" and v is None)}
        # Strip keys not in the model
        valid_cols = {c.name for c in model.__table__.columns}
        data = {k: v for k, v in data.items() if k in valid_cols}

        with self._session() as db:
            obj = model(**data)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return _row_to_dict(obj)

    def update(self, table_name: str, record_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        model = self._get_model_class(table_name)
        valid_cols = {c.name for c in model.__table__.columns}
        updates = {k: v for k, v in updates.items() if k in valid_cols and k != "id"}

        with self._session() as db:
            obj = db.query(model).filter(model.id == record_id).first()
            if not obj:
                return None
            for key, val in updates.items():
                setattr(obj, key, val)
            if "updated_at" in valid_cols:
                obj.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(obj)
            return _row_to_dict(obj)

    def delete(self, table_name: str, record_id: int) -> bool:
        model = self._get_model_class(table_name)
        with self._session() as db:
            obj = db.query(model).filter(model.id == record_id).first()
            if not obj:
                return False
            db.delete(obj)
            db.commit()
            return True

    # ------------------------------------------------------------------ #
    #  Legacy JSON helpers (kept for backward compat, now no-ops)         #
    # ------------------------------------------------------------------ #

    def _load_table(self, table_name: str) -> List[Dict[str, Any]]:
        return self.get_all(table_name)

    def _save_table(self, table_name: str, data: List[Dict[str, Any]]):
        pass  # Not needed with SQL backend
