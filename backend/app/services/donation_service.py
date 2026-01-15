from typing import List, Optional, Dict, Any
from datetime import datetime, date
from app.repositories.donation_repository import DonationRepository
from app.repositories.member_repository import MemberRepository

class DonationService:
    def __init__(self):
        self.donation_repo = DonationRepository()
        self.member_repo = MemberRepository()
    
    def get_all_donations(self) -> List[Dict[str, Any]]:
        """Get all donations"""
        return self.donation_repo.get_all_donations()
    
    def get_donation_by_id(self, donation_id: int) -> Optional[Dict[str, Any]]:
        """Get donation by ID"""
        return self.donation_repo.get_donation_by_id(donation_id)
    
    def create_donation(self, donation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new donation"""
        # Validate member exists if not anonymous
        member_id = donation_data.get('member_id')
        if member_id and not donation_data.get('is_anonymous', False):
            member = self.member_repo.get_member_by_id(member_id)
            if not member:
                raise ValueError("Member not found")
        
        # Set donation date if not provided
        if 'donation_date' not in donation_data:
            donation_data['donation_date'] = date.today().isoformat()
        
        # Validate amount is positive
        if donation_data.get('amount', 0) <= 0:
            raise ValueError("Donation amount must be positive")
        
        return self.donation_repo.create_donation(donation_data)
    
    def update_donation(self, donation_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update donation"""
        # Validate amount is positive if being updated
        if 'amount' in updates and updates['amount'] <= 0:
            raise ValueError("Donation amount must be positive")
        
        # Validate member exists if being updated
        if 'member_id' in updates and updates['member_id']:
            member = self.member_repo.get_member_by_id(updates['member_id'])
            if not member:
                raise ValueError("Member not found")
        
        return self.donation_repo.update_donation(donation_id, updates)
    
    def delete_donation(self, donation_id: int) -> bool:
        """Delete donation"""
        return self.donation_repo.delete_donation(donation_id)
    
    def get_donations_by_member(self, member_id: int) -> List[Dict[str, Any]]:
        """Get donations by member"""
        return self.donation_repo.get_donations_by_member(member_id)
    
    def get_donations_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get donations within a date range"""
        return self.donation_repo.get_donations_by_date_range(start_date, end_date)
    
    def get_donations_by_fund(self, fund: str) -> List[Dict[str, Any]]:
        """Get donations by fund"""
        return self.donation_repo.get_donations_by_fund(fund)
    
    def get_member_donation_summary(self, member_id: int, year: Optional[int] = None) -> Dict[str, Any]:
        """Get donation summary for a member"""
        donations = self.donation_repo.get_donations_by_member(member_id)
        
        if year:
            donations = [d for d in donations if d.get('donation_date', '').startswith(str(year))]
        
        summary = {
            'member_id': member_id,
            'total_donations': len(donations),
            'total_amount': sum(d.get('amount', 0) for d in donations),
            'donations_by_type': {},
            'donations_by_fund': {},
            'tax_deductible_total': 0
        }
        
        for donation in donations:
            # By type
            donation_type = donation.get('donation_type', 'unknown')
            if donation_type not in summary['donations_by_type']:
                summary['donations_by_type'][donation_type] = {'count': 0, 'amount': 0}
            summary['donations_by_type'][donation_type]['count'] += 1
            summary['donations_by_type'][donation_type]['amount'] += donation.get('amount', 0)
            
            # By fund
            fund = donation.get('fund', 'general')
            if fund not in summary['donations_by_fund']:
                summary['donations_by_fund'][fund] = {'count': 0, 'amount': 0}
            summary['donations_by_fund'][fund]['count'] += 1
            summary['donations_by_fund'][fund]['amount'] += donation.get('amount', 0)
            
            # Tax deductible
            if donation.get('tax_deductible', True):
                summary['tax_deductible_total'] += donation.get('amount', 0)
        
        return summary
    
    def get_fund_totals(self) -> Dict[str, float]:
        """Get total donations by fund"""
        all_donations = self.donation_repo.get_all_donations()
        fund_totals = {}
        
        for donation in all_donations:
            fund = donation.get('fund', 'general')
            if fund not in fund_totals:
                fund_totals[fund] = 0
            fund_totals[fund] += donation.get('amount', 0)
        
        return fund_totals
    
    def get_monthly_totals(self, year: int) -> Dict[str, float]:
        """Get monthly donation totals for a year"""
        return self.donation_repo.get_monthly_totals(year)
    
    def get_donation_statistics(self) -> Dict[str, Any]:
        """Get donation statistics"""
        all_donations = self.donation_repo.get_all_donations()
        current_year = datetime.now().year
        
        # Get donations for current year
        current_year_donations = [
            d for d in all_donations 
            if d.get('donation_date', '').startswith(str(current_year))
        ]
        
        stats = {
            'total_donations': len(all_donations),
            'total_amount': sum(d.get('amount', 0) for d in all_donations),
            'current_year_donations': len(current_year_donations),
            'current_year_amount': sum(d.get('amount', 0) for d in current_year_donations),
            'average_donation': 0,
            'donations_by_type': {},
            'donations_by_fund': {},
            'donations_by_method': {},
            'anonymous_donations': len([d for d in all_donations if d.get('is_anonymous', False)]),
            'tax_deductible_total': sum(d.get('amount', 0) for d in all_donations if d.get('tax_deductible', True))
        }
        
        if all_donations:
            stats['average_donation'] = round(stats['total_amount'] / len(all_donations), 2)
        
        # Group by various categories
        for donation in all_donations:
            # By type
            donation_type = donation.get('donation_type', 'unknown')
            if donation_type not in stats['donations_by_type']:
                stats['donations_by_type'][donation_type] = {'count': 0, 'amount': 0}
            stats['donations_by_type'][donation_type]['count'] += 1
            stats['donations_by_type'][donation_type]['amount'] += donation.get('amount', 0)
            
            # By fund
            fund = donation.get('fund', 'general')
            if fund not in stats['donations_by_fund']:
                stats['donations_by_fund'][fund] = {'count': 0, 'amount': 0}
            stats['donations_by_fund'][fund]['count'] += 1
            stats['donations_by_fund'][fund]['amount'] += donation.get('amount', 0)
            
            # By payment method
            method = donation.get('payment_method', 'unknown')
            if method not in stats['donations_by_method']:
                stats['donations_by_method'][method] = {'count': 0, 'amount': 0}
            stats['donations_by_method'][method]['count'] += 1
            stats['donations_by_method'][method]['amount'] += donation.get('amount', 0)
        
        return stats