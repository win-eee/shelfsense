# 🛒 ShelfSense — Smart Inventory for Kirana Stores

> Helping small kirana store owners track stock, predict demand, and never run out of essentials — in English, Malayalam, and Hindi.

[ShelfSense Dashboard](https://drive.google.com/file/d/17YS8qTrIwobdHcHMeFxPZcgDR1jfpQPX/view?usp=sharing)

---

## 📖 Project Description

ShelfSense is a lightweight,  inventory management web app built for kirana (Indian small grocery) store owners. It runs entirely in the browser via Streamlit and stores data locally using SQLite — no cloud account required. Owners can record daily sales, get automated restock alerts, track perishable items by expiry date, and send shopping lists directly to suppliers over WhatsApp, all in their preferred language.

Built for **Tink-her-hack 4.0 2026**.

---
## Problem Statement 
Small Kirana store owners in India face several inventory challenges:

| Challenge | Impact |
|-----------|--------|
| *Manual tracking* | Leads to errors and stockouts |
| *No demand forecasting* | Orders based on gut feeling, not data |
| *Language barrier* | Most inventory software is English-only |
| Overstocking/Understocking* | Either blocked capital or lost sales |
| No systematic reorder alerts* | Discover stock empty only when customer asks |
|  *WhatsApp-based ordering* | Requires manually typing lists for suppliers |

---
## Solution Overview

ShelfSense provides:

| Feature | Description |
|---------|-------------|
| *Real-time Dashboard* | See all products with color-coded stock status (Red- Critical, Yellow-  Low, Green- Good) |
| * Sales Tracking* | Record daily sales to build historical data |
| * Demand Prediction* | Simple average-based forecasting to suggest order quantities |
| *Smart Alerts* | Automatic identification of items needing restock |
| *WhatsApp Integration* | One-click sharing of shopping list with suppliers |
| *Multilingual UI* | English, Malayalam, and Hindi support |

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://shelfsense-8sqpj3inkgsbuhyhtc8vqr.streamlit.app/) |
| Database | SQLite (via Python `sqlite3`) |
| Data processing | Pandas |
| Language | Python 3.10+ |
| Deployment | Streamlit Community Cloud |

---

## ✨ Features

1. **📊 Live Dashboard** — Real-time stock cards with colour-coded status (Critical / Low / Good / Out of Stock), average daily sales, days-of-stock remaining, and sales trend indicators (📈 📉 ➡️).
2. **➕ Sales Recording** — Log what was sold each day; stock updates automatically and prevents over-selling.
3. **📦 Product Management** — Add new products, restock existing ones, and delete incorrect entries — all with a two-step confirmation guard.
4. **🔔 Smart Restock Alerts** — Automatically flags items below reorder level and generates a shopping list you can send to your supplier via WhatsApp in one tap.
5. **🥛 Perishable Items Tracker** — Assign expiry dates to products and get colour-coded warnings (Expired 🔴 / ≤3 days 🟠 / ≤7 days 🟡 / Fresh 🟢) with a WhatsApp expiry alert.
6. **🌐 Multilingual UI** — Full interface in **English**, **Malayalam**, and **Hindi** — switch languages instantly from the sidebar.
7. **📱 WhatsApp Integration** — One-click buttons to send restock shopping lists and expiry alerts directly to suppliers via WhatsApp.
8. **📈 Demand Prediction** — 7-day rolling average used to estimate how many days of stock remain and suggest optimal reorder quantities.

---

## 🖼️ Screenshots

| Dashboard | Alerts | Perishables |
|---|---|---|
| [Dashboard](https://drive.google.com/file/d/17YS8qTrIwobdHcHMeFxPZcgDR1jfpQPX/view?usp=sharing) | [Alerts](https://drive.google.com/file/d/1MgmKZAM9k1D4cgZw8CWAPTawripIq6Wt/view?usp=sharing) | [Perishables](https://drive.google.com/file/d/1x6eeGJRoQNouFFQzktk5vYGVP9Xe7bl-/view?usp=sharing) |

---

## 🎬 Demo Video

▶️ https://drive.google.com/file/d/12Zkhat1WJHaJZgeRfIHWeoklJrLfPcjb/view?usp=sharing

---

## 🏗️ Architecture

![Architecture Diagram](https://drive.google.com/file/d/1J-T6r9g_qKcLNDXdgOZ_61iK2zjkR8F_/view?usp=sharing)

The app follows a simple three-layer architecture:

- **UI layer** — Five Streamlit pages (Dashboard, Enter Sales, Products, Alerts, Perishables) rendered server-side.
- **Business logic layer** — Pure Python functions for demand prediction, trend analysis, expiry tracking, and alert generation.
- **Data layer** — Two SQLite tables (`products` and `sales`) stored locally in `shelfsense.db`.
- **i18n layer** — A `LABELS` dictionary provides all UI strings in English, Malayalam, and Hindi.

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/shelfsense.git
cd shelfsense

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`. Sample inventory data loads automatically on first run.

---

## 📁 Folder Structure

```
shelfsense/
├── app.py                  # Main application (entry point)
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
├── .gitignore
├── README.md
├── docs/
│   ├── architecture.svg    # Architecture diagram
│   └── screenshots/        # App screenshots
└── static/                 # Static assets (if any)
```

---

## 🌐 Live Demo

🔗 **[shelfsense.streamlit.app](#)** *(https://shelfsense-8sqpj3inkgsbuhyhtc8vqr.streamlit.app/)*

---

## 🤖 AI Tools Used

This project was built with assistance from **Claude (Anthropic)**. AI was used for:
- Generating boilerplate Streamlit layout and CSS theming
- Implementing the perishables expiry tracking feature
- Writing the multilingual label dictionaries (Malayalam and Hindi translations)
- Helping structure the README and architecture diagram

All code was reviewed, tested, and adjusted by the team.

---

## 👥 Team

| Name | Role |
|---|---|
| Hanna Vin Varghese | Lead Developer |
| Sreeyuktha Anil | Product Designer |

---
## 👥 Team Members & Contribution Summary

### *Hanna Vin Varghese* — Lead Developer

Hanna led the technical development as the core architect and coder of ShelfSense. She built the   infrastructure, including the Streamlit application framework and SQLite database integration. Hanna implemented the sales prediction algorithm that helps Kirana stores forecast demand based on historical sales data. Her focus was on writing clean, efficient, and maintainable code that would be reliable for everyday use by shopkeepers. She identified and analyzed the Razorpay problem statement.

*Key Contributions:*
- Core architecture and database design
- Streamlit framework implementation
- SQLite database integration
- Sales prediction algorithm development
-  Coding and functionality

---

### *Sreeyuktha Anil* — Product Designer

Sreeyuktha shaped the product vision and user experience. She conducted local user research. She analyzed the Razorpay problem statement  and ensured our technical solution aligned with their "Simplify Commerce for India" vision. Sreeyuktha designed the navigation system that makes the app accessible to first-time and older users, creating the color-coded alert system that allows shopkeepers to assess stock at a glance. She also handled all project documentation, user testing, and feedback incorporation.

*Key Contributions:*
- User research and requirement gathering
-  Navigation design
- Color-coded alert system
- Multilingual implementation
- Documentation and user testing

---

### *Collaborative Approach*

Together, we collaborated closely on problem-solving, feature ideation, and overall solution design. Our roles naturally complemented each other - while Hanna focused on *"making it work"* through robust code and technical implementation, Sreeyuktha focused on *"making it useful"* by deeply understanding user needs and designing intuitive experiences. We worked as a cohesive unit, with constant feedback loops between development and design, ensuring that every feature was both technically sound and genuinely helpful for shopkeepers.

By combining our strengths, we created an inventory system that speaks the language of local shopkeepers and fits seamlessly into their daily workflow - no training required, just open and use.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

*Made with ❤️ for kirana store owners everywhere.*
