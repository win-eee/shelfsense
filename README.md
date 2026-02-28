# 🛒 ShelfSense — Smart Inventory for Kirana Stores

> Helping small kirana store owners track stock, predict demand, and never run out of essentials — in English, Malayalam, and Hindi.

![ShelfSense Dashboard](https://drive.google.com/file/d/17YS8qTrIwobdHcHMeFxPZcgDR1jfpQPX/view?usp=sharing)

---

## 📖 Project Description

ShelfSense is a lightweight,  inventory management web app built for kirana (Indian small grocery) store owners. It runs entirely in the browser via Streamlit and stores data locally using SQLite — no internet or cloud account required. Owners can record daily sales, get automated restock alerts, track perishable items by expiry date, and send shopping lists directly to suppliers over WhatsApp, all in their preferred language.

Built for **Tink-her-hack 4.0 2026**.

---

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
| ![Dashboard](https://drive.google.com/file/d/17YS8qTrIwobdHcHMeFxPZcgDR1jfpQPX/view?usp=sharing) | ![Alerts](https://drive.google.com/file/d/1MgmKZAM9k1D4cgZw8CWAPTawripIq6Wt/view?usp=sharing) | ![Perishables](https://drive.google.com/file/d/1x6eeGJRoQNouFFQzktk5vYGVP9Xe7bl-/view?usp=sharing) |

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

🔗 **[shelfsense.streamlit.app](#)** *(add link after deploying)*

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
| Sreeyuktha Anil | Developer |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

*Made with ❤️ for kirana store owners everywhere.*
