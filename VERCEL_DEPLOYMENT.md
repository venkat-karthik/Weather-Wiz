# Weather Wiz - Vercel Deployment Guide

## 🚀 Quick Deployment to Vercel

### Prerequisites
- GitHub account with your Weather Wiz repository
- Vercel account (free tier available)
- OpenWeatherMap API key

### Step 1: Prepare Your Repository
Make sure your repository has these files:
- ✅ `app_vercel.py` - Simplified Flask app for serverless
- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version specification
- ✅ All template files in `/templates` directory
- ✅ All static files in `/static` directory

### Step 2: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Python project
5. Click "Deploy"

#### Option B: Deploy via Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name: weather-wiz
# - Directory: ./
# - Override settings? No
```

### Step 3: Configure Environment Variables
In your Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add these variables:

```
OPENWEATHER_API_KEY=your_openweather_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
```

### Step 4: Custom Domain (Optional)
1. In Vercel dashboard, go to "Domains"
2. Add your custom domain
3. Follow DNS configuration instructions

## 📁 File Structure for Vercel

```
weather-wiz/
├── app_vercel.py          # Main Flask app (simplified for serverless)
├── weather_service.py     # Weather API service
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version
├── pyproject.toml       # Project metadata
├── .env                 # Environment variables (not deployed)
├── templates/           # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── forecast.html
│   ├── search.html
│   ├── map.html
│   ├── outfit_affiliate.html
│   ├── auth/
│   ├── errors/
│   └── legal/
└── static/             # CSS, JS, images
    ├── css/
    ├── js/
    └── images/
```

## ⚙️ Vercel Configuration Explained

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app_vercel.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app_vercel.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "PYTHONPATH": "."
  },
  "functions": {
    "app_vercel.py": {
      "maxDuration": 30
    }
  }
}
```

### Key Differences from Full App
The `app_vercel.py` is a simplified version that:
- ❌ Removes database dependencies (SQLAlchemy, migrations)
- ❌ Removes Redis dependencies (caching, sessions)
- ❌ Removes complex authentication system
- ❌ Removes admin dashboard
- ❌ Removes email system
- ✅ Keeps core weather functionality
- ✅ Keeps affiliate product display
- ✅ Keeps basic session management
- ✅ Keeps all templates and styling

## 🔧 Troubleshooting

### Common Issues

1. **Build Fails with uv.lock Error**
   - Solution: Delete `uv.lock` file (already done)
   - Use `requirements.txt` instead

2. **Import Errors**
   - Make sure all required files are in the repository
   - Check that `weather_service.py` is present

3. **Environment Variables Not Working**
   - Set them in Vercel dashboard, not just in `.env`
   - Redeploy after adding environment variables

4. **Static Files Not Loading**
   - Ensure `/static` directory is in your repository
   - Check file paths in templates

5. **Weather API Not Working**
   - Verify `OPENWEATHER_API_KEY` is set correctly
   - Check API key is valid and has quota

### Testing Your Deployment

After deployment, test these URLs:
- `https://your-app.vercel.app/` - Main page
- `https://your-app.vercel.app/forecast` - Forecast page
- `https://your-app.vercel.app/search` - City search
- `https://your-app.vercel.app/outfit-affiliate` - Outfit marketplace
- `https://your-app.vercel.app/health` - Health check

## 🌟 Features Available on Vercel

✅ **Working Features:**
- Weather dashboard with real-time data
- City search and management
- Weather forecasts (hourly/daily)
- Interactive weather map
- Outfit marketplace with affiliate products
- Responsive design with dark/light themes
- Basic session management

❌ **Not Available (Serverless Limitations):**
- User registration/authentication
- Database persistence
- Admin dashboard
- Email notifications
- Advanced analytics
- Background tasks

## 🚀 Going Live Checklist

- [ ] Repository is public or Vercel has access
- [ ] All template files are committed
- [ ] All static files (CSS/JS) are committed
- [ ] `OPENWEATHER_API_KEY` environment variable is set
- [ ] `SECRET_KEY` environment variable is set
- [ ] Test all main pages work
- [ ] Test weather API integration
- [ ] Test affiliate product display
- [ ] Test responsive design on mobile

## 📈 Next Steps

After successful Vercel deployment:
1. **Custom Domain**: Add your own domain name
2. **Analytics**: Add Vercel Analytics or Google Analytics
3. **Performance**: Monitor Core Web Vitals
4. **SEO**: Add meta tags and structured data
5. **CDN**: Optimize static asset delivery

Your Weather Wiz app will be live at: `https://your-project-name.vercel.app`

## 💡 Pro Tips

1. **Fast Deployments**: Vercel deploys automatically on git push
2. **Preview Deployments**: Every branch gets a preview URL
3. **Edge Functions**: Consider upgrading for better performance
4. **Monitoring**: Use Vercel's built-in monitoring tools
5. **Scaling**: Vercel handles scaling automatically

Happy deploying! 🎉