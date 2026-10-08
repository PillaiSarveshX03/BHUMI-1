# BHUMI

**BHUMI** (भूमि) is a web application aimed at promoting smarter farming for a better tomorrow. The platform provides resources and information on agriculture, including crop data and related services, utilizing a clean, vanilla HTML/CSS/JS architecture.

## 📂 Project Structure

```text
BHUMI/
│
├── index.html           # Main landing page for the application
├── style.css            # Global stylesheet and styles for the home page
├── script.js            # Main JavaScript file containing interactive logic
├── README.md            # Project documentation (this file)
│
├── Pages/               # Contains HTML and CSS files for additional routes
│   ├── about.html       # About Us page
│   ├── about.css        # Stylesheet for the About page
│   ├── contact.html     # Contact page for connecting with the team
│   ├── contact.css      # Stylesheet for the Contact page
│   ├── database.html    # Database page (for exploring crop information)
│   ├── database.css     # Stylesheet for the Database page
│   ├── services.html    # Services offered page
│   └── services.css     # Stylesheet for the Services page
│
├── Data/                # Contains local data used in the application
│   └── crops.json       # JSON file storing data and information about different crops
│   
└── assets/              # Contains static media assets like images
    ├── ai-image.png
    ├── extend.png
    ├── region.png
    └── soil.png
```

## 🛠️ Tech Stack

- **HTML5:** Semantic layout and structure for all the pages.
- **CSS3:** Custom styling for a modern and responsive user interface, with per-page CSS files for maintainability.
- **Vanilla JavaScript:** Frontend logic, DOM manipulation, and handling of local JSON data.

## 🚀 Getting Started

To run the project locally, you don't need any special build tools or servers. 

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   ```
2. **Open the project:**
   Simply double-click the `index.html` file in the root directory to open it in your default web browser, or use a local server like VS Code's "Live Server" extension for a better development experience.

## ✨ Features

- **Home Page:** A welcoming landing page introducing the vision of BHUMI.
- **Crop Database:** Explores rich local data from `crops.json` to provide valuable agricultural insights.
- **Services:** Details on what the BHUMI platform offers to its users.
- **Contact:** An easy way to connect with the team.