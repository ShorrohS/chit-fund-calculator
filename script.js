// ============================================
// CHIT FUND CALCULATOR - JAVASCRIPT LOGIC
// ============================================

// DOM Elements
const chitAmountInput = document.getElementById('chitAmount');
const chitTermInput = document.getElementById('chitTerm');
const fdRateInput = document.getElementById('fdRate');
const calculateBtn = document.getElementById('calculateBtn');
const resetBtn = document.getElementById('resetBtn');
const resultsSection = document.getElementById('resultsSection');
const presetButtons = document.querySelectorAll('.preset-btn');
const recommendationBox = document.getElementById('recommendationBox');

// State
let calculationData = null;

// ============================================
// EVENT LISTENERS
// ============================================

calculateBtn.addEventListener('click', handleCalculate);
resetBtn.addEventListener('click', handleReset);

// Preset rate buttons
presetButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        presetButtons.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        fdRateInput.value = e.target.dataset.rate;
    });
});

// Update preset button state when input changes
fdRateInput.addEventListener('input', () => {
    presetButtons.forEach(btn => {
        if (btn.dataset.rate === fdRateInput.value) {
            presetButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
});

// ============================================
// CALCULATION FUNCTIONS
// ============================================

/**
 * Calculate compound interest for Bank FD
 * Formula: A = P(1 + r/100)^t
 * where P = principal, r = rate p.a., t = time in years
 */
function calculateFDReturns(principal, ratePerAnnum, termInMonths) {
    const timeInYears = termInMonths / 12;
    const rateDecimal = ratePerAnnum / 100;
    
    // Compound Interest Formula
    const maturityAmount = principal * Math.pow(1 + rateDecimal, timeInYears);
    const interestEarned = maturityAmount - principal;
    
    return {
        principal,
        ratePerAnnum,
        termInMonths,
        timeInYears,
        maturityAmount: Math.round(maturityAmount),
        interestEarned: Math.round(interestEarned)
    };
}

/**
 * Calculate Chit Breakeven Amount
 * 
 * In a chit fund, the value you receive when you "call" the chit
 * is the corpus minus a discount amount. This discount is typically
 * 5-10% based on demand and group dynamics.
 * 
 * Breakeven point: Amount received from chit call should equal FD maturity
 * 
 * If you invest X in chit and call it at discount D%:
 * Received Amount = X * (1 - D/100)
 * 
 * Find minimum X such that X * (1 - D/100) >= FD Maturity Amount
 * X >= FD Maturity Amount / (1 - D/100)
 */
function calculateChitBreakeven(fdMaturityAmount, discountPercent = 5) {
    // Breakeven = Required amount at which chit must be called to match FD returns
    const breakevenAmount = fdMaturityAmount / (1 - (discountPercent / 100));
    
    return {
        fdMaturityAmount,
        discountPercent,
        breakevenAmount: Math.round(breakevenAmount),
        breakevenEstimatedMin: Math.round(fdMaturityAmount / (1 - 0.10)), // 10% discount
        breakevenEstimatedMax: Math.round(fdMaturityAmount / (1 - 0.05))  // 5% discount
    };
}

/**
 * Main calculation handler
 */
function handleCalculate() {
    // Get input values
    const chitAmount = parseFloat(chitAmountInput.value) || 0;
    const chitTerm = parseFloat(chitTermInput.value) || 0;
    const fdRate = parseFloat(fdRateInput.value) || 0;

    // Validation
    if (chitAmount <= 0 || chitTerm <= 0 || fdRate <= 0) {
        alert('Please enter valid values for all fields (greater than 0)');
        return;
    }

    if (fdRate > 15) {
        alert('Interest rate seems too high. Please verify.');
        return;
    }

    // Calculate FD Returns
    const fdData = calculateFDReturns(chitAmount, fdRate, chitTerm);

    // Calculate Chit Breakeven
    const chitData = calculateChitBreakeven(fdData.maturityAmount, 5);

    // Store calculation data
    calculationData = {
        fd: fdData,
        chit: chitData,
        inputAmount: chitAmount,
        inputTerm: chitTerm
    };

    // Display results
    displayResults(calculationData);

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Display all results
 */
function displayResults(data) {
    const { fd, chit, inputAmount, inputTerm } = data;

    // Summary
    document.getElementById('summaryInitial').textContent = formatCurrency(inputAmount);
    document.getElementById('summaryTerm').textContent = inputTerm;
    document.getElementById('summaryRate').textContent = fd.ratePerAnnum.toFixed(1);
    document.getElementById('summaryYears').textContent = fd.timeInYears.toFixed(2);

    // FD Details
    document.getElementById('fdPrincipal').textContent = formatCurrency(fd.principal);
    document.getElementById('fdDisplayRate').textContent = fd.ratePerAnnum.toFixed(1);
    document.getElementById('fdDisplayYears').textContent = fd.timeInYears.toFixed(2);
    document.getElementById('fdMaturity').textContent = formatCurrency(fd.maturityAmount);
    document.getElementById('fdInterest').textContent = formatCurrency(fd.interestEarned);

    // Chit Details
    document.getElementById('chitDisplayAmount').textContent = formatCurrency(inputAmount);
    document.getElementById('estimatedMin').textContent = formatCurrency(chit.breakevenEstimatedMin);
    document.getElementById('estimatedMax').textContent = formatCurrency(chit.breakevenEstimatedMax);
    document.getElementById('breakevenValue').textContent = formatCurrency(chit.breakevenAmount);
    document.getElementById('breakeven').textContent = formatCurrency(chit.breakevenAmount);

    // Chart Display
    displayComparisonChart(fd, chit, inputAmount);

    // Recommendation
    displayRecommendation(fd, chit, inputAmount);

    // Show results section
    resultsSection.style.display = 'block';
}

/**
 * Display comparison chart
 */
function displayComparisonChart(fd, chit, investmentAmount) {
    const fdProfit = fd.interestEarned;
    const chitProfit = chit.breakevenAmount - investmentAmount;

    // Calculate max for scaling
    const maxValue = Math.max(fdProfit, chitProfit, investmentAmount);

    // FD Bar
    const fdBarHeight = (fdProfit / maxValue) * 100;
    const fdBar = document.getElementById('fdBar');
    fdBar.style.height = fdBarHeight + '%';
    document.getElementById('fdProfitDisplay').textContent = formatCurrency(fdProfit);

    // Chit Bar
    const chitBarHeight = (chitProfit / maxValue) * 100;
    const chitBar = document.getElementById('chitBar');
    chitBar.style.height = chitBarHeight + '%';
    document.getElementById('chitProfitDisplay').textContent = formatCurrency(chitProfit);
}

/**
 * Display recommendation based on analysis
 */
function displayRecommendation(fd, chit, investmentAmount) {
    const fdProfit = fd.interestEarned;
    const chitProfit = chit.breakevenAmount - investmentAmount;
    const profitDifference = Math.abs(fdProfit - chitProfit);
    const profitDifferencePercent = ((profitDifference / fdProfit) * 100).toFixed(1);

    let recommendation = '';
    let recommendationClass = '';

    if (chit.breakevenAmount <= chit.breakevenEstimatedMax) {
        // Chit is more favorable
        recommendationClass = 'chit-favorable';
        recommendation = `
            <strong style="color: #16a34a; font-size: 16px;">✓ Chit Fund is More Favorable!</strong>
            <p>
                If you can call your chit at <strong>₹${formatCurrency(chit.breakevenAmount)}</strong> or more, 
                you'll earn better returns than a bank FD at ${fd.ratePerAnnum.toFixed(1)}% p.a.
            </p>
            <p>
                <strong>Key Insight:</strong> With typical chit discounts of 5-10%, there's a ${profitDifferencePercent}% 
                higher return potential compared to fixed deposits.
            </p>
            <p>
                <strong>Risk Factor:</strong> However, chit funds carry higher risk. Ensure your chit group is reliable 
                and all members are trustworthy.
            </p>
        `;
    } else {
        // FD is more favorable
        recommendationClass = 'fd-favorable';
        recommendation = `
            <strong style="color: #ea580c; font-size: 16px;">⚠ Bank FD is Safer</strong>
            <p>
                To match bank FD returns, you'd need to call your chit at 
                <strong>₹${formatCurrency(chit.breakevenAmount)}</strong>, requiring a discount lower than typical market rates.
            </p>
            <p>
                <strong>Better Option:</strong> Bank FD at ${fd.ratePerAnnum.toFixed(1)}% guarantees 
                ₹${formatCurrency(fd.interestEarned)} in returns with zero risk.
            </p>
            <p>
                <strong>Timeline:</strong> Over ${fd.timeInYears.toFixed(1)} years, FD will give you 
                ₹${formatCurrency(fd.maturityAmount)} without depending on group dynamics.
            </p>
        `;
    }

    recommendationBox.className = 'recommendation-box ' + recommendationClass;
    recommendationBox.innerHTML = recommendation;
}

/**
 * Format number as Indian currency
 */
function formatCurrency(amount) {
    if (!amount && amount !== 0) return '0';
    
    const num = Math.round(amount);
    const str = num.toString();
    
    // Indian numbering system: 1,00,000
    if (num >= 100000) {
        const crores = Math.floor(num / 10000000);
        const lakhs = Math.floor((num % 10000000) / 100000);
        const thousands = Math.floor((num % 100000) / 1000);
        const remainder = num % 1000;
        
        let result = '';
        if (crores > 0) result += crores + ',';
        if (lakhs > 0 || crores > 0) result += lakhs.toString().padStart(2, '0') + ',';
        if (thousands > 0 || lakhs > 0 || crores > 0) result += thousands.toString().padStart(2, '0') + ',';
        result += remainder.toString().padStart(3, '0');
        
        return result;
    }
    
    return num.toLocaleString('en-IN');
}

/**
 * Reset form and hide results
 */
function handleReset() {
    resultsSection.style.display = 'none';
    calculationData = null;
    presetButtons.forEach(b => b.classList.remove('active'));
    document.querySelector('.preset-btn[data-rate="9"]').classList.add('active');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Initialize app
 */
function initializeApp() {
    // Set default preset button
    document.querySelector('.preset-btn[data-rate="9"]').classList.add('active');
    
    // Set default values if not already set
    if (!chitAmountInput.value) chitAmountInput.value = '100000';
    if (!chitTermInput.value) chitTermInput.value = '12';
    if (!fdRateInput.value) fdRateInput.value = '9';
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initializeApp);
