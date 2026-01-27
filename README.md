# Weather Wiz ⛅

A beautiful, responsive weather application with outfit recommendations and affiliate shopping integration. Built with Flask and optimized for Vercel deployment.

## 🌟 Features

- **Real-time Weather Data** - Powered by OpenWeatherMap API
- **Weather Forecasts** - Hourly and daily forecasts
- **Interactive Weather Map** - Visual weather exploration
- **Outfit Recommendations** - Weather-based clothing suggestions
- **Affiliate Marketplace** - Amazon affiliate product integration
- **Responsive Design** - Beautiful UI with dark/light themes
- **City Management** - Save and manage favorite cities

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/weather-wiz)

### Prerequisites
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))
- Amazon Affiliate Tag (optional, for affiliate features)

### Environment Variables
Set these in your Vercel dashboard:

```
OPENWEATHER_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
AMAZON_AFFILIATE_TAG=your-affiliate-tag-20
```

## 🛠️ Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/weather-wiz.git
   cd weather-wiz
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
weather-wiz/
├── app.py                    # Main Flask application
├── weather_service.py       # Weather API integration
├── affiliate_products.py    # Product database
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel deployment config
├── runtime.txt             # Python version
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── forecast.html
│   ├── search.html
│   ├── map.html
│   ├── outfit_affiliate.html
│   ├── errors/
│   └── legal/
└── static/                 # CSS, JS, images
    ├── css/
    └── js/
```

## 🎨 Features Overview

### Weather Dashboard
- Current weather conditions
- Temperature, humidity, wind speed
- Weather icons and descriptions
- Location-based weather data

### Forecast System
- 24-hour hourly forecasts
- 7-day daily forecasts
- Detailed weather information
- Interactive forecast display

### Outfit Recommendations
- Weather-appropriate clothing suggestions
- Amazon affiliate product integration
- Categorized by clothing type
- Price and rating information

### City Management
- Search and add cities
- Save favorite locations
- Quick city switching
- Session-based storage

## 🔧 Configuration

### Weather API
Get your free API key from [OpenWeatherMap](https://openweathermap.org/api):
1. Sign up for a free account
2. Generate an API key
3. Add to environment variables

### Affiliate Products
Update `affiliate_products.py` with your Amazon affiliate products:
1. Get your Amazon Associate tag
2. Add product ASINs and details
3. Configure affiliate URLs

## 🌐 Deployment

### Vercel (Recommended)
1. Fork this repository
2. Connect to Vercel
3. Set environment variables
4. Deploy automatically

### Other Platforms
- **Heroku**: Use `requirements.txt` and `runtime.txt`
- **Railway**: Direct deployment support
- **PythonAnywhere**: Upload and configure
- **DigitalOcean**: Use App Platform

## 📱 Responsive Design

Weather Wiz is fully responsive and works great on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktop computers
- 🖥️ Large screens

## 🎯 Performance

- ⚡ Fast loading times
- 🔄 Efficient API calls
- 💾 Smart caching
- 📊 Optimized assets

## 🔒 Privacy & Security

- 🛡️ Secure API key handling
- 🔐 Session-based storage
- 🚫 No personal data collection
- ✅ GDPR compliant

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for weather data
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Vercel](https://vercel.com/) for hosting platform
- [Amazon Associates](https://affiliate-program.amazon.com/) for affiliate program

## 📞 Support

For support and questions:
- 📧 Email: support@weatherwiz.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/weather-wiz/issues)
- 📖 Docs: [Documentation](https://github.com/your-username/weather-wiz/wiki)

---

Made with ❤️ by [Your Name](https://github.com/your-username)

⭐ Star this repo if you found it helpful!