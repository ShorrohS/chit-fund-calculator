"""
Chit Fund Calculator - Streamlit Web Application
================================================
Mobile-first web interface for realistic chit fund calculations
Compares chit returns vs Bank FD under Kerala Chit Funds Act 1982
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
from chit_logic import ChitInput, ChitFundAnalyzer

# ============================================
# STREAMLIT PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Chit Fund Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-first design
st.markdown("""
<style>
    /* Mobile-first responsive */
    .main {
        padding: 0.5rem;
    }
    
    /* Input containers */
    .stNumberInput, .stSlider {
        padding: 0.5rem 0;
    }
    
    /* Results cards */
    .result-card {
        padding: 1rem;
        border-radius: 8px;
        background: #f0f7ff;
        border: 1px solid #e0e7ff;
        margin: 0.5rem 0;
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e40af;
    }
    
    .comparison-better {
        color: #16a34a;
        font-weight: bold;
    }
    
    .comparison-worse {
        color: #ea580c;
        font-weight: bold;
    }
    
    /* Tabs responsive */
    .stTabs [role="tab"] {
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        .stTabs [role="tab"] {
            padding: 0.3rem 0.5rem;
            font-size: 0.8rem;
        }
        
        .metric-value {
            font-size: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# PAGE HEADER
# ============================================

st.markdown("# 💰 Chit Fund Calculator")
st.markdown("**Real-time comparison: Chit Funds vs Bank FD (9% p.a.)**")
st.markdown("---")

# ============================================
# SIDEBAR - INPUT PARAMETERS
# ============================================

with st.sidebar:
    st.header("📋 Input Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        corpus = st.number_input(
            "Chit Corpus (₹)",
            min_value=100000,
            max_value=10000000,
            value=1000000,
            step=100000,
            help="Total chit amount (e.g., ₹10 lakh)"
        )
        
        num_months = st.number_input(
            "Duration (Months)",
            min_value=12,
            max_value=240,
            value=100,
            step=1,
            help="How many months will the chit run"
        )
        
        user_call_month = st.number_input(
            "User Calls at (Month)",
            min_value=1,
            max_value=None,
            value=50,
            step=1,
            help="Month when you bid/win the chit"
        )
    
    with col2:
        monthly_installment = st.number_input(
            "Monthly Installment (₹)",
            min_value=100,
            max_value=100000,
            value=10000,
            step=100,
            help="Your monthly payment"
        )
        
        num_members = st.number_input(
            "Total Members",
            min_value=5,
            max_value=500,
            value=100,
            step=1,
            help="Size of your chit group"
        )
        
        user_prize_pct = st.number_input(
            "User's Prize % (of chit value)",
            min_value=0.0,
            max_value=100.0,
            value=90.0,
            step=1.0,
            help="Prize as % of chit value after commission. E.g., 85% → ₹850K for ₹1M chit"
        )
    
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        foreman_commission_pct = st.slider(
            "Foreman Commission (%)",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5,
            help="Commission as % of corpus (deducted monthly)"
        )
        
        fd_rate_pa = st.slider(
            "Bank FD Rate (% p.a.)",
            min_value=0.1,
            max_value=15.0,
            value=9.0,
            step=0.1,
            help="Benchmark bank FD rate for comparison"
        )
    
    with col4:
        discount_pct = st.slider(
            "Avg Discount % (Chit Value)",
            min_value=1.0,
            max_value=30.0,
            value=10.0,
            step=1.0,
            help="Average discount given in chit auctions. 100% - prize%"
        )

# ============================================
# VALIDATION AND CALCULATION
# ============================================

try:
    # Validate inputs
    if user_call_month > num_months:
        st.error(f"❌ Call month ({user_call_month}) cannot be greater than duration ({num_months})")
        st.stop()
    
    # Create chit input
    params = ChitInput(
        corpus=corpus,
        monthly_installment=monthly_installment,
        num_months=num_months,
        num_members=num_members,
        foreman_commission_pct=foreman_commission_pct,
        user_call_month=user_call_month,
        user_prize_pct=user_prize_pct,
        user_assumed_discount_pct=discount_pct,
        fd_rate_pa=fd_rate_pa
    )
    
    # Run analysis
    analyzer = ChitFundAnalyzer(params)
    results = analyzer.run_analysis()
    
except Exception as e:
    st.error(f"❌ Calculation error: {str(e)}")
    st.stop()

# ============================================
# MAIN CONTENT - RESULTS
# ============================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Summary", "📈 Detailed Analysis", "📋 Monthly Breakdown", "📉 Charts", "⚙️ Explanation"]
)

# ============================================
# TAB 1: SUMMARY
# ============================================

with tab1:
    st.header("Your Chit Fund Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Amount Invested",
            f"₹{results['chit']['total_paid']:,.0f}",
            help="Sum of all net installments you paid"
        )
        st.metric(
            "Prize Received",
            f"₹{results['chit']['prize_received']:,.0f}",
            help=f"Prize at month {params.user_call_month} ({user_prize_pct:.1f}% of chit value)"
        )
    
    with col2:
        chit_profit = results['chit']['net_profit']
        profit_color = "🟢" if chit_profit > 0 else "🔴"
        
        st.metric(
            "Net Profit (Chit)",
            f"{profit_color} ₹{abs(chit_profit):,.0f}",
            delta=f"{chit_profit:+,.0f}" if chit_profit < 0 else None,
            help="Prize received minus total amount paid"
        )
        
        st.metric(
            "Effective IRR",
            f"{results['chit']['irr_pct']:.2f}% p.a.",
            help="Annualized return on your chit investment"
        )
    
    with col3:
        st.metric(
            "Bank FD Alternative",
            f"₹{results['fd']['maturity_amount']:,.0f}",
            help=f"Maturity if you invested ₹{results['chit']['total_paid']:,.0f} in {fd_rate_pa}% Bank FD for {num_months} months"
        )
        st.metric(
            "FD Interest Earned",
            f"₹{results['fd']['interest_earned']:,.0f}",
            help="Pure interest/profit from equivalent Bank FD"
        )
    
    with col4:
        better_chit = results['chit']['net_profit'] > results['fd']['interest_earned']
        better_option = "Chit Fund ✅" if better_chit else "Bank FD ✅"
        difference = results['comparison']['profit_difference']
        
        st.metric(
            "Better Option",
            better_option,
            help="Which gives better returns"
        )
        st.metric(
            "Difference",
            f"₹{difference:,.0f}",
            help=f"Profit gap between Chit and FD"
        )
    
    st.divider()
    
    # Breakeven Analysis
    st.subheader("🎯 Breakeven Analysis")
    
    breakeven_prize = results['comparison']['breakeven_prize']
    current_prize = results['chit']['prize_received']
    breakeven_diff = breakeven_prize - current_prize
    breakeven_pct = (breakeven_diff / current_prize * 100) if current_prize > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Minimum Prize to Match FD Returns:**
        
        ₹{breakeven_prize:,.0f}
        
        *You currently expect: ₹{current_prize:,.0f}*
        
        **Gap: ₹{breakeven_diff:,.0f} ({breakeven_pct:+.1f}%)**
        """)
    
    with col2:
        if breakeven_diff > 0:
            st.warning(f"""
            ❌ **You need {breakeven_pct:.1f}% higher prize to match Bank FD**
            
            Current prize: ₹{current_prize:,.0f}
            
            Target (to beat FD): ₹{breakeven_prize:,.0f}
            """)
        else:
            st.success(f"""
            ✅ **Chit Fund is BETTER!**
            
            Your expected return ₹{current_prize:,.0f} exceeds FD returns!
            
            Extra profit: ₹{abs(breakeven_diff):,.0f}
            """)

# ============================================
# TAB 2: DETAILED ANALYSIS
# ============================================

with tab2:
    st.header("Detailed Financial Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Chit Fund Details")
        chit_data = results['chit']
        
        chit_df = pd.DataFrame({
            'Metric': [
                'Total Paid (after dividends)',
                'Prize Received',
                'Gross Profit/Loss',
                'Effective IRR',
                'Call Month',
                'Prize % of Chit Value'
            ],
            'Value': [
                f"₹{chit_data['total_paid']:,.0f}",
                f"₹{chit_data['prize_received']:,.0f}",
                f"₹{chit_data['net_profit']:,.0f}",
                f"{chit_data['irr_pct']:.2f}%",
                f"Month {params.user_call_month}",
                f"{params.user_prize_pct:.1f}%"
            ]
        })
        
        st.dataframe(chit_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Bank FD Equivalent (9% p.a.)")
        fd_data = results['fd']
        
        fd_df = pd.DataFrame({
            'Metric': [
                'Principal (Same as Chit Paid)',
                'Maturity Amount',
                'Interest Earned',
                'Effective Rate',
                'Duration',
                'Compounding'
            ],
            'Value': [
                f"₹{fd_data['total_invested']:,.0f}",
                f"₹{fd_data['maturity_amount']:,.0f}",
                f"₹{fd_data['interest_earned']:,.0f}",
                f"{fd_data['effective_irr_pct']:.2f}%",
                f"{params.num_months} months",
                "Monthly"
            ]
        })
        
        st.dataframe(fd_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Comparison explanation
    st.subheader("Why These Results?")
    
    chit_profit = results['chit']['net_profit']
    fd_profit = results['fd']['interest_earned']
    
    if chit_profit > fd_profit:
        st.success(f"""
        **Chit Fund is {((chit_profit/fd_profit - 1)*100):.1f}% better** 🎉
        
        - Prize received: ₹{results['chit']['prize_received']:,.0f}
        - Total paid: ₹{results['chit']['total_paid']:,.0f}
        - Net profit: ₹{chit_profit:,.0f}
        
        vs Bank FD's ₹{fd_profit:,.0f}
        """)
    else:
        st.warning(f"""
        **Bank FD is {((fd_profit/abs(chit_profit) - 1)*100):.1f}% better** if profit is positive
        
        **Chit Fund shows a loss** if you negotiate poorly on the prize ❌
        
        - Prize received: ₹{results['chit']['prize_received']:,.0f}
        - Total paid: ₹{results['chit']['total_paid']:,.0f}
        - Net loss: ₹{abs(chit_profit):,.0f}
        
        vs Bank FD's guaranteed ₹{fd_profit:,.0f} profit
        """)

# ============================================
# TAB 3: MONTHLY DATA
# ============================================

with tab3:
    st.header("Month-by-Month Breakdown")
    
    # Show full monthly table with styled columns
    monthly_df = results['monthly_data'].copy()
    
    st.subheader("Your Payment Schedule & Chit Value")
    
    # Create a more readable version
    display_data = []
    for md in results['chit_calc'].monthly_data:
        display_data.append({
            'Month': md.month,
            'Collection (₹)': f"{md.gross_collection:,.0f}",
            'Commission (₹)': f"{md.foreman_commission:,.0f}",
            'Chit Value (₹)': f"{md.chit_value_available:,.0f}",
            'Prize (₹)': f"{md.prize_amount:,.0f}",
            'Discount %': f"{md.discount_percentage:.1f}%",
            'Dividend (₹)': f"{md.dividend_per_member:,.0f}",
            'Your Net Payment (₹)': f"{md.user_paid:,.0f}",
            'Your Cumulative (₹)': f"{md.user_cumulative_paid:,.0f}",
        })
    
    display_df = pd.DataFrame(display_data)
    
    # Highlight the call month
    def highlight_call_month(row):
        if row['Month'] == params.user_call_month:
            return ['background-color: #fff7ed'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        display_df.style.apply(highlight_call_month, axis=1),
        use_container_width=True,
        height=400
    )
    
    st.caption(f"🟠 Highlighted row: Month {params.user_call_month} is when you call the chit")
    
    # Key observations
    st.subheader("Key Observations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        first_month_paid = results['chit_calc'].monthly_data[0].user_paid
        last_month_paid = results['chit_calc'].monthly_data[-1].user_paid
        
        st.metric(
            "1st Month Payment",
            f"₹{first_month_paid:,.0f}",
            help="Net after dividend credit"
        )
    
    with col2:
        st.metric(
            "Payment at Call Month",
            f"₹{results['chit_calc'].monthly_data[params.user_call_month-1].user_paid:,.0f}",
            help=f"Month {params.user_call_month} payment"
        )
    
    with col3:
        st.metric(
            "Last Month Payment",
            f"₹{last_month_paid:,.0f}",
            help="Final payment of the chit"
        )

# ============================================
# TAB 4: CHARTS
# ============================================

with tab4:
    st.header("Visual Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cumulative Payment Tracking")
        
        # Cumulative payments chart
        months = [md.month for md in results['chit_calc'].monthly_data]
        cumulative_paid = [md.user_cumulative_paid for md in results['chit_calc'].monthly_data]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=cumulative_paid,
            mode='lines',
            name='Your Cumulative Payment',
            fill='tozeroy',
            line=dict(color='#2563eb', width=2),
            hovertemplate='<b>Month %{x}</b><br>Paid: ₹%{y:,.0f}<extra></extra>'
        ))
        
        # Add prize received marker
        call_month = params.user_call_month
        call_month_paid = results['chit_calc'].monthly_data[call_month-1].user_cumulative_paid
        
        fig.add_trace(go.Scatter(
            x=[call_month],
            y=[call_month_paid],
            mode='markers',
            name=f'Prize Received (Month {call_month})',
            marker=dict(color='#ea580c', size=12),
            hovertemplate=f'<b>Month {call_month}</b><br>Prize: ₹{results["chit"]["prize_received"]:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Cumulative Payment Progress",
            xaxis_title="Month",
            yaxis_title="Amount (₹)",
            hovermode='x unified',
            height=350,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Chit vs FD Returns Comparison")
        
        # Profit comparison
        categories = ['Chit Fund', 'Bank FD']
        profits = [
            results['chit']['net_profit'],
            results['fd']['interest_earned']
        ]
        colors = ['#16a34a' if p > 0 else '#ea580c' for p in profits]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=profits,
                marker_color=colors,
                text=[f'₹{p:,.0f}' for p in profits],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Profit: ₹%{y:,.0f}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="Profit Comparison",
            yaxis_title="Profit (₹)",
            height=350,
            showlegend=False,
            yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='#888')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Monthly Chit Value Trend")
        
        chit_values = [md.chit_value_available for md in results['chit_calc'].monthly_data]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=chit_values,
            mode='lines',
            name='Chit Value',
            fill='tozeroy',
            line=dict(color='#16a34a', width=2),
            hovertemplate='<b>Month %{x}</b><br>Value: ₹%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Chit Value Available Each Month",
            xaxis_title="Month",
            yaxis_title="Chit Value (₹)",
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.subheader("Monthly Dividend Distribution")
        
        dividends = [md.dividend_per_member for md in results['chit_calc'].monthly_data]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months,
            y=dividends,
            marker_color='#3b82f6',
            name='Dividend/Member',
            hovertemplate='<b>Month %{x}</b><br>Dividend: ₹%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Monthly Dividend Per Remaining Member",
            xaxis_title="Month",
            yaxis_title="Dividend (₹)",
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 5: EXPLANATION & RISKS
# ============================================

with tab5:
    st.header("How This Calculator Works...")
    
    st.subheader("📚 Understanding the Calculation")
    
    st.markdown("""
    #### What is a Chit Fund?
    A **chit fund** is a savings and borrowing scheme where a group of members (typically 100) contribute
    a fixed monthly amount (₹10,000) until a total corpus (₹10L) is accumulated.
    
    Each month, **ONE member wins** the auction and receives the chit value, while others continue paying
    and earn dividends from the discount given by the winner.
    
    #### How Calculations Work:
    
    **Each Month:**
    1. Gross Collection = No. of Members × Monthly Installment = 100 × ₹10,000 = ₹10L
    2. Foreman Commission (5%) = ₹50,000 is deducted
    3. Chit Value = ₹10L - ₹50K = ₹9.5L (for auction)
    4. **You receive:** Your prize when you call (e.g., ₹8.55L at 90% of ₹9.5L)
    5. **Others receive:** Discount shared as dividend (e.g., ₹950 each)
    
    **Your Total Investment:**
    - Monthly payment: ₹10,000
    - Less: Dividend credit: ₹950
    - **Net payment:** ₹9,050/month × 100 months = ₹9,05,000
    
    **Your Profit:**
    - Prize received: ₹8,55,000
    - Total paid: ₹9,05,000
    - **Net profit:** ₹8,55,000 - ₹9,05,000 = **-₹50,000 (Loss!)**
    
    #### Bank FD Comparison:
    If you invested ₹9,05,000 in a Bank FD @ 9% p.a. (compounded monthly) for 100 months:
    - Final amount: ₹13,50,749
    - Interest earned: ₹4,45,759
    - **This is better than the -₹50,000 chit loss!**
    
    #### Breakeven Prize:
    To match the FD's ₹4,45,759 profit, your chit prize must be:
    - ₹9,05,000 (paid) + ₹4,45,759 (profit) = **₹13,50,759**
    
    This means you need to negotiate a **MUCH HIGHER prize** at auction (way above 90%!) 
    or call the chit early when discounts are still high.
    """)
    
    st.divider()
    
    st.subheader("⚠️ Important Risks & Assumptions")
    
    st.warning("""
    #### Risks of Chit Funds:
    
    1. **Default Risk:** Members may default on payments → Your prize is delayed or reduced
    2. **Broker Credibility:** Unethical brokers may manipulate auctions → You get less than expected
    3. **Trust Risk:** Group dynamics → Personal conflicts can destroy group cohesion
    4. **Liquidity Risk:** Once you call, you're locked in for remaining duration
    5. **Regulatory Risk:** Lesser regulated than banks (no FDIC equivalent)
    6. **Market Risk:** Discounts depend on demand → You can't predict future discounts
    
    #### Assumptions in This Calculation:
    
    1. **All members continue paying:** No defaults assumed
    2. **Constant discounts:** We assume average {discount_pct}% discount every month
    3. **Simple dividend distribution:** Divided equally among members (actually varies)
    4. **You keep paying:** After calling, you continue monthly payments for full duration
    5. **No tax considerations:** Real chit funds have tax implications
    6. **Broker credibility:** Assumes honest broker (5% commission only)
    
    #### How to Make Chit Better Than FD:
    
    1. **Call at the right time:** Early calls have higher discounts → larger prize
    2. **Negotiate hard:** Brokers set auction rules → negotiate for better terms
    3. **Choose reliable group:** Reputable brokers have 0% default rates
    4. **Monitor market:** Chit market rates vary → call when rates are favorable
    5. **Diversify:** Don't put all eggs in one chit → use multiple chits
    6. **Post-call strategy:** Invest prize amount in FD for guaranteed returns
    """)
    
    st.divider()
    
    st.subheader("💡 Quick Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ✅ **When Chit is Better:**
        - Discount < 5% (prize > 95%)
        - Call early (month 20-40)
        - Strong group with 0% defaults
        - You need liquidity in 6-12 months
        """)
    
    with col2:
        st.info("""
        ✅ **When FD is Better:**
        - Risk-averse investor
        - Discount > 15% (prize < 85%)
        - Want guaranteed returns
        - Don't have time to monitor chit
        """)

# ============================================
# FOOTER & EXPORT
# ============================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    # Export as CSV
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Monthly Data (CSV)",
        data=csv,
        file_name=f"chit_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    # Summary as text
    summary_text = f"""CHIT FUND CALCULATOR REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INPUT PARAMETERS:
- Chit Corpus: ₹{corpus:,}
- Monthly Installment: ₹{monthly_installment:,}
- Duration: {num_months} months ({num_months/12:.1f} years)
- Members: {num_members}
- Your Call Month: {user_call_month}
- Expected Prize: {user_prize_pct:.1f}%
- Foreman Commission: {foreman_commission_pct:.1f}%
- Bank FD Rate: {fd_rate_pa:.1f}% p.a.

RESULTS:
Chit Fund:
- Total Invested: ₹{results['chit']['total_paid']:,.0f}
- Prize Received: ₹{results['chit']['prize_received']:,.0f}
- Net Profit: ₹{results['chit']['net_profit']:,.0f}
- Effective IRR: {results['chit']['irr_pct']:.2f}%

Bank FD (9% p.a.):
- Total Invested: ₹{results['fd']['total_invested']:,.0f}
- Maturity: ₹{results['fd']['maturity_amount']:,.0f}
- Interest Earned: ₹{results['fd']['interest_earned']:,.0f}
- Effective IRR: {results['fd']['effective_irr_pct']:.2f}%

RECOMMENDATION:
{results['comparison']['better_option']} is better by ₹{results['comparison']['profit_difference']:,.0f}
Breakeven Prize for Chit: ₹{results['comparison']['breakeven_prize']:,.0f}
"""
    
    st.download_button(
        label="📄 Download Summary Report",
        data=summary_text,
        file_name=f"chit_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

with col3:
    st.caption("💰 Chit Fund Calculator v1.0")
    st.caption("*For Kerala & Indian chit funds under Chit Funds Act, 1982*")

st.markdown("""
---
**Disclaimer:** This is an educational tool. Not financial advice. Consult experts before investing.
Chit funds carry higher risk than bank deposits. Past performance ≠ future results.
""")
