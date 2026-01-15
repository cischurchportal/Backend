from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.schemas import DonationCreate, DonationResponse
from app.services.donation_service import DonationService
from app.utils.responses import success_response, not_found_response, error_response

router = APIRouter(prefix="/api/donations", tags=["Donations"])
donation_service = DonationService()

@router.get("/")
async def get_all_donations():
    """Get all donations"""
    donations = donation_service.get_all_donations()
    return success_response(data={"donations": donations}, message="Donations retrieved successfully")

@router.get("/statistics")
async def get_donation_statistics():
    """Get donation statistics"""
    stats = donation_service.get_donation_statistics()
    return success_response(data=stats, message="Donation statistics retrieved successfully")

@router.get("/fund-totals")
async def get_fund_totals():
    """Get total donations by fund"""
    totals = donation_service.get_fund_totals()
    return success_response(data=totals, message="Fund totals retrieved successfully")

@router.get("/monthly-totals/{year}")
async def get_monthly_totals(year: int):
    """Get monthly donation totals for a year"""
    totals = donation_service.get_monthly_totals(year)
    return success_response(data=totals, message=f"Monthly totals for {year} retrieved successfully")

@router.get("/by-member/{member_id}")
async def get_donations_by_member(member_id: int):
    """Get donations by member"""
    donations = donation_service.get_donations_by_member(member_id)
    return success_response(data={"donations": donations}, message="Member donations retrieved successfully")

@router.get("/by-fund/{fund}")
async def get_donations_by_fund(fund: str):
    """Get donations by fund"""
    donations = donation_service.get_donations_by_fund(fund)
    return success_response(data={"donations": donations}, message=f"Donations for {fund} fund retrieved successfully")

@router.get("/by-date-range")
async def get_donations_by_date_range(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)")
):
    """Get donations within a date range"""
    donations = donation_service.get_donations_by_date_range(start_date, end_date)
    return success_response(data={"donations": donations}, message="Donations in date range retrieved successfully")

@router.get("/member-summary/{member_id}")
async def get_member_donation_summary(member_id: int, year: Optional[int] = Query(None, description="Year filter")):
    """Get donation summary for a member"""
    summary = donation_service.get_member_donation_summary(member_id, year)
    return success_response(data=summary, message="Member donation summary retrieved successfully")

@router.get("/{donation_id}")
async def get_donation(donation_id: int):
    """Get a specific donation by ID"""
    donation = donation_service.get_donation_by_id(donation_id)
    if not donation:
        raise not_found_response("Donation")
    
    return success_response(data=donation, message="Donation retrieved successfully")

@router.post("/", response_model=DonationResponse)
async def create_donation(donation_data: DonationCreate):
    """Create a new donation"""
    try:
        donation = donation_service.create_donation(donation_data.dict())
        return success_response(data=donation, message="Donation created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/{donation_id}")
async def update_donation(donation_id: int, updates: dict):
    """Update donation information"""
    try:
        donation = donation_service.update_donation(donation_id, updates)
        if not donation:
            raise not_found_response("Donation")
        
        return success_response(data=donation, message="Donation updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/{donation_id}")
async def delete_donation(donation_id: int):
    """Delete a donation"""
    success = donation_service.delete_donation(donation_id)
    if not success:
        raise not_found_response("Donation")
    
    return success_response(message="Donation deleted successfully")