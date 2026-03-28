from typing import Optional, Dict, Any, List
from app.repositories.base_repository import BaseRepository


class DonationRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "donations"

    def get_all_donations(self) -> List[Dict[str, Any]]:
        return self.get_all(self.table_name)

    def get_donation_by_id(self, donation_id: int) -> Optional[Dict[str, Any]]:
        return self.get_by_id(self.table_name, donation_id)

    def get_donations_by_member(self, member_id: int) -> List[Dict[str, Any]]:
        return self.get_by_field(self.table_name, "member_id", member_id)

    def get_donations_by_type(self, donation_type: str) -> List[Dict[str, Any]]:
        return self.get_by_field(self.table_name, "donation_type", donation_type)

    def get_donations_by_fund(self, fund: str) -> List[Dict[str, Any]]:
        return self.get_by_field(self.table_name, "fund", fund)

    def get_anonymous_donations(self) -> List[Dict[str, Any]]:
        return self.get_by_field(self.table_name, "is_anonymous", True)

    def create_donation(self, donation_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(self.table_name, donation_data)

    def update_donation(self, donation_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.update(self.table_name, donation_id, updates)

    def delete_donation(self, donation_id: int) -> bool:
        return self.delete(self.table_name, donation_id)

    def get_donations_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        all_donations = self.get_all_donations()
        return [
            d for d in all_donations
            if start_date <= (d.get("donation_date") or "") <= end_date
        ]

    def get_total_by_fund(self, fund: str) -> float:
        return sum(d.get("amount", 0) for d in self.get_donations_by_fund(fund))

    def get_total_by_member(self, member_id: int) -> float:
        return sum(d.get("amount", 0) for d in self.get_donations_by_member(member_id))

    def get_monthly_totals(self, year: int) -> Dict[str, float]:
        monthly: Dict[str, float] = {}
        for d in self.get_all_donations():
            date_str = d.get("donation_date", "") or ""
            if date_str.startswith(str(year)):
                month = date_str[5:7]
                monthly[month] = monthly.get(month, 0) + d.get("amount", 0)
        return monthly
