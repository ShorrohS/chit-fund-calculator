# 💰 Chit Fund Calculator

A modern, responsive web application that helps users calculate and compare Chit Fund returns with Bank Fixed Deposits.

## Features

✅ **Quick Calculations** - Calculate FD returns and chit breakeven amounts instantly
✅ **Customizable Interest Rates** - Select from preset rates (8%, 9%, 10%, 11%) or enter custom rates
✅ **Detailed Analysis** - Get comprehensive breakdown of calculations and recommendations
✅ **Comparison Charts** - Visual comparison of FD vs Chit Fund profits
✅ **Mobile Responsive** - Works perfectly on Android, iOS, and desktop browsers
✅ **Offline Support** - Progressive Web App that works without internet after first load
✅ **Easy to Use** - Simple, intuitive interface for quick decisions

## How to Use

### 1. **Enter Your Investment Details**
   - **Chit Amount**: Total amount you plan to invest (e.g., ₹100,000)
   - **Chit Term**: Duration of your chit investment in months (e.g., 12 months)
   - **Bank FD Interest Rate**: Choose from presets or enter a custom rate (default: 9% p.a.)

### 2. **View Results**
   The app will show:
   - Bank FD maturity amount and interest earned
   - **Breakeven Amount**: Minimum chit call amount needed to match FD returns
   - Profit comparison chart
   - Smart recommendation based on your inputs

### 3. **Adjust & Compare**
   - Change the interest rate to see how it affects breakeven
   - Try different chit amounts and terms
   - Use preset buttons for quick rate selection

## Understanding the Calculations

### Bank FD Returns
Uses the **Compound Interest Formula**:
```
A = P(1 + r/100)^t
```
Where:
- **A** = Final Amount (Maturity)
- **P** = Principal (Initial Investment)
- **r** = Rate of Interest (per annum)
- **t** = Time Period (in years)

### Chit Fund Breakeven
**Breakeven Amount** = FD Maturity ÷ (1 - Discount%)

This tells you the minimum amount you need to receive when calling your chit to match FD returns.

**Example:**
- FD Maturity: ₹109,000 (on ₹100,000 at 9% for 1 year)
- With 5% typical chit discount:
  - Breakeven = 109,000 ÷ (1 - 0.05) = **₹114,737**
  - This means your chit must be called at ₹114,737 or more to beat the FD

## Key Insights

### When is Chit Fund Better?
- If typical chit market discounts are 5-10%
- If you have access to a reliable chit group
- If you can negotiate better calling prices

### When is Bank FD Better?
- You want guaranteed, risk-free returns
- Lower breakeven amounts (chit call < breakeven amount)
- Peace of mind with government-backed guarantee

### Risk Comparison
| Aspect | Chit Fund | Bank FD |
|--------|-----------|---------|
| **Return Potential** | Higher | Fixed/Guaranteed |
| **Risk Level** | Higher | Very Low |
| **Liquidity** | Variable | Fixed |
| **Documentation** | Complex | Simple |
| **Default Risk** | Yes | No |

## Technical Details

### Discount Assumptions
The calculator uses a **5% standard discount** for breakeven calculation:
- **Estimated Range**: 5-10% (shows minimum and maximum scenarios)
- **Actual discounts** vary based on:
  - Demand for chit amounts
  - Group dynamics
  - Economic conditions
  - Participant creditworthiness

### Calculation Examples

#### Example 1: ₹100,000 for 12 months at 9% FD rate
- **FD Maturity**: ₹109,000
- **FD Interest**: ₹9,000
- **Breakeven Amount** (5% discount): ₹114,737
- **Your Chit Must Get**: At least ₹114,737 to beat FD

#### Example 2: ₹100,000 for 24 months at 9% FD rate
- **FD Maturity**: ₹118,810
- **FD Interest**: ₹18,810
- **Breakeven Amount** (5% discount): ₹125,063
- **Trend**: Longer terms increase breakeven amounts

## Installation & Setup

### For Web Browsers
1. Open `index.html` in any modern web browser
2. No installation or dependencies required!

### For Mobile Devices
1. **Android**: 
   - Open in Chrome/Firefox
   - Tap menu → "Install app" or "Add to Home Screen"
   - App will work offline after installation

2. **iOS**:
   - Open in Safari
   - Tap Share → "Add to Home Screen"
   - App will work offline after installation

### For Desktop (Windows/Mac/Linux)
- Simply open `index.html` in your preferred browser
- Bookmark for quick access

## Project Structure

```
chit_calculator/
├── index.html          # Main HTML structure
├── styles.css          # Responsive styling
├── script.js           # Calculator logic & interactions
├── manifest.json       # PWA configuration
├── service-worker.js   # Offline support
├── README.md          # This file
└── assets/            # Images and icons (optional)
```

## Browser Compatibility

✅ **Chrome** (v90+)
✅ **Firefox** (v88+)
✅ **Safari** (v14+)
✅ **Edge** (v90+)
✅ **Android Chrome**
✅ **iOS Safari**

## PWA Features (Progressive Web App)

This app works as a Progressive Web App:
- 📱 Installable on home screen
- 📴 Works offline (after first load)
- ⚡ Fast loading times
- 🔄 Automatic updates

## Disclaimer

⚠️ **Educational Tool Only**

This calculator is designed for educational and comparison purposes. It does not constitute financial advice. 

**Important Notes:**
- Actual chit fund returns depend on group dynamics and market conditions
- Consult with financial advisors before making investment decisions
- Chit funds are not regulated by banking authorities
- Always verify rates and terms with your financial institution

## Future Enhancements

- [ ] Add investment timeline visualization
- [ ] Multiple simultaneous calculations comparison
- [ ] Export results as PDF
- [ ] Historical data tracking
- [ ] Share results via email
- [ ] Chit group management features
- [ ] Push notifications for interest rate updates
- [ ] Dark mode support
- [ ] Multi-language support (Hindi, Tamil, Bengali)
- [ ] Advanced financial metrics

## Formula Reference

### Compound Interest (Annual Compounding)
```
A = P(1 + r/100)^n
CI = A - P
Where:
  A = Final Amount
  P = Principal
  r = Rate of Interest
  n = Time period (years)
  CI = Compound Interest
```

### Breakeven Calculation
```
Breakeven = FD_Maturity / (1 - discount%/100)
```

### Years from Months
```
Years = Months / 12
```

## Support & Feedback

For issues, suggestions, or improvements:
- Test across different devices
- Check browser console for errors
- Verify input values before calculating
- Clear browser cache if facing issues

## License

This calculator is provided as-is for educational purposes. Feel free to modify and use for personal or educational use.

---

**Last Updated**: March 2026
**Version**: 1.0.0

Happy Calculating! 💰📱
