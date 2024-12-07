"""Investment Memorandum Template Module.

This module provides a structured framework for generating investment memorandums.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Optional

@dataclass
class ContactInfo:
    """Basic contact information for the investment memo."""
    regional_director: str
    regional_team: str
    phone: str
    email: str
    date: date

@dataclass
class InvestmentSummary:
    """Key information about the investment opportunity."""
    borrower: str
    entrepreneurs: List[str]
    financing_need: float
    purpose: str
    co_financiers: Optional[str]
    investor_loan: float
    duration: int
    interest_rate: float
    ticket_size: float
    payment_schedule: str
    prepayment_penalty: str
    repayment_schedule: str
    risk_score: str
    admin_costs: float
    securities: List[str]
    conditions: List[str]

@dataclass
class CompanyAnalysis:
    """Detailed company information and analysis."""
    company_history: str
    business_model: str
    management_team: List[Dict[str, str]]
    innovations: List[str]
    risks: Dict[str, List[str]]  # SWOT analysis

@dataclass
class FinancialAnalysis:
    """Financial analysis and projections."""
    key_figures: Dict[str, float]
    balance_sheet: Dict[str, float]
    income_statement: Dict[str, float]
    cash_flow: Dict[str, float]
    ratios: Dict[str, float]

class InvestmentMemorandum:
    """Generate a complete investment memorandum."""
    
    def __init__(self, 
                 contact_info: ContactInfo,
                 investment_summary: InvestmentSummary,
                 company_analysis: CompanyAnalysis,
                 financial_analysis: FinancialAnalysis):
        self.contact_info = contact_info
        self.investment_summary = investment_summary
        self.company_analysis = company_analysis
        self.financial_analysis = financial_analysis

    def generate_memo(self) -> str:
        """Generate the complete memorandum text."""
        sections = [
            self._generate_header(),
            self._generate_investment_summary(),
            self._generate_company_analysis(),
            self._generate_financial_analysis(),
            self._generate_structure_and_return(),
        ]
        return "\n\n".join(sections)

    def _generate_header(self) -> str:
        return f"""
INVESTMENT MEMORANDUM

Regional Director: {self.contact_info.regional_director}
Regional Team: {self.contact_info.regional_team}
Phone: {self.contact_info.phone}
Email: {self.contact_info.email}
Date: {self.contact_info.date.strftime('%d-%m-%Y')}
"""

    def _generate_investment_summary(self) -> str:
        return f"""
1. Investment Opportunity Summary

Borrower(s): {self.investment_summary.borrower}
Financing Need: €{self.investment_summary.financing_need:,.2f}
Purpose: {self.investment_summary.purpose}
Duration: {self.investment_summary.duration} years
Interest Rate: {self.investment_summary.interest_rate}%
Risk Score: {self.investment_summary.risk_score}

Securities:
{"".join(f"- {security}\\n" for security in self.investment_summary.securities)}

Additional Conditions:
{"".join(f"- {condition}\\n" for condition in self.investment_summary.conditions)}
"""

    def _generate_company_analysis(self) -> str:
        return """
2. Company Analysis
[Company history, business model, market position]

3. Management Team
[Key personnel and their experience]

4. Product/Service Analysis
[Core offerings and innovations]

5. Market Analysis
[Industry overview, competition, opportunities]

6. Risk Analysis
[SWOT analysis and risk mitigation]
"""

    def _generate_financial_analysis(self) -> str:
        return """
7. Financial Analysis
[Historical performance]
[Financial projections]
[Key ratios and metrics]
[Cash flow analysis]
"""

    def _generate_structure_and_return(self) -> str:
        return """
8. Investment Structure
[Loan terms and conditions]
[Security structure]
[Reporting requirements]

9. Return Profile
[Interest rates]
[Payment schedule]
[Expected returns]
"""