"""
Base repository using SQLAlchemy ORM for Azure SQL Database.
All repositories inherit from this class.
"""
import json
from typing import Any, Dict, List, Optional, Type, TypeVar
from datetime import datetime
from sqlalchemy import JSON as SA_JSON
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
        # Deserialize JSON strings that pymssql returns as str
        elif isinstance(val, str) and isinstance(col.type, SA_JSON):
            try:
                val = json.loads(val)
            except (ValueError, TypeError):
                pass
        d[col.name] = val
    return d


def _sanitize_for_insert(model, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare a data dict for INSERT/UPDATE:
    - Strip keys not in the model
    - Convert ISO datetime strings → datetime objects
    - Serialize JSON columns (list/dict) → JSON strings (pymssql requirement)
    """
    clean = {}
    for col in model.__table__.columns:
        k = col.name
        if k not in data:
            continue
        v = data[k]
        col_type = type(col.type).__name__
        # DateTime: convert ISO string → datetime object
        if col_type in ("DateTime", "DATETIME") and isinstance(v, str):
            try:
                v = datetime.fromisoformat(v.rstrip("Z"))
            except (ValueError, TypeError):
                continue  # skip unparseable datetime values
        # JSON columns: pymssql needs a serialized string, not a Python object
        elif isinstance(col.type, SA_JSON):
            if isinstance(v, (list, dict)):
                v = json.dumps(v)
            elif isinstance(v, str):
                # validate it's valid JSON, normalise it
                try:
                    v = json.dumps(json.loads(v))
                except (ValueError, TypeError):
                    v = json.dumps([])
        clean[k] = v
    return clean


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
        # Sanitize types and strip unknown columns
        data = _sanitize_for_insert(model, data)
        # Never manually set created_at/updated_at — let DB defaults handle them
        data.pop("created_at", None)
        data.pop("updated_at", None)

        with self._session() as db:
            obj = model(**data)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return _row_to_dict(obj)

    def update(self, table_name: str, record_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        model = self._get_model_class(table_name)
        valid_col_names = {c.name for c in model.__table__.columns}
        # Sanitize types
        updates = _sanitize_for_insert(model, {k: v for k, v in updates.items() if k != "id"})
        # Never manually set timestamps — base handles updated_at below
        updates.pop("created_at", None)
        updates.pop("updated_at", None)

        with self._session() as db:
            obj = db.query(model).filter(model.id == record_id).first()
            if not obj:
                return None
            for key, val in updates.items():
                setattr(obj, key, val)
            if "updated_at" in valid_col_names:
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
