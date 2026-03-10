"""
Chit Fund Calculator - Core Logic Module
========================================
Implements accurate chit fund mechanics as per Chit Funds Act, 1982 (Kerala/India)

Key Components:
- Month-by-month simulation
- Dividend tracking and net installment calculation
- Prize/Foreman commission deduction
- User's call month execution
- Bank FD comparison
- IRR calculation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChitInput:
    """Input parameters for chit fund calculation"""
    corpus: float = 1000000          # Total chit corpus (₹)
    monthly_installment: float = 10000  # Monthly payment per member
    num_months: int = 100            # Duration in months
    num_members: int = 100           # Total members
    foreman_commission_pct: float = 5.0  # Foreman commission as % of corpus
    user_call_month: int = 50        # Month when user calls (wins/bids)
    user_prize_pct: float = 85.0     # Prize as % of chit value after commission
    user_assumed_discount_pct: float = 15.0  # Average discount % (100 - prize%)
    fd_rate_pa: float = 9.0          # Bank FD interest rate (p.a.)
    
    def __post_init__(self):
        """Validate inputs"""
        if self.user_call_month < 1 or self.user_call_month > self.num_months:
            raise ValueError(f"Call month must be between 1 and {self.num_months}")
        if self.user_prize_pct < 0 or self.user_prize_pct > 100:
            raise ValueError("Prize percentage must be 0-100%")
        if self.monthly_installment <= 0:
            raise ValueError("Monthly installment must be positive")


@dataclass
class ChitMonth:
    """Monthly chit fund data"""
    month: int
    gross_collection: float          # N * monthly_installment
    foreman_commission: float        # Commission deducted
    chit_value_available: float      # Available for prize
    prize_amount: float              # Prize for winner
    discount_percentage: float       # Discount given to winner
    dividend_per_member: float       # Dividend for non-winning members
    net_installment: float           # Net payment = install - dividend credit
    user_paid: float                 # User's payment in this month
    user_cumulative_paid: float      # User's cumulative total paid
    user_remaining_months_for_collection: int  # Months user still pays
    

class ChitFundCalculator:
    """
    Core chit fund calculation engine
    Simulates month-by-month chit fund mechanics
    """
    
    def __init__(self, params: ChitInput):
        self.params = params
        self.monthly_data: List[ChitMonth] = []
        self.user_prize_received: float = 0
        self.user_total_paid: float = 0
        self.user_net_profit: float = 0
        self.user_irr: float = 0
        
    def calculate(self) -> pd.DataFrame:
        """
        Run complete month-by-month simulation
        Returns DataFrame with all monthly data
        """
        self._simulate_chit_months()
        return self._create_dataframe()
    
    def _simulate_chit_months(self):
        """
        Simulate each month of the chit fund
        
        Logic:
        1. Each month, collect: N * monthly_installment
        2. Deduct foreman commission
        3. Remaining is prize pool available
        4. In user's call month: User wins prize
        5. Other months: Prize goes to someone else, remainder as dividend
        6. User's net payment = installment - dividend accrual
        """
        user_cumulative_paid = 0
        user_dividend_credit = 0  # Accumulated dividend to offset future payments
        
        for month in range(1, self.params.num_months + 1):
            # 1. Gross collection from all members
            gross_collection = self.params.num_members * self.params.monthly_installment
            
            # 2. Foreman commission (% of corpus, deducted monthly)
            foreman_commission = (self.params.foreman_commission_pct / 100) * self.params.corpus
            
            # 3. Chit value available for prize
            chit_value_available = gross_collection - foreman_commission
            
            # Initialize monthly data
            prize_amount = 0
            discount_pct = 0
            dividend_per_member = 0
            
            # 4. Check if this is user's call month
            if month == self.params.user_call_month:
                # User wins/calls chit
                prize_amount = (self.params.user_prize_pct / 100) * chit_value_available
                self.user_prize_received = prize_amount
                discount_pct = 100 - self.params.user_prize_pct
                
                # Remaining discount is shared as dividend among (N-1) other members
                total_discount = (self.params.user_assumed_discount_pct / 100) * chit_value_available
                remaining_for_dividend = total_discount
                dividend_per_member = remaining_for_dividend / (self.params.num_members - 1)
                
            else:
                # Other member (or someone) wins this month
                # Assume average discount for non-user months
                discount_pct = self.params.user_assumed_discount_pct
                prize_amount = (1 - discount_pct / 100) * chit_value_available
                
                # Discount shared among remaining members (N-1 if not user's month, or N if distributed)
                # Simplified: dividend = discount / N (all members share)
                total_discount = (discount_pct / 100) * chit_value_available
                dividend_per_member = total_discount / self.params.num_members
            
            # 5. User's payment for this month
            # Each month user must pay: installment - dividend accrual
            # Dividend accrual is added up to offset future payments
            user_dividend_credit += dividend_per_member
            
            # Net installment is gross minus dividend accrual
            net_installment = self.params.monthly_installment - dividend_per_member
            
            # User pays the net amount
            user_paid_this_month = max(0, net_installment)  # Can't pay negative
            user_cumulative_paid += user_paid_this_month
            
            # Remaining months for collection (after user calls, they still pay)
            remaining_months_count = self.params.num_months - month
            
            # Store monthly data
            month_data = ChitMonth(
                month=month,
                gross_collection=gross_collection,
                foreman_commission=foreman_commission,
                chit_value_available=chit_value_available,
                prize_amount=prize_amount,
                discount_percentage=discount_pct,
                dividend_per_member=dividend_per_member,
                net_installment=net_installment,
                user_paid=user_paid_this_month,
                user_cumulative_paid=user_cumulative_paid,
                user_remaining_months_for_collection=remaining_months_count
            )
            self.monthly_data.append(month_data)
        
        # 6. User's total investment = total paid
        self.user_total_paid = user_cumulative_paid
        
        # 7. User's net profit
        self.user_net_profit = self.user_prize_received - self.user_total_paid
        
        # 8. Calculate IRR
        self._calculate_irr()
    
    def _calculate_irr(self):
        """
        Calculate user's effective IRR
        
        Cashflows:
        - Months 1 to user_call_month-1: -user_paid (outflows)
        - Month user_call_month: -user_paid + prize_received (inflow)
        - Months user_call_month+1 to end: -user_paid (outflows)
        """
        try:
            cashflows = [0]  # Month 0
            
            for month_data in self.monthly_data:
                if month_data.month == self.params.user_call_month:
                    # Month of call: outflow for payment, inflow for prize
                    cf = -month_data.user_paid + self.user_prize_received
                else:
                    # Regular months: just payment outflow
                    cf = -month_data.user_paid
                
                cashflows.append(cf)
            
            # Use numpy's IRR-like calculation (NPV at 0% is IRR)
            # Simplified: annualized return from monthly cashflows
            self.user_irr = self._npv_irr(cashflows)
            
        except Exception as e:
            self.user_irr = 0.0
    
    def _npv_irr(self, cashflows: List[float], rate_guess: float = 0.01) -> float:
        """
        Calculate IRR using Newton-Raphson method
        IRR is the rate where NPV = 0
        """
        def npv(rate, cfs):
            return sum(cf / (1 + rate) ** (i) for i, cf in enumerate(cfs))
        
        def npv_derivative(rate, cfs):
            return sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cfs))
        
        rate = rate_guess
        for _ in range(100):
            npv_val = npv(rate, cashflows)
            if abs(npv_val) < 1e-6:
                break
            npv_deriv = npv_derivative(rate, cashflows)
            if npv_deriv == 0:
                break
            rate = rate - npv_val / npv_deriv
        
        return rate * 12 * 100  # Convert monthly to annualized percentage
    
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert monthly data to pandas DataFrame"""
        data = []
        for md in self.monthly_data:
            data.append({
                'Month': md.month,
                'Gross Collection (₹)': f"{md.gross_collection:,.2f}",
                'Foreman Commission (₹)': f"{md.foreman_commission:,.2f}",
                'Chit Value (₹)': f"{md.chit_value_available:,.2f}",
                'Prize (₹)': f"{md.prize_amount:,.2f}",
                'Discount %': f"{md.discount_percentage:.2f}%",
                'Dividend/Member (₹)': f"{md.dividend_per_member:,.2f}",
                'Net Installment (₹)': f"{md.net_installment:,.2f}",
                'User Paid (₹)': f"{md.user_paid:,.2f}",
                'Cumulative Paid (₹)': f"{md.user_cumulative_paid:,.2f}",
            })
        
        return pd.DataFrame(data)


class BankFDCalculator:
    """
    Bank FD calculation for comparison
    Assumes monthly deposits compounded monthly
    """
    
    def __init__(self, params: ChitInput, user_total_paid: float, monthly_payments: List[float]):
        self.params = params
        self.user_total_paid = user_total_paid
        self.monthly_payments = monthly_payments
        
    def calculate(self) -> Tuple[float, float, float]:
        """
        Calculate FD maturity with monthly compounding
        
        Returns:
            maturity_amount: Final amount after 100 months
            total_interest: Interest earned
            effective_irr: Annualized return rate
        """
        monthly_rate = self.params.fd_rate_pa / 12 / 100
        maturity_amount = 0
        
        # Sum of each deposit compounded for remaining months
        for month_idx, payment in enumerate(self.monthly_payments):
            remaining_months = self.params.num_months - month_idx
            maturity_amount += payment * ((1 + monthly_rate) ** remaining_months)
        
        total_interest = maturity_amount - self.user_total_paid
        
        # Effective annual rate (simplified)
        period_years = self.params.num_months / 12
        if self.user_total_paid > 0:
            effective_rate = ((maturity_amount / self.user_total_paid) ** (1 / period_years) - 1) * 100
        else:
            effective_rate = 0
        
        return maturity_amount, total_interest, effective_rate
    
    def breakeven_prize(self, chit_values: List[float]) -> float:
        """
        Calculate minimum prize needed to match FD returns
        where: {prize - user_total_paid > fd_total_interest}
        """
        # Simplified: breakeven prize = total_paid + fd_interest
        fd_maturity, fd_interest, _ = self.calculate()
        breakeven = self.user_total_paid + fd_interest
        return breakeven


class ChitFundAnalyzer:
    """
    Comprehensive analysis combining chit and FD calculations
    """
    
    def __init__(self, params: ChitInput):
        self.params = params
        self.chit_calc = ChitFundCalculator(params)
        self.monthly_df = None
        self.fd_calc = None
        
    def run_analysis(self) -> Dict:
        """
        Run complete analysis and return all results
        """
        # 1. Run chit calculation
        self.monthly_df = self.chit_calc.calculate()
        
        # 2. Extract user's monthly payments
        user_payments = [md.user_paid for md in self.chit_calc.monthly_data]
        
        # 3. Run FD calculation
        self.fd_calc = BankFDCalculator(
            self.params,
            self.chit_calc.user_total_paid,
            user_payments
        )
        fd_maturity, fd_interest, fd_effective_rate = self.fd_calc.calculate()
        
        # 4. Calculate breakeven prize
        chit_values = [md.chit_value_available for md in self.chit_calc.monthly_data]
        breakeven_prize = self.fd_calc.breakeven_prize(chit_values)
        
        # 5. Compile results
        results = {
            'monthly_data': self.monthly_df,
            'chit_calc': self.chit_calc,  # Include calculator for monthly data access
            'chit': {
                'total_paid': self.chit_calc.user_total_paid,
                'prize_received': self.chit_calc.user_prize_received,
                'net_profit': self.chit_calc.user_net_profit,
                'irr_pct': self.chit_calc.user_irr,
            },
            'fd': {
                'total_invested': self.chit_calc.user_total_paid,
                'maturity_amount': fd_maturity,
                'interest_earned': fd_interest,
                'effective_irr_pct': fd_effective_rate,
            },
            'comparison': {
                'chit_profit': self.chit_calc.user_net_profit,
                'fd_profit': fd_interest,
                'better_option': 'Chit Fund' if self.chit_calc.user_net_profit > fd_interest else 'Bank FD',
                'profit_difference': abs(self.chit_calc.user_net_profit - fd_interest),
                'breakeven_prize': breakeven_prize,
            },
            'params': {
                'corpus': self.params.corpus,
                'monthly_installment': self.params.monthly_installment,
                'num_months': self.params.num_months,
                'num_members': self.params.num_members,
                'foreman_commission_pct': self.params.foreman_commission_pct,
                'user_call_month': self.params.user_call_month,
                'user_prize_pct': self.params.user_prize_pct,
                'fd_rate_pa': self.params.fd_rate_pa,
            }
        }
        
        return results


# ============================================
# QUICK TEST
# ============================================
if __name__ == "__main__":
    # Test scenario: User's example
    params = ChitInput(
        corpus=1000000,
        monthly_installment=10000,
        num_months=100,
        num_members=100,
        foreman_commission_pct=5.0,
        user_call_month=50,
        user_prize_pct=90.0,
        user_assumed_discount_pct=10.0,
        fd_rate_pa=9.0
    )
    
    analyzer = ChitFundAnalyzer(params)
    results = analyzer.run_analysis()
    
    print("\n" + "="*70)
    print("CHIT FUND CALCULATOR - TEST RESULTS")
    print("="*70)
    
    print("\n📊 USER'S CHIT FUND DETAILS:")
    print(f"  Total Invested (Paid):    ₹{results['chit']['total_paid']:,.2f}")
    print(f"  Prize Received:           ₹{results['chit']['prize_received']:,.2f}")
    print(f"  Net Profit (Chit):        ₹{results['chit']['net_profit']:,.2f}")
    print(f"  Effective IRR:            {results['chit']['irr_pct']:.2f}% p.a.")
    
    print("\n🏦 BANK FD EQUIVALENT:")
    print(f"  Total Invested:           ₹{results['fd']['total_invested']:,.2f}")
    print(f"  Maturity Amount:          ₹{results['fd']['maturity_amount']:,.2f}")
    print(f"  Interest Earned:          ₹{results['fd']['interest_earned']:,.2f}")
    print(f"  Effective IRR:            {results['fd']['effective_irr_pct']:.2f}% p.a.")
    
    print("\n⚖️ COMPARISON:")
    print(f"  Chit Fund Profit:         ₹{results['comparison']['chit_profit']:,.2f}")
    print(f"  Bank FD Profit:           ₹{results['comparison']['fd_profit']:,.2f}")
    print(f"  Better Option:            {results['comparison']['better_option']}")
    print(f"  Breakeven Prize (vs FD):  ₹{results['comparison']['breakeven_prize']:,.2f}")
    
    print("\n📈 MONTHLY BREAKDOWN (First 10 months):")
    print(results['monthly_data'].head(10).to_string(index=False))
    
    print("\n✅ Test completed successfully!")
