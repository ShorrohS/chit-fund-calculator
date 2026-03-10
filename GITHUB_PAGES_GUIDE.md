# 🌐 Publishing via GitHub Pages

## ⚠️ Important: Two Versions of This Project

Your project has **two different apps**:

### **Version 1: Static HTML Calculator** (Can deploy to GitHub Pages)
- Files: `index.html`, `styles.css`, `script.js`
- Type: Pure frontend (no backend needed)
- Hosting: ✅ GitHub Pages (free, static)
- URL Example: `https://ShorrohS.github.io/chit-fund-calculator`
- Pros: Simple, fast, offline support via PWA
- Cons: Limited features, simpler calculations

### **Version 2: Streamlit Calculator** (Cannot deploy to GitHub Pages)
- Files: `streamlit_app.py`, `chit_logic.py`
- Type: Full-stack Python web app (needs backend)
- Hosting: ✅ Streamlit Cloud (free, recommended)
- URL Example: `https://chit-fund-calculator.streamlit.app`
- Pros: Advanced calculations, interactive, professional
- Cons: Requires backend server

---

## 🚀 Option A: Deploy HTML Version to GitHub Pages

GitHub Pages hosts **static files only** (HTML, CSS, JS). Your HTML calculator works perfectly here!

### Step-by-Step Guide

#### **1. Enable GitHub Pages**

In your GitHub repository (`https://github.com/ShorrohS/chit-fund-calculator`):

1. Click **Settings** (top right)
2. Left sidebar → **Pages**
3. Under "Build and deployment":
   - **Source:** Deploy from a branch
   - **Branch:** main
   - **Folder:** / (root)
4. Click **Save**

#### **2. GitHub Will Build & Deploy**

You'll see:
```
Your site is ready to be published at https://ShorrohS.github.io/chit-fund-calculator/
```

**That's it!** 🎉

#### **3. Access Your App**

Browser: `https://ShorrohS.github.io/chit-fund-calculator/`

---

## 🚀 Option B: Deploy Streamlit Version to Streamlit Cloud (Recommended for Full App)

If you want the **advanced Python version** (better calculations, more features), deploy to Streamlit Cloud instead.

### Why Streamlit Cloud?

✅ Free tier available  
✅ Automatic deployment from GitHub  
✅ Full Python capabilities  
✅ Real-time updates  
✅ Better calculations & visualizations  

### Step-by-Step Guide

#### **1. Create Streamlit Cloud Account**

Go to **https://streamlit.io/cloud**

- Sign up with GitHub
- Authorize Streamlit to access your GitHub repos

#### **2. Deploy Your App**

1. Click **"Create app"**
2. Fill in:
   - **GitHub account:** ShorrohS
   - **Repository:** chit-fund-calculator
   - **Branch:** main
   - **Main file path:** `streamlit_app.py`
3. Click **"Deploy"**

Streamlit automatically:
- Installs dependencies from `requirements.txt`
- Runs your Streamlit app
- Gives you a public URL

#### **3. Create requirements.txt**

If not already present, create `requirements.txt`:

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.16.0
```

Add to GitHub and commit:
```powershell
git add requirements.txt
git commit -m "Add requirements.txt for Streamlit Cloud"
git push origin main
```

#### **4. Your Live App**

URL will be: `https://chit-fund-calculator.streamlit.app`

(Or custom subdomain if you choose)

---

## 📊 Comparison: Which to Use?

| Feature | GitHub Pages (HTML) | Streamlit Cloud |
|---------|-------------------|-----------------|
| **Cost** | Free | Free |
| **Setup Time** | 2 minutes | 5 minutes |
| **Backend Needed** | ❌ No | ✅ Yes (provided) |
| **Calculations** | Basic | Advanced |
| **Charts** | Simple | Interactive |
| **Real-time Updates** | Manual refresh | Instant |
| **Python Support** | ❌ No | ✅ Yes |
| **Best For** | Quick demo | Production app |

---

## ✅ Do Both!

**Recommended approach:**

1. **GitHub Pages:** Static HTML version
   - URL: `https://ShorrohS.github.io/chit-fund-calculator/`
   - Purpose: Quick demo, offline access
   - Setup: 2 minutes

2. **Streamlit Cloud:** Full Python app
   - URL: `https://chit-fund-calculator.streamlit.app/`
   - Purpose: Primary app, all features
   - Setup: 5 minutes

---

## 🔧 GitHub Pages Setup (Detailed)

### **Step 1: Check Your Files are in GitHub**

Your repo should have these files at the root:
```
README.md
DEPLOYMENT.md
chit_logic.py
streamlit_app.py
index.html           ◄── This is the GitHub Pages entry point
styles.css
script.js
manifest.json
service-worker.js
.gitignore
run-streamlit.bat
... (other docs)
```

✅ Already have all these? Continue to Step 2.

### **Step 2: Go to Repository Settings**

1. Go to: `https://github.com/ShorrohS/chit-fund-calculator`
2. Click **Settings** tab (near top right)

### **Step 3: Find Pages Section**

Left sidebar:
- Scroll down to **"Pages"**
- Click it

### **Step 4: Configure GitHub Pages**

You'll see:

```
Build and deployment

Source
┌─────────────────────────┐
│ Deploy from a branch    │  ◄── Select this dropdown
└─────────────────────────┘

Branch
┌──────────────┐
│ main  / (root) │  ◄── Keep these defaults
└──────────────┘
```

- **Source:** "Deploy from a branch"
- **Branch:** "main"
- **Folder:** "/ (root)"

### **Step 5: Save**

Click the blue **"Save"** button.

### **Step 6: Wait for Build**

GitHub will show:
```
✓ Your site is live at https://ShorrohS.github.io/chit-fund-calculator/
```

This takes 30 seconds - 2 minutes.

You can check status: 
- Go to **Actions** tab
- See deployment progress

### **Step 7: Visit Your Site!**

Open browser:
```
https://ShorrohS.github.io/chit-fund-calculator/
```

---

## 🐛 Troubleshooting GitHub Pages

### **Problem: "404 Page not found"**

**Solution:** Make sure `index.html` is in the root of your GitHub repo.

Run in terminal:
```powershell
cd "C:\Users\NDH01061\Desktop\Personal\Working Prototypes_Projects\budget_tracking_app\chit_calculator"
ls index.html
```

If it shows the file, push to GitHub:
```powershell
git add index.html
git commit -m "Ensure index.html in root"
git push origin main
```

### **Problem: "GitHub Actions error"**

**Solution:** Check Actions tab for error details:
1. Go to **Actions** → **Deployments** → **Latest run**
2. Click the failed run
3. Look for error message
4. Usually just needs files to be properly pushed

### **Problem: "App not loading correctly"**

**Solution:** Check browser console for errors:
1. Open app in browser
2. Press **F12** (Developer Tools)
3. Check **Console** tab for red errors
4. Common issue: `styles.css` not found
   - Verify all CSS files are in root
   - Refresh page (Ctrl+F5)

---

## 🎯 Custom Domain (Optional)

Want to use your own domain (e.g., `chit.yoursite.com`)?

### **Add Custom Domain to GitHub Pages**

1. Settings → Pages
2. Under "Custom domain" field:
   - Enter: `chit.yoursite.com`
   - Click **Save**
3. Update your domain registrar DNS:
   - Add CNAME record pointing to `ShorrohS.github.io`

(Detailed DNS setup varies by registrar)

---

## 📱 Test on Mobile

### **After Deploying to GitHub Pages:**

1. Get public URL: `https://ShorrohS.github.io/chit-fund-calculator/`
2. On your phone:
   - Open browser
   - Go to that URL
   - Should work instantly (PWA enabled)
   - Add to home screen (optional)

### **After Deploying to Streamlit Cloud:**

1. Get public URL: `https://chit-fund-calculator.streamlit.app`
2. On your phone:
   - Open browser
   - Go to that URL
   - Full Streamlit app loads
   - Much more interactive!

---

## 📊 Monitor Your Site

### **GitHub Pages Analytics**

GitHub provides basic insights:

1. Settings → Pages
2. Scroll to bottom
3. See deployment history, status

### **Advanced Analytics (Optional)**

Add Google Analytics to `index.html`:

```html
<!-- Add to HEAD section of index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

Replace `GA_ID` with your Google Analytics ID.

---

## 🔐 Security Notes

GitHub Pages is **public** (read-only). Your code is visible to everyone.

✅ This is fine because:
- Users can't modify data
- No backend credentials exposed
- Standard for open-source projects

---

## 🚀 Next Steps

### **Immediate (Pick One):**

✅ **Option A: Quick Demo**
- Deploy HTML to GitHub Pages (2 minutes)
- URL: `https://ShorrohS.github.io/chit-fund-calculator/`

✅ **Option B: Full App**
- Deploy Streamlit to Streamlit Cloud (5 minutes)
- URL: `https://chit-fund-calculator.streamlit.app/`

✅ **Option C: Both** (Recommended)
- GitHub Pages for preview
- Streamlit Cloud for full features

---

## 📝 Deployment Checklist

### **For GitHub Pages (HTML):**
- [ ] `index.html` in root directory
- [ ] `styles.css` in root directory
- [ ] `script.js` in root directory
- [ ] `manifest.json` in root directory
- [ ] `service-worker.js` in root directory
- [ ] All files committed and pushed to main
- [ ] GitHub Pages enabled in Settings
- [ ] Wait 2-3 minutes for deployment
- [ ] Visit `https://ShorrohS.github.io/chit-fund-calculator/`
- [ ] Test on desktop and mobile

### **For Streamlit Cloud:**
- [ ] `streamlit_app.py` in root directory
- [ ] `chit_logic.py` in root directory
- [ ] `requirements.txt` with dependencies
- [ ] All files committed and pushed to main
- [ ] Streamlit Cloud account created
- [ ] App deployed from GitHub
- [ ] Wait 1-2 minutes for first build
- [ ] Visit Streamlit Cloud URL
- [ ] Test all tabs and features

---

## 💡 Pro Tips

1. **Share URLs easily:**
   - GitHub Pages: Shorter, easier to remember
   - Streamlit Cloud: Full features, better for serious users

2. **Update content:**
   - Just edit files, commit, push
   - Both deploy automatically!

3. **Custom branding:**
   - Edit `manifest.json` for app name/icon
   - Update about section in app

4. **Tell the world:**
   - Add to your portfolio
   - Share on Twitter, LinkedIn, Reddit
   - Trending on GitHub = more users!

---

## ❓ FAQ

**Q: Can I run Python on GitHub Pages?**  
A: No, GitHub Pages is static-only. Streamlit Cloud is needed for Python.

**Q: Will GitHub Pages be slow?**  
A: No, it's very fast! Hosted on GitHub's global CDN.

**Q: Do I need to pay after free tier?**  
A: Both GitHub Pages and Streamlit Cloud free tiers have no limits for public projects.

**Q: Can users submit data?**  
A: The HTML version runs locally (no backend). The Streamlit version can, but currently doesn't save data.

**Q: How often should I update?**  
A: As often as you want! Just git push and both deploy automatically.

---

**Ready to launch? Start with Step-by-Step Guide above!** 🚀
