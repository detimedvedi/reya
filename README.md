# 🚀 Reya Chain Points Analytics Dashboard

Comprehensive analytics dashboard for Reya Chain Points leaderboard with 84,615+ participants. Real-time visualization and analysis of trading, staking, and signal points across the entire Reya ecosystem.

## 🌐 Live Demo

**🔗 [https://reya-points-dashboard.vercel.app/](https://reya-points-dashboard.vercel.app/)**

## ✨ Features

- **📊 Complete Dataset**: Full leaderboard with 84,615+ users
- **📈 Interactive Charts**: Distribution analysis, scatter plots, percentile rankings
- **🔍 Advanced Filtering**: Search by wallet address, points range, and categories
- **🎯 Multi-Category Analysis**: Trading, Staking, and Signal Points breakdown
- **📱 Responsive Design**: Optimized for desktop and mobile devices
- **🔄 Auto-Updates**: Daily data refresh at 01:00 UTC via GitHub Actions
- **⚡ Fast Performance**: Static site with optimized JSON data loading

## 🏗️ Project Structure

```
reya/
├── index.html                          # Main dashboard (frontend)
├── reya_complete_leaderboard.json      # Complete leaderboard data (84,615+ users)
├── fetch_complete_leaderboard.py       # Basic API fetcher
├── fetch_complete_leaderboard_v2.py    # Advanced fetcher with detailed logging
├── analytics_processor.py              # Python analytics & visualization tools
├── test_api.py                         # API testing suite
├── test_update_cycle.py                # Update cycle testing
├── vercel.json                         # Vercel deployment config
├── package.json                        # Project metadata
└── .github/workflows/update-data.yml   # GitHub Actions workflow
```

## 🔧 Tech Stack

### Frontend
- **HTML5/CSS3/JavaScript (ES6+)**: Pure vanilla JS, no frameworks
- **Chart.js**: Interactive data visualizations
- **Responsive Design**: Mobile-first approach

### Backend & Data
- **Python 3.11**: Data fetching and processing
- **Requests**: HTTP client for API calls
- **Pandas/NumPy**: Advanced analytics (optional)
- **Matplotlib/Seaborn**: Data visualization (optional)

### Infrastructure
- **Hosting**: Vercel (static site)
- **CI/CD**: GitHub Actions
- **Data Source**: Reya Chain API
- **Auto-Deploy**: Push to main branch triggers deployment

## 📈 Data Sources

- **API Endpoint**: `https://api.reya.xyz/api/incentives/leaderBoard/total`
- **Update Schedule**: Daily at 01:00 UTC
- **Total Participants**: 84,615+ users
- **Point Categories**: 
  - 💹 Trading Points
  - 🔒 Staking Points
  - 📡 Signal Points

## 🚀 Quick Start

### View Dashboard Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/detimedvedi/reya.git
   cd reya
   ```

2. **Open in browser**
   ```bash
   # Option 1: Direct file open
   open index.html
   
   # Option 2: Local server (recommended)
   python -m http.server 3000
   # Visit http://localhost:3000
   ```

### Fetch Latest Data

```bash
# Install dependencies
pip install requests

# Basic fetch
python fetch_complete_leaderboard.py

# Advanced fetch with detailed logging
python fetch_complete_leaderboard_v2.py
```

### Run Analytics

```bash
# Install analytics dependencies
pip install pandas numpy matplotlib seaborn

# Generate analytics report
python analytics_processor.py
```

### Test API

```bash
# Run comprehensive API tests
python test_api.py
```

## 📊 Analytics Features

### Dashboard Visualizations
- **Points Distribution**: Histogram showing user point ranges
- **Category Breakdown**: Pie chart of Trading/Staking/Signal points
- **Top 50 Leaderboard**: Real-time rankings
- **Percentile Analysis**: User segmentation by performance
- **Scatter Plots**: Trading vs Staking correlation

### Python Analytics (`analytics_processor.py`)
- **User Segmentation**: Whale/High Performer/Active/Regular/New users
- **Strategy Analysis**: Trading-focused, Staking-focused, Balanced strategies
- **Correlation Analysis**: Point type relationships
- **Top Performers**: Detailed analysis of top 100 users
- **Export Reports**: JSON format with comprehensive statistics

## 🔄 Automated Updates

### GitHub Actions Workflow

The project uses GitHub Actions to automatically update data daily:

1. **Schedule**: Runs at 01:00 UTC every day
2. **Fetch**: Executes `fetch_complete_leaderboard_v2.py`
3. **Commit**: Pushes updated JSON if data changed
4. **Deploy**: Vercel auto-deploys on push to main

**Manual Trigger**: Go to Actions tab → "Update Reya Leaderboard Data" → Run workflow

### Vercel Configuration

- **Output Directory**: `.` (root)
- **Build Command**: Static site (no build needed)
- **Cache Headers**: 
  - General: 1 hour
  - JSON data: 5 minutes
- **CORS**: Enabled for JSON endpoint

## 🧪 Testing

### API Testing Suite (`test_api.py`)

Comprehensive tests for API behavior:
- ✅ Response structure validation
- ✅ Pagination mechanism testing
- ✅ Alternative endpoint discovery
- ✅ Query parameter variations
- ✅ Current data file analysis

```bash
python test_api.py
```

## 📱 Responsive Design

- **Desktop**: Full-featured dashboard with all charts
- **Tablet**: Optimized layout with responsive charts
- **Mobile**: Touch-friendly interface with collapsible sections
- **Performance**: Lazy loading for large datasets

## 🎯 Key Metrics

- **Total Participants**: 84,615+ users
- **Total Points Distributed**: Millions across all categories
- **Update Frequency**: Daily
- **Data Freshness**: < 24 hours
- **API Response Time**: < 2 seconds
- **Dashboard Load Time**: < 3 seconds

## 🛠️ Development

### File Descriptions

- **`index.html`**: Complete frontend dashboard with Chart.js visualizations
- **`fetch_complete_leaderboard.py`**: Simple API fetcher (legacy)
- **`fetch_complete_leaderboard_v2.py`**: Production fetcher with pagination handling, logging, and error recovery
- **`analytics_processor.py`**: Advanced analytics engine with segmentation, strategy analysis, and visualization
- **`test_api.py`**: API testing and validation suite
- **`reya_complete_leaderboard.json`**: Complete dataset with metadata and 84,615+ user records

### Adding New Features

1. **Frontend**: Edit `index.html` (self-contained)
2. **Data Processing**: Modify `fetch_complete_leaderboard_v2.py`
3. **Analytics**: Extend `analytics_processor.py`
4. **Deployment**: Push to main branch (auto-deploys)

## 📦 Dependencies

### Required (Data Fetching)
```bash
pip install requests
```

### Optional (Analytics)
```bash
pip install pandas numpy matplotlib seaborn
```

### Frontend
No dependencies - pure vanilla JavaScript with CDN-loaded Chart.js

## 🚨 Troubleshooting

### Data Not Updating
- Check GitHub Actions logs
- Verify API endpoint is accessible
- Ensure `fetch_complete_leaderboard_v2.py` runs successfully

### Dashboard Not Loading
- Check browser console for errors
- Verify `reya_complete_leaderboard.json` exists
- Clear browser cache

### Vercel Deployment Issues
- Verify `vercel.json` configuration
- Check build logs in Vercel dashboard
- Ensure `outputDirectory` is set to `.`

## 📄 License

MIT License - feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review API testing results

---

**Built with ❤️ for the Reya Chain community**

*Last updated: Auto-updated daily via GitHub Actions*
