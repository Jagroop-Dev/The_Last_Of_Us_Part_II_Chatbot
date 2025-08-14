# 🧟‍♀️ The Last of Us Part 2 - Interactive Chatbot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite%20%7C%20MySQL%20%7C%20PostgreSQL-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

> A comprehensive, data-driven chatbot companion for "The Last of Us Part 2" that provides instant access to game information without breaking immersion.

## 🎯 Overview

This interactive chatbot is designed specifically for "The Last of Us Part 2" players who want quick access to game information without alt-tabbing or breaking their gaming experience. It is built as a lightweight Windows application and it provides instant responses to questions about characters, locations, items, and weapons.

### 🎮 Why This Project?

- **Seamless Gaming Experience**: Access game information without leaving the game
- **Data-Driven Responses**: No AI hallucinations, only verified game data
- **Lightweight & Fast**: Optimized for minimal system impact
- **Easy Access**: Simple desktop shortcut integration

## ✨ Features

### 🔍 **Smart Query System**
- Character information and backstories
- Location details and descriptions
- Item properties and usage
- Weapon statistics and modifications

### 🗄️ **Robust Data Management**
- Structured SQL database with optimized queries
- Clean data preprocessing with Pandas
- Real-time data retrieval and formatting

### 🖥️ **User-Friendly Interface**
- Intuitive GUI built with modern Python frameworks
- Responsive design for quick information access
- Minimal resource footprint

### 📦 **Easy Deployment**
- Standalone Windows executable (.exe)
- One-click installation
- Desktop shortcut integration

## 🛠️ Technologies Used

| Category | Technologies |
|----------|-------------|
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white) |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white) |
| **GUI** | ![Tkinter](https://img.shields.io/badge/Tkinter-306998?style=flat&logo=python&logoColor=white) ![PyQt](https://img.shields.io/badge/PyQt-41CD52?style=flat&logo=qt&logoColor=white) |
| **Packaging** | ![PyInstaller](https://img.shields.io/badge/PyInstaller-3776AB?style=flat&logo=python&logoColor=white) |

## 🚀 Installation

### Prerequisites

- Windows 10/11

### How to use

1. **Download the latest release**
   ```
   Download TLOU2-Chatbot-v1.0.exe from the Releases page
   ```

2. **Run the installer**
   ```
   Double-click the downloaded .exe file
   ```

3. **Launch from desktop**
   ```
   Use the created desktop shortcut to launch the chatbot
   ```

## 💡 Usage

### Basic Queries

- **Character Info**: `"Tell me about Ellie"` or `"Who is Abby?"`
- **Location Details**: `"Describe Seattle"` or `"What's in the hospital?"`
- **Item Information**: `"What does the health kit do?"` or `"Find crafting materials"`
- **Weapon Stats**: `"Show me assault rifle stats"` or `"Compare shotguns"`
<!--
### Advanced Features

- **Filtered Searches**: Use specific keywords to narrow down results
- **Quick References**: Access frequently requested information instantly
- **Context-Aware Responses**: Get relevant information based on your query context
-->
## 📁 Project Structure

```
The_Last_Of_Us_Part_II_Chatbot/
├── 📂 Scraper/
│   ├── 📄 Game_Data_Scraper.ipynb  # Core scraping logic
├── 📂 Data/
│   ├── 📂 Images/                  # UI images and icons
│       ├── 📂 chapter_images             # Location images
│       ├── 📂 character_icon_images      # Character icons images
│       ├── 📂 character_images           # Character images
│       ├── 📂 enemy_images               # Enemy images
│       ├── 📂 how_to_kill_enemy_images   # How to kill enemy steps images
│       ├── 📂 safe_code_images           # How to find safe codes images
│       ├── 📂 tips_images                # Tip banner image
│       ├── 📂 trophy_images              # Trophy images
│       └── 📂 weapon_images              # Weapon images
│   ├── 📄 image_downloader.ipynb   # Image downloader
│   ├── 📄 chapter_data.csv         # Data on all game chapters
│   ├── 📄 character_data.csv       # Data on all game characters
│   ├── 📄 detailed_tips_data.csv   # Data on all game tip details
│   ├── 📄 tips_data.csv            # Data on all game tips
│   ├── 📄 enemy_data.csv           # Data on all game enemy types
│   ├── 📄 how_to_kill_enemy.csv    # Data on how to kill game enemies
│   ├── 📄 safe_codes_data.csv      # Data on all game safe codes
│   ├── 📄 safe_codes_.csv          # Data on all safe locations and details
│   ├── 📄 throphy_data.csv         # Data on all game achievements
│   ├── 📄 walkthrough_data.csv     # Data on all mission walkthroughs
│   ├── 📄 full_weapon_info.csv     # Data on all game weapon details
│   └── 📄 weapons_data.csv         # Data on all game weapons
└── 📄 README.md               # This file
```








<!--

├── 📂 assets/
│   ├── 📂 images/              # UI images and icons
│   └── 📂 fonts/               # Custom fonts
├── 📂 tests/
│   ├── 📄 test_database.py     # Database tests
│   └── 📄 test_chatbot.py      # Chatbot functionality tests
├── 📄 requirements.txt         # Python dependencies
├── 📄 setup.py                 # Application setup script



## 🔄 Development Phases

### ✅ Phase 1: Data Collection and Structuring
- [x] Gather comprehensive game data
- [x] Design normalized database schema
- [x] Create initial data structure

### ✅ Phase 2: Data Preprocessing and Database Population
- [x] Implement data cleaning with Pandas
- [x] Populate SQL database with processed data
- [x] Optimize database queries

### 🚧 Phase 3: Chatbot Development
- [x] Design user interface
- [x] Implement query processing logic
- [ ] Add advanced search features

### ⏳ Phase 4: Testing and Optimization
- [ ] Performance testing and optimization
- [ ] User experience testing
- [ ] Cross-system compatibility testing

### ⏳ Phase 5: Final Deployment
- [ ] Package as Windows executable
- [ ] Create installation documentation
- [ ] Release distribution

## 📊 Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| **Query Response Time** | < 100ms | 85ms |
| **Database Query Efficiency** | < 50ms | 32ms |
| **Memory Usage** | < 50MB | 38MB |
| **Startup Time** | < 3s | 2.1s |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Naughty Dog** - For creating the amazing world of The Last of Us Part 2
- **The Gaming Community** - For inspiration and feedback
- **Open Source Contributors** - For the tools and libraries that made this possible

## 📞 Support

- 📧 **Email**: your.email@example.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/tlou2-interactive-chatbot/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/tlou2-interactive-chatbot/discussions)

---

<div align="center">

**Made with ❤️ for The Last of Us Part 2 community**

[⬆ Back to Top](#-the-last-of-us-part-2---interactive-chatbot)

</div>
