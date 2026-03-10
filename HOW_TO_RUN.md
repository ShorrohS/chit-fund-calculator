# 🚀 How to Run the Chit Fund Calculator

## ✅ Quick Start (Recommended)

### Windows Users:
**Double-click this file in the chit_calculator folder:**
```
run-streamlit.bat
```

This will:
1. Start the Streamlit server
2. Automatically open http://localhost:8501 in your browser
3. Load the mobile-first Chit Fund Calculator

**That's it!** 🎉 The app is now running.

---

## 🔧 If the Batch File Doesn't Work

### Step 1: Open Terminal/PowerShell
```powershell
# Windows PowerShell
cd "C:\Users\NDH01061\Desktop\Personal\Working Prototypes_Projects\budget_tracking_app\chit_calculator"
```

### Step 2: Activate Virtual Environment
```powershell
# Windows
.\.venv\Scripts\Activate.ps1

# If you get a permission error:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Run Streamlit
```bash
streamlit run streamlit_app.py
```

### Step 4: Open in Browser
Streamlit will show something like:
```
Welcome to Streamlit!
If this is your first time using Streamlit, welcome!
...
Local URL: http://localhost:8501
```

Copy the **Local URL** and paste into your browser address bar.

---

## 📱 Mobile Testing

### Android (On Your Phone):
1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.x.x)

2. On your Android phone, open Chrome and go to:
   ```
   http://YOUR_IP_ADDRESS:8501
   ```
   Example: `http://192.168.1.10:8501`

### iOS (On Your iPhone):
Same as Android - find your IP and navigate to it in Safari.

---

## 🌐 Web Testing

Just use your computer browser:
```
http://localhost:8501
```

The app is fully responsive on:
- Desktop (1920px+)
- Tablets (768px+)
- Mobile phones (320px+)

---

## ⚙️ What's Running?

### Python Modules:
- **chit_logic.py** - Core calculation engine
  - Month-by-month chit simulation
  - Dividend tracking
  - Bank FD comparison
  - IRR calculations

- **streamlit_app.py** - Web interface (~600 lines)
  - 5 tabs: Summary, Analysis, Breakdown, Charts, Explanation
  - Mobile responsive design
  - Export CSV & reports
  - Real-time calculations

### Tech Stack:
- **Python 3.13**
- **Streamlit** - Web framework
- **Pandas** - Data tables
- **Plotly** - Interactive charts
- **NumPy** - Numerical calculations

---

## 🧪 Test the Logic First (Optional)

If you want to see the core calculation without the web UI:

```powershell
cd "C:\Users\NDH01061\Desktop\Personal\Working Prototypes_Projects\budget_tracking_app\chit_calculator"

# Activate venv
.\.venv\Scripts\Activate.ps1

# Run the logic test
python chit_logic.py
```

Output:
```
CHIT FUND CALCULATOR - TEST RESULTS
===================================
Total Invested: ₹904,990.40
Prize Received: ₹855,000.00
Net Profit: -₹49,990.40
Effective IRR: 0.00% p.a.

Bank FD Equivalent:
Maturity Amount: ₹1,350,749.10
Interest Earned: ₹445,758.69
```

---

## 🎯 Key Features

Once the app is running, you can:

1. **Adjust Parameters** (Left Sidebar):
   - Chit Corpus (₹)
   - Monthly Installment
   - Duration (months)
   - Call Month
   - Prize Percentage
   - Foreman Commission
   - Bank FD Rate

2. **View Results** (5 Tabs):
   - **Summary** - Quick comparison (Chit vs FD)
   - **Analysis** - Detailed numbers & breakeven
   - **Breakdown** - Month-by-month table
   - **Charts** - Visual comparisons
   - **Explanation** - How it works & risks

3. **Export Data**:
   - Download monthly data as CSV
   - Download summary report as TXT

---

## 🔌 Troubleshooting

### Problem: "streamlit: command not found"
**Solution:** Activate virtual environment first
```powershell
.\.venv\Scripts\Activate.ps1
```

### Problem: Imports not found (pandas, numpy, etc.)
**Solution:** Install dependencies
```powershell
.\.venv\Scripts\pip install pandas numpy plotly streamlit
```

### Problem: Port 8501 already in use
**Solution:** Kill existing process or use different port
```powershell
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

### Problem: Browser doesn't open automatically
**Solution:** Manually open the URL shown in terminal
```
Local URL: http://localhost:8501  <- Copy this
```

### Problem: App is slow
**Solution:** 
- Clear browser cache (Ctrl+Shift+Delete)
- Restart Streamlit (Ctrl+C, then run again)
- Check your internet connection

---

## 📊 Sample Calculation

**Input:**
- Corpus: ₹10,00,000
- Monthly: ₹10,000
- Months: 100
- Members: 100
- Call at: Month 50
- Prize: 90% of chit value
- FD Rate: 9% p.a.
- Discount: 10%

**Output:**
- Total Paid: ₹9,04,990
- Prize Received: ₹8,55,000
- Chit Profit: **-₹49,990** (Loss!)
- FD Profit: **₹4,45,759** (Better!)
- **Better Option: Bank FD** ✅

**Why Loss?** Prize (90%) is less than total paid, due to 10% discount shared as dividends to other members.

---

## 💡 Tips for Best Experience

1. **Start simple:** Use default parameters first
2. **Vary one thing:** Change call month, see impact
3. **Export results:** Download CSV for your records
4. **Mobile test:** Try on actual phone (responsive design)
5. **Check calculations:** Manual verification on Month 50 row

---

## 🚀 Next Steps

Once app is running:
1. Explore all 5 tabs
2. Download sample CSV
3. Try different scenarios
4. Share results with financial advisor
5. Make informed decision between Chit & FD

---

## 📞 Help & Support

### If you have questions:
1. Check the **"Explanation" tab** in the app
2. Review **calculation examples** in this README
3. Test with **simple numbers** first
4. Export **CSV data** to verify manually

### Common Scenarios to Test:
- Early call (Month 20): What if I need money sooner?
- Late call (Month 80): What if I save longer?
- High prize (95%): Best case scenario
- Low prize (80%): Worst case scenario
- Different rates (6%, 12%): How FD rate affects comparison

---

**Happy Calculating! 💰📱**

Your chit calculator is now ready to make smarter financial decisions!
