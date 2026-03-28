from app.repositories.base_repository import BaseRepository


class DeveloperRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "developers"

    def get_all_developers(self):
        return self._load_table(self.table_name)

    def get_active_developers(self):
        developers = self.get_by_field(self.table_name, "is_active", True)
        return sorted(developers, key=lambda x: x.get("order", 999))

    def get_developer_by_id(self, developer_id: int):
        return self.get_by_id(self.table_name, developer_id)

    def create_developer(self, developer_data: dict):
        return self.insert(self.table_name, developer_data)

    def update_developer(self, developer_id: int, updates: dict):
        return self.update(self.table_name, developer_id, updates)

    def delete_developer(self, developer_id: int):
        return self.delete(self.table_name, developer_id)
