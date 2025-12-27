"""Mock database for testing"""
from typing import Any, Dict, List, Optional
from datetime import datetime


class MockDatabase:
    """Mock database for testing"""
    
    def __init__(self):
        """Initialize mock database with empty tables"""
        self.tables: Dict[str, List[Dict[str, Any]]] = {
            "users": [],
            "projects": [],
            "scripts": [],
            "jobs": [],
            "assets": [],
        }
        self._id_counters: Dict[str, int] = {table: 0 for table in self.tables}
    
    def _generate_id(self, table: str) -> int:
        """Generate auto-incrementing ID for table"""
        self._id_counters[table] += 1
        return self._id_counters[table]
    
    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert record into table"""
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        # Add ID and timestamp if not present
        record = data.copy()
        if "id" not in record:
            record["id"] = self._generate_id(table)
        if "created_at" not in record:
            record["created_at"] = datetime.utcnow().isoformat()
        
        self.tables[table].append(record)
        return record
    
    def find_by_id(self, table: str, record_id: int) -> Optional[Dict[str, Any]]:
        """Find record by ID"""
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        for record in self.tables[table]:
            if record.get("id") == record_id:
                return record
        return None
    
    def find_all(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Find all records matching filters"""
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        if not filters:
            return self.tables[table].copy()
        
        results = []
        for record in self.tables[table]:
            match = True
            for key, value in filters.items():
                if record.get(key) != value:
                    match = False
                    break
            if match:
                results.append(record)
        
        return results
    
    def update(self, table: str, record_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update record by ID"""
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        for record in self.tables[table]:
            if record.get("id") == record_id:
                record.update(updates)
                record["updated_at"] = datetime.utcnow().isoformat()
                return record
        
        return None
    
    def delete(self, table: str, record_id: int) -> bool:
        """Delete record by ID"""
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        for i, record in enumerate(self.tables[table]):
            if record.get("id") == record_id:
                del self.tables[table][i]
                return True
        
        return False
    
    def count(self, table: str, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records matching filters"""
        if filters:
            return len(self.find_all(table, filters))
        return len(self.tables[table])
    
    def clear_table(self, table: str):
        """Clear all records from table"""
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        self.tables[table] = []
        self._id_counters[table] = 0
    
    def clear_all(self):
        """Clear all tables"""
        for table in self.tables:
            self.clear_table(table)
    
    def add_table(self, table: str):
        """Add new table to database"""
        if table not in self.tables:
            self.tables[table] = []
            self._id_counters[table] = 0


# Example usage in tests:
# def test_database_operations():
#     db = MockDatabase()
#     
#     # Insert user
#     user = db.insert("users", {
#         "email": "test@example.com",
#         "username": "testuser"
#     })
#     assert user["id"] == 1
#     
#     # Find user
#     found = db.find_by_id("users", 1)
#     assert found["email"] == "test@example.com"
#     
#     # Update user
#     updated = db.update("users", 1, {"username": "newname"})
#     assert updated["username"] == "newname"
#     
#     # Delete user
#     deleted = db.delete("users", 1)
#     assert deleted is True
#     
#     # Cleanup
#     db.clear_all()
