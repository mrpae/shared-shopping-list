# 🛒 Shopping List App

A beautiful Streamlit shopping list application with dark mode, bright colors, CSV storage, and Docker support with ngrok for external access.

## Features

- ✨ **Dark Mode Design** with bright, vibrant colors
- 🏷️ **Tag-like Display** for items with quantity badges
- ❌ **Easy Removal** - click "×" to remove individual items
- 📊 **Statistics Dashboard** showing total items and quantities
- 💾 **CSV Storage** - automatically saves your list to `shopping_list.csv`
- 🔄 **Auto-save** - your list persists between sessions
- 📱 **Responsive Design** - works on desktop and mobile
- 🐳 **Docker Support** - easy containerization
- 🌐 **Ngrok Integration** - expose your app to the internet
- 🛍️ **Shopping Mode** - table view with cart tracking
- 🔒 **Password Protection** - secure reset functionality

## Project Structure

```
├── dashboards/
│   ├── shopping_list_app.py      # Main application entry point
│   └── pages/
│       ├── shopping_list_page.py # Shopping list creation page
│       └── shopping_mode_page.py # Shopping mode with table view
├── data/                         # CSV storage directory
├── Dockerfile                    # Docker configuration
├── docker-compose.yml           # Docker Compose setup
├── requirements.txt             # Python dependencies
├── setup.bat                    # Windows setup script
├── dev_update.bat               # Docker development update script
├── env.example                  # Environment variables template
└── README.md                    # This file
```

## Quick Start (Windows 11)

### One-Click Setup
```cmd
# Double-click or run in Command Prompt:
setup.bat
```

### Manual Setup
```cmd
# 1. Get your ngrok auth token from https://dashboard.ngrok.com/get-started/your-authtoken

# 2. Create .env file
copy env.example .env
# Edit .env and add your NGROK_AUTHTOKEN

# 3. Run with Docker and ngrok
docker-compose --profile ngrok up --build
```

## Prerequisites

1. **Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Install and start Docker Desktop
   - Ensure WSL 2 is enabled (Docker Desktop will guide you)

2. **Ngrok Account**
   - Sign up at: https://ngrok.com
   - Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken

## Setup Instructions

### Step 1: Run Setup Script
```cmd
setup.bat
```

The setup script will:
- ✅ Check if Docker Desktop is running
- ✅ Create the data directory
- ✅ Prompt for your ngrok auth token
- ✅ Configure the `.env` file
- ✅ Start the app with Docker and ngrok

### Step 2: Access Your App
- **Local access:** http://localhost:8501
- **Ngrok dashboard:** http://localhost:4040
- **Public URL:** Check ngrok dashboard for the public URL

## Development & Updates

### Auto-Reload (Recommended)
- The app is configured with `STREAMLIT_SERVER_RUN_ON_SAVE=true`
- **Most changes auto-reload** when you save files
- **No restart needed** for code changes

### Manual Rebuild
```cmd
# Rebuild containers for updates
dev_update.bat

# OR manually:
docker-compose down
docker-compose --profile ngrok up --build
```

### What Triggers Auto-Reload:
- ✅ **Code changes** in `.py` files
- ✅ **CSS changes** in the app
- ✅ **Page modifications**
- ❌ **New dependencies** (requires rebuild)
- ❌ **Dockerfile changes** (requires rebuild)

## Docker Commands

```cmd
# Start with ngrok
docker-compose --profile ngrok up --build

# Run in background
docker-compose --profile ngrok up -d --build

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Restart for updates
docker-compose restart shopping-list-app
```

## Data Persistence

The app automatically saves your shopping list to:
- **Docker:** `/app/data/shopping_list.csv` (mounted to `./data/` on host)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NGROK_AUTHTOKEN` | Your ngrok authentication token | Required for ngrok |
| `STREAMLIT_SERVER_PORT` | Streamlit server port | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Streamlit server address | 0.0.0.0 |
| `STREAMLIT_SERVER_RUN_ON_SAVE` | Auto-reload on file changes | true |

## Troubleshooting

### Common Issues

**Docker Desktop not running:**
- Start Docker Desktop from the Start menu
- Wait for it to fully load (green icon in system tray)
- Try running `docker info` in Command Prompt

**Ngrok not working:**
- Check your auth token in `.env` file
- Verify ngrok account is active
- Check ngrok dashboard at http://localhost:4040

**Port already in use:**
```cmd
# Check what's using port 8501
netstat -ano | findstr :8501

# Kill the process or change port in docker-compose.yml
ports:
  - "8502:8501"  # Use different host port
```

**Changes not appearing:**
```cmd
# Rebuild containers
dev_update.bat

# OR manually:
docker-compose down
docker-compose --profile ngrok up --build
```

**WSL 2 issues:**
- Update Windows to latest version
- Enable WSL 2: `wsl --set-default-version 2`
- Restart Docker Desktop

## Features in Detail

### 🎨 Design
- Dark background with neon accents
- Gradient effects and animations
- Responsive layout with columns
- Hover effects and smooth transitions

### 📊 Data Management
- Automatic CSV file creation and updates
- Session state management for real-time updates
- Duplicate item detection (adds quantities together)
- Timestamp tracking for each item

### 🛠️ Technical Features
- Built with Streamlit for easy deployment
- Pandas for CSV data handling
- Custom CSS for styling
- Session state for persistent data
- Docker containerization with auto-reload
- Ngrok integration for external access
- Modular page structure for maintainability

## Customization

You can easily customize the app by modifying:
- **Colors:** Edit CSS variables in `dashboards/shopping_list_app.py`
- **Pages:** Modify files in `dashboards/pages/`
- **Ports:** Change in `docker-compose.yml`
- **Data location:** Modify volume mounts in `docker-compose.yml`

## Color Scheme
- Primary: `#00ff88` (neon green)
- Secondary: `#ff6b6b` (coral red)
- Accent: `#00ffff` (cyan)
- Background: `#0e1117` (dark)

## Windows Tips

- **Use PowerShell or Command Prompt** for running commands
- **Docker Desktop** must be running before using Docker commands
- **WSL 2** is required for Docker Desktop on Windows 11
- **File paths** use backslashes in Windows but forward slashes work in Docker
- **Environment variables** are case-sensitive in Docker
- **Auto-reload** works best with volume mounts in development

Enjoy your shopping! 🛍️
