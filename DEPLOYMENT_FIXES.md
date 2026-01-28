# Deployment Fixes & Solutions

## 🐍 Python Version Issues

### Problem: "python-build: definition not found: python-3.12"

**Platforms affected**: Netlify, some Heroku buildpacks, older hosting providers

**Solution**: Use Python 3.11 instead of 3.12

✅ **Fixed files**:
- `runtime.txt` → `python-3.11.10`
- `pyproject.toml` → `requires-python = ">=3.10"`

### Why This Happens
- Python 3.12 is relatively new
- Some hosting platforms haven't updated their build systems
- pyenv/python-build databases may be outdated

## 🚀 Recommended Deployment Platforms

### 1. Vercel (Best Choice) ⭐
- ✅ Supports Python 3.11 and 3.12
- ✅ Automatic Flask app detection
- ✅ Serverless functions
- ✅ Easy environment variables
- ✅ Built-in CDN

**Deploy**: Connect GitHub repo to Vercel dashboard

### 2. Railway
- ✅ Good Python support
- ✅ Automatic deployments
- ✅ Database support
- ✅ Simple configuration

**Deploy**: `railway login && railway deploy`

### 3. Render
- ✅ Flask-friendly
- ✅ Free tier available
- ✅ Automatic SSL
- ✅ Environment variables

**Deploy**: Connect GitHub repo to Render dashboard

### 4. PythonAnywhere
- ✅ Python-focused hosting
- ✅ Good for beginners
- ✅ Web-based file editor
- ✅ Multiple Python versions

**Deploy**: Upload files via web interface

## 🔧 Platform-Specific Fixes

### Netlify Issues
**Problem**: Netlify is designed for static sites, not Flask apps

**Solutions**:
1. **Use Vercel instead** (recommended)
2. Convert to static site with build process
3. Use Netlify Functions (requires restructuring)

### Heroku Issues
**Problem**: No free tier, requires specific buildpack

**Solutions**:
1. Use `python-3.11.10` in `runtime.txt`
2. Ensure `Procfile` exists: `web: gunicorn app:app`
3. Add `gunicorn` to `requirements.txt`

### Railway Issues
**Problem**: Usually works well, but may need configuration

**Solutions**:
1. Add `railway.toml` if needed
2. Set environment variables in dashboard
3. Use `python-3.11.10` in `runtime.txt`

## 📋 Pre-Deployment Checklist

### Required Files ✅
- [x] `app.py` - Main Flask application
- [x] `requirements.txt` - Python dependencies
- [x] `runtime.txt` - Python version (3.11.10)
- [x] `vercel.json` - Vercel configuration
- [x] `.env.example` - Environment template
- [x] `templates/` - HTML templates
- [x] `static/` - CSS/JS files

### Environment Variables ✅
- [x] `OPENWEATHER_API_KEY` - Weather API key
- [x] `SECRET_KEY` - Flask secret key
- [x] `AMAZON_AFFILIATE_TAG` - Affiliate tag (optional)

### Testing ✅
- [x] App runs locally: `python app.py`
- [x] All routes work: `/`, `/forecast`, `/search`, etc.
- [x] Weather API integration works
- [x] Static files load correctly

## 🆘 Common Error Solutions

### "Module not found" errors
```bash
# Solution: Check requirements.txt has all dependencies
pip freeze > requirements.txt
```

### "Template not found" errors
```bash
# Solution: Ensure templates/ directory is committed to git
git add templates/
git commit -m "Add templates"
```

### "Static files not loading"
```bash
# Solution: Ensure static/ directory is committed
git add static/
git commit -m "Add static files"
```

### "Environment variables not working"
```bash
# Solution: Set in platform dashboard, not just .env file
# Vercel: Project Settings → Environment Variables
# Railway: Project → Variables
# Render: Environment → Environment Variables
```

## 🎯 Quick Deploy Commands

### Vercel
```bash
npm i -g vercel
vercel login
vercel
# Follow prompts, set environment variables in dashboard
```

### Railway
```bash
npm i -g @railway/cli
railway login
railway deploy
# Set environment variables in dashboard
```

### Git Deployment (Most Platforms)
```bash
git add .
git commit -m "Fix Python version for deployment"
git push origin main
# Connect repo to hosting platform dashboard
```

## ✅ Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ App loads at provided URL
- ✅ Weather data displays correctly
- ✅ All navigation links work
- ✅ Static files (CSS/JS) load
- ✅ No console errors in browser

## 🔄 If Deployment Still Fails

1. **Check build logs** for specific error messages
2. **Verify all files are committed** to git repository
3. **Test locally first** with `python app.py`
4. **Use Vercel** - it has the best Flask support
5. **Check environment variables** are set correctly
6. **Clear build cache** and redeploy

## 📞 Platform Support

- **Vercel**: Excellent documentation, community support
- **Railway**: Good Discord community, responsive support
- **Render**: Comprehensive docs, email support
- **PythonAnywhere**: Forums, help pages

Choose Vercel for the smoothest deployment experience! 🚀