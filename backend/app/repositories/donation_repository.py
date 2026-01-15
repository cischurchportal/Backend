from typing import Optional, Dict, Any, List
from .base_repository import BaseRepository

class DonationRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "donations"
    
    def get_all_donations(self) -> List[Dict[str, Any]]:
        """Get all donations"""
        return self.get_all(self.table_name)
    
    def get_donation_by_id(self, donation_id: int) -> Optional[Dict[str, Any]]:
        """Get donation by ID"""
        return self.get_by_id(self.table_name, donation_id)
    
    def get_donations_by_member(self, member_id: int) -> List[Dict[str, Any]]:
        """Get donations by member"""
        return self.get_by_field(self.table_name, 'member_id', member_id)
    
    def get_donations_by_type(self, donation_type: str) -> List[Dict[str, Any]]:
        """Get donations by type"""
        return self.get_by_field(self.table_name, 'donation_type', donation_type)
    
    def get_donations_by_fund(self, fund: str) -> List[Dict[str, Any]]:
        """Get donations by fund"""
        return self.get_by_field(self.table_name, 'fund', fund)
    
    def get_anonymous_donations(self) -> List[Dict[str, Any]]:
        """Get anonymous donations"""
        return self.get_by_field(self.table_name, 'is_anonymous', True)
    
    def create_donation(self, donation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new donation"""
        return self.insert(self.table_name, donation_data)
    
    def update_donation(self, donation_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update donation"""
        return self.update(self.table_name, donation_id, updates)
    
    def delete_donation(self, donation_id: int) -> bool:
        """Delete donation"""
        return self.delete(self.table_name, donation_id)
    
    def get_donations_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get donations within a date range"""
        all_donations = self.get_all_donations()
        
        results = []
        for donation in all_donations:
            donation_date = donation.get('donation_date', '')
            if start_date <= donation_date <= end_date:
                results.append(donation)
        
        return results
    
    def get_total_by_fund(self, fund: str) -> float:
        """Get total donations for a specific fund"""
        donations = self.get_donations_by_fund(fund)
        return sum(donation.get('amount', 0) for donation in donations)
    
    def get_total_by_member(self, member_id: int) -> float:
        """Get total donations by a member"""
        donations = self.get_donations_by_member(member_id)
        return sum(donation.get('amount', 0) for donation in donations)
    
    def get_monthly_totals(self, year: int) -> Dict[str, float]:
        """Get monthly donation totals for a year"""
        all_donations = self.get_all_donations()
        monthly_totals = {}
        
        for donation in all_donations:
            donation_date = donation.get('donation_date', '')
            if donation_date.startswith(str(year)):
                month = donation_date[5:7]  # Extract month from YYYY-MM-DD
                if month not in monthly_totals:
                    monthly_totals[month] = 0
                monthly_totals[month] += donation.get('amount', 0)
        
        return monthly_totals