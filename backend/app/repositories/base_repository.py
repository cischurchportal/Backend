import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    def __init__(self, db_path: str = "../database"):
        self.db_path = db_path
        self.ensure_db_path()
    
    def ensure_db_path(self):
        """Ensure the database path exists"""
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
    
    def _get_file_path(self, table_name: str) -> str:
        """Get the full file path for a table"""
        return os.path.join(self.db_path, f"{table_name}.json")
    
    def _load_table(self, table_name: str) -> List[Dict[str, Any]]:
        """Load data from a JSON file"""
        file_path = self._get_file_path(table_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def _save_table(self, table_name: str, data: List[Dict[str, Any]]):
        """Save data to a JSON file"""
        file_path = self._get_file_path(table_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def get_all(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all records from a table"""
        return self._load_table(table_name)
    
    def get_by_id(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        """Get a record by ID"""
        data = self._load_table(table_name)
        for record in data:
            if record.get('id') == record_id:
                return record
        return None
    
    def get_by_field(self, table_name: str, field: str, value: Any) -> List[Dict[str, Any]]:
        """Get records by field value"""
        data = self._load_table(table_name)
        return [record for record in data if record.get(field) == value]
    
    def insert(self, table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new record"""
        data = self._load_table(table_name)
        
        # Auto-generate ID if not provided
        if 'id' not in record:
            max_id = max([r.get('id', 0) for r in data], default=0)
            record['id'] = max_id + 1
        
        # Add timestamps
        if 'created_at' not in record:
            record['created_at'] = datetime.utcnow().isoformat() + 'Z'
        
        data.append(record)
        self._save_table(table_name, data)
        return record
    
    def update(self, table_name: str, record_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record by ID"""
        data = self._load_table(table_name)
        
        for i, record in enumerate(data):
            if record.get('id') == record_id:
                # Add updated_at timestamp
                updates['updated_at'] = datetime.utcnow().isoformat() + 'Z'
                data[i].update(updates)
                self._save_table(table_name, data)
                return data[i]
        
        return None
    
    def delete(self, table_name: str, record_id: int) -> bool:
        """Delete a record by ID"""
        data = self._load_table(table_name)
        original_length = len(data)
        
        data = [record for record in data if record.get('id') != record_id]
        
        if len(data) < original_length:
            self._save_table(table_name, data)
            return True
        
        return False