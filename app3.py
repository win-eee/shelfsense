import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(page_title="ShelfSense", page_icon="🛒", layout="wide")

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    body, .main, .block-container {
        background-color: #E6F0FA !important;
    }
    .stApp {
        background-color: #E6F0FA !important;
    }
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
        color: #1A3B5D !important;
    }
    h1, h2, h3, h4 {
        color: #1A3B5D !important;
        font-weight: 700 !important;
    }
    [data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 2px solid #88BDA3 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    [data-testid="metric-container"] * { color: #1A3B5D !important; }
    .stTextInput input {
        color: #1A3B5D !important;
        background-color: #ffffff !important;
        border: 1px solid #88BDA3 !important;
    }
    .stSelectbox div { color: #1A3B5D !important; background-color: #ffffff !important; }
    .stNumberInput input {
        color: #1A3B5D !important;
        background-color: #ffffff !important;
        border: 1px solid #88BDA3 !important;
    }
    .stButton button {
        background-color: #1A3B5D !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    .stButton button:hover { background-color: #D4AF37 !important; color: #1A3B5D !important; }
    .stAlert { color: #1A3B5D !important; }
    hr { border-color: #88BDA3 !important; }
    /* Remove streamlit black header */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    /* Remove gap left by hidden header */
    .block-container {
        padding-top: 1rem !important;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background-color: #1A3B5D !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] a {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #2C5282 !important;
        border: 1px solid #88BDA3 !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        background-color: #2C5282 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] label:hover {
        color: #D4AF37 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── DATABASE ────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('shelfsense.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, category TEXT,
                  current_stock REAL, unit TEXT, reorder_level REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY, product_id INTEGER,
                  quantity REAL, date TEXT)''')
    conn.commit()
    conn.close()

def get_conn():
    return sqlite3.connect('shelfsense.db')

def load_sample_data():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        products = [
            ('Atta 10kg',        'Grains',        15, 'bags',    5),
            ('Rice 5kg',         'Grains',         8, 'bags',    4),
            ('Toor Dal 1kg',     'Pulses',         20, 'packets', 8),
            ('Sunflower Oil 1L', 'Oil',             6, 'bottles', 5),
            ('Sugar 1kg',        'Essentials',     12, 'packets', 6),
            ('Tea Powder 500g',  'Beverages',       9, 'packets', 4),
            ('Biscuits Parle-G', 'Snacks',         40, 'packets',15),
            ('Soap Lifebuoy',    'Personal Care',  18, 'bars',    8),
            ('Salt 1kg',         'Essentials',     11, 'packets', 5),
            ('Coconut Oil 500ml','Oil',             4, 'bottles', 4),
        ]
        c.executemany(
            "INSERT INTO products (name,category,current_stock,unit,reorder_level) VALUES (?,?,?,?,?)",
            products)
        import random
        for days_ago in range(10, 0, -1):
            date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            for pid in range(1, 11):
                qty = random.randint(1, 5)
                c.execute("INSERT INTO sales (product_id,quantity,date) VALUES (?,?,?)",
                          (pid, qty, date))
        conn.commit()
    conn.close()

def get_products():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    return df

def get_prediction(product_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT quantity FROM sales WHERE product_id=? ORDER BY date DESC LIMIT 7", (product_id,))
    sales = [r[0] for r in c.fetchall()]
    conn.close()
    if not sales:
        return 0
    return round(sum(sales) / len(sales), 1)

def get_trend(product_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT quantity FROM sales WHERE product_id=? ORDER BY date DESC LIMIT 14", (product_id,))
    sales = [r[0] for r in c.fetchall()]
    conn.close()
    if len(sales) < 2:
        return "⚪ Not enough data"
    recent   = sales[:7]
    previous = sales[7:] if len(sales) > 7 else sales
    r_avg = sum(recent) / len(recent)
    p_avg = sum(previous) / len(previous)
    if p_avg == 0:
        return "⚪ No trend data"
    change = ((r_avg - p_avg) / p_avg) * 100
    if change > 10:    return f"📈 Selling faster (+{round(change)}%)"
    elif change < -10: return f"📉 Selling slower ({round(change)}%)"
    return "➡️ Stable"

def get_days_of_data(product_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(DISTINCT date) FROM sales WHERE product_id=?", (product_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def add_sale(product_id, quantity):
    conn = get_conn()
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute("INSERT INTO sales (product_id,quantity,date) VALUES (?,?,?)", (product_id, quantity, today))
    c.execute("UPDATE products SET current_stock = current_stock - ? WHERE id = ?", (quantity, product_id))
    conn.commit()
    conn.close()

def add_product(name, category, stock, unit, reorder):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO products (name,category,current_stock,unit,reorder_level) VALUES (?,?,?,?,?)",
              (name, category, stock, unit, reorder))
    conn.commit()
    conn.close()

def restock_product(product_id, quantity):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE products SET current_stock = current_stock + ? WHERE id = ?", (quantity, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    c.execute("DELETE FROM sales WHERE product_id=?", (product_id,))
    conn.commit()
    conn.close()

# ─── INIT ────────────────────────────────────────────────────────────────────
init_db()
load_sample_data()

# ─── SESSION STATE ───────────────────────────────────────────────────────────
if 'sale_success' not in st.session_state:
    st.session_state.sale_success = None
if 'add_success' not in st.session_state:
    st.session_state.add_success = None
if 'restock_success' not in st.session_state:
    st.session_state.restock_success = None
if 'delete_success' not in st.session_state:
    st.session_state.delete_success = None

# ─── LANGUAGE LABELS ─────────────────────────────────────────────────────────
LABELS = {
    "English": {
        "title": "ShelfSense",
        "subtitle": "Smart Inventory for Kirana Stores",
        "navigate": "Navigate",
        "dashboard": "🏠 Dashboard",
        "enter_sales": "➕ Enter Sales",
        "products": "📦 Products",
        "alerts": "🔔 Alerts",
        "filter_cat": "Filter by Category",
        "all_cat": "All Categories",
        "search": "🔍 Search products...",
        "total": "Total Products",
        "critical": "🔴 Critical",
        "low": "🟡 Low Stock",
        "stock": "Stock",
        "avg_day": "Avg/day",
        "days_left": "Days left",
        "suggest": "Suggest order",
        "restock_now": "CRITICAL – Restock Now!",
        "running_low": "🟡 Running Low",
        "good": "🟢 Good",
        "out": "🔴 OUT OF STOCK",
        "record_title": "➕ Record Today's Sales",
        "record_sub": "Update stock by entering what you sold today",
        "select_prod": "Select Product",
        "qty_sold": "Quantity Sold",
        "record_btn": "Record Sale ✅",
        "prod_title": "📦 Manage Products",
        "add_tab": "➕ Add New Product",
        "restock_tab": "🔄 Restock Existing",
        "prod_name": "Product Name (e.g. Maggi 70g)",
        "category": "Category",
        "unit": "Unit",
        "curr_stock": "Current Stock",
        "reorder_lvl": "Reorder Level",
        "add_btn": "Add Product ✅",
        "restock_btn": "Restock ✅",
        "qty_add": "Quantity to Add",
        "alerts_title": "🔔 Restock Alerts & Shopping List",
        "alerts_sub": "Items that need your attention today",
        "all_good": "✅ All stocks are at healthy levels!",
        "shopping_list": "🛒 Today's Shopping List",
        "copy_hint": "Copy this list and share on WhatsApp with your supplier!",
        "no_sales": "No sales yet",
        "no_products": "No products found.",
        "enter_name": "Please enter a product name.",
        "overview": "📊 Stock Overview",
        "navy_label": "🔵 Navy = Current Stock",
        "gold_label": "🟡 Gold = Reorder Level",
        "all_products": "📋 All Products",
    },
    "Malayalam": {
        "title": "ShelfSense",
        "subtitle": "കിരാന കടകൾക്കുള്ള സ്മാർട്ട് ഇൻവെന്ററി",
        "navigate": "നാവിഗേറ്റ്",
        "dashboard": "🏠 ഡാഷ്ബോർഡ്",
        "enter_sales": "➕ വിൽപ്പന നൽകുക",
        "products": "📦 ഉൽപ്പന്നങ്ങൾ",
        "alerts": "🔔 അലേർട്ടുകൾ",
        "filter_cat": "വിഭാഗം തിരഞ്ഞെടുക്കുക",
        "all_cat": "എല്ലാ വിഭാഗങ്ങളും",
        "search": "🔍 ഉൽപ്പന്നം തിരയുക...",
        "total": "മൊത്തം ഉൽപ്പന്നങ്ങൾ",
        "critical": "🔴 അടിയന്തിരം",
        "low": "🟡 കുറഞ്ഞ സ്റ്റോക്ക്",
        "stock": "സ്റ്റോക്ക്",
        "avg_day": "ശരാശരി/ദിവസം",
        "days_left": "ദിവസങ്ങൾ ശേഷിക്കുന്നു",
        "suggest": "ഓർഡർ നിർദ്ദേശം",
        "restock_now": "അടിയന്തിരം – ഇപ്പോൾ വാങ്ങുക!",
        "running_low": "🟡 കുറഞ്ഞുവരുന്നു",
        "good": "🟢 നല്ലത്",
        "out": "🔴 സ്റ്റോക്ക് തീർന്നു",
        "record_title": "➕ ഇന്നത്തെ വിൽപ്പന രേഖപ്പെടുത്തുക",
        "record_sub": "ഇന്ന് വിറ്റത് നൽകി സ്റ്റോക്ക് അപ്ഡേറ്റ് ചെയ്യുക",
        "select_prod": "ഉൽപ്പന്നം തിരഞ്ഞെടുക്കുക",
        "qty_sold": "വിറ്റ അളവ്",
        "record_btn": "വിൽപ്പന രേഖപ്പെടുത്തുക ✅",
        "prod_title": "📦 ഉൽപ്പന്നങ്ങൾ നിയന്ത്രിക്കുക",
        "add_tab": "➕ പുതിയ ഉൽപ്പന്നം",
        "restock_tab": "🔄 സ്റ്റോക്ക് നിറയ്ക്കുക",
        "prod_name": "ഉൽപ്പന്നത്തിന്റെ പേര്",
        "category": "വിഭാഗം",
        "unit": "യൂണിറ്റ്",
        "curr_stock": "നിലവിലെ സ്റ്റോക്ക്",
        "reorder_lvl": "റീഓർഡർ ലെവൽ",
        "add_btn": "ഉൽപ്പന്നം ചേർക്കുക ✅",
        "restock_btn": "സ്റ്റോക്ക് നിറയ്ക്കുക ✅",
        "qty_add": "ചേർക്കേണ്ട അളവ്",
        "alerts_title": "🔔 റീസ്റ്റോക്ക് അലേർട്ടുകൾ",
        "alerts_sub": "ഇന്ന് ശ്രദ്ധിക്കേണ്ട ഇനങ്ങൾ",
        "all_good": "✅ എല്ലാ സ്റ്റോക്കും നല്ല നിലയിലാണ്!",
        "shopping_list": "🛒 ഇന്നത്തെ വാങ്ങൽ പട്ടിക",
        "copy_hint": "ഈ പട്ടിക കോപ്പി ചെയ്ത് സപ്ലയർക്ക് WhatsApp ചെയ്യുക!",
        "no_sales": "വിൽപ്പന ഇല്ല",
        "no_products": "ഉൽപ്പന്നങ്ങൾ കണ്ടെത്തിയില്ല.",
        "enter_name": "ഉൽപ്പന്നത്തിന്റെ പേര് നൽകുക.",
        "overview": "📊 സ്റ്റോക്ക് അവലോകനം",
        "navy_label": "🔵 നേവി = നിലവിലെ സ്റ്റോക്ക്",
        "gold_label": "🟡 സ്വർണ്ണം = റീഓർഡർ ലെവൽ",
        "all_products": "📋 എല്ലാ ഉൽപ്പന്നങ്ങളും",
    },
    "Hindi": {
        "title": "ShelfSense",
        "subtitle": "किराना दुकानों के लिए स्मार्ट इन्वेंटरी",
        "navigate": "नेविगेट",
        "dashboard": "🏠 डैशबोर्ड",
        "enter_sales": "➕ बिक्री दर्ज करें",
        "products": "📦 उत्पाद",
        "alerts": "🔔 अलर्ट",
        "filter_cat": "श्रेणी चुनें",
        "all_cat": "सभी श्रेणियाँ",
        "search": "🔍 उत्पाद खोजें...",
        "total": "कुल उत्पाद",
        "critical": "🔴 गंभीर",
        "low": "🟡 कम स्टॉक",
        "stock": "स्टॉक",
        "avg_day": "औसत/दिन",
        "days_left": "दिन शेष",
        "suggest": "ऑर्डर सुझाव",
        "restock_now": "गंभीर – अभी मंगाएं!",
        "running_low": "🟡 कम हो रहा है",
        "good": "🟢 ठीक है",
        "out": "🔴 स्टॉक खत्म",
        "record_title": "➕ आज की बिक्री दर्ज करें",
        "record_sub": "आज क्या बेचा वो डालें और स्टॉक अपडेट करें",
        "select_prod": "उत्पाद चुनें",
        "qty_sold": "बेची गई मात्रा",
        "record_btn": "बिक्री दर्ज करें ✅",
        "prod_title": "📦 उत्पाद प्रबंधित करें",
        "add_tab": "➕ नया उत्पाद जोड़ें",
        "restock_tab": "🔄 स्टॉक भरें",
        "prod_name": "उत्पाद का नाम (जैसे Maggi 70g)",
        "category": "श्रेणी",
        "unit": "इकाई",
        "curr_stock": "वर्तमान स्टॉक",
        "reorder_lvl": "रीऑर्डर स्तर",
        "add_btn": "उत्पाद जोड़ें ✅",
        "restock_btn": "स्टॉक भरें ✅",
        "qty_add": "जोड़ने की मात्रा",
        "alerts_title": "🔔 रीस्टॉक अलर्ट और खरीदारी सूची",
        "alerts_sub": "आज ध्यान देने वाली चीज़ें",
        "all_good": "✅ सभी स्टॉक अच्छे स्तर पर हैं!",
        "shopping_list": "🛒 आज की खरीदारी सूची",
        "copy_hint": "यह सूची कॉपी करें और सप्लायर को WhatsApp करें!",
        "no_sales": "अभी कोई बिक्री नहीं",
        "no_products": "कोई उत्पाद नहीं मिला।",
        "enter_name": "कृपया उत्पाद का नाम डालें।",
        "overview": "📊 स्टॉक अवलोकन",
        "navy_label": "🔵 नेवी = वर्तमान स्टॉक",
        "gold_label": "🟡 सोना = रीऑर्डर स्तर",
        "all_products": "📋 सभी उत्पाद",
    },
}

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
st.sidebar.markdown("🌐 **Language / ഭാഷ / भाषा**")
lang = st.sidebar.selectbox("lang", ["English", "Malayalam", "Hindi"],
                             label_visibility="collapsed")
L = LABELS[lang]

st.sidebar.markdown(f"**{L['navigate']}**")
page = st.sidebar.radio("nav", [L['dashboard'], L['enter_sales'], L['products'], L['alerts']],
                        label_visibility="collapsed")

products_df = get_products()
all_categories = [L['all_cat']] + sorted(products_df['category'].unique().tolist())
st.sidebar.markdown(f"**{L['filter_cat']}**")
selected_category = st.sidebar.selectbox("cat", all_categories, label_visibility="collapsed")

# ─── DASHBOARD ───────────────────────────────────────────────────────────────
if page == L['dashboard']:
    st.markdown(f"""
    <div style="padding: 20px 0px 10px 0px;">
        <h1 style="font-size: 52px; font-weight: 900; color: #1A3B5D; 
                   letter-spacing: -1px; margin-bottom: 4px;">
            🛒 ShelfSense
        </h1>
        <p style="font-size: 14px; color: #88BDA3; font-weight: 600; 
                  letter-spacing: 3px; text-transform: uppercase; margin: 0;">
            {L['subtitle']}
        </p>
        <div style="width: 60px; height: 4px; background: #D4AF37; 
                    border-radius: 2px; margin-top: 8px; margin-bottom: 8px;"></div>
        <p style="font-size: 13px; color: #888; margin: 0;">
            📅 {datetime.now().strftime('%A, %d %B %Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input(L['search'], "")

    filtered_df = products_df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search, case=False)]
    if selected_category != L['all_cat']:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    def priority(row):
        if row['current_stock'] <= row['reorder_level']:           return 0
        elif row['current_stock'] <= row['reorder_level'] * 1.5:  return 1
        else:                                                       return 2

    filtered_df = filtered_df.copy()
    filtered_df['priority'] = filtered_df.apply(priority, axis=1)
    filtered_df = filtered_df.sort_values('priority')

    total    = len(products_df)
    critical = len(products_df[products_df['current_stock'] <= products_df['reorder_level']])
    low      = len(products_df[(products_df['current_stock'] > products_df['reorder_level']) &
                                (products_df['current_stock'] <= products_df['reorder_level'] * 1.5)])

    c1, c2, c3 = st.columns(3)
    c1.metric(L['total'],    total)
    c2.metric(L['critical'], critical)
    c3.metric(L['low'],      low)

    if critical > 0:
        st.error(f"🔴 {critical} item(s) — {L['restock_now']}")

    st.divider()

    if filtered_df.empty:
        st.info(L['no_products'])
    else:
        for _, row in filtered_df.iterrows():
            avg_daily    = get_prediction(row['id'])
            trend        = get_trend(row['id'])
            days_of_data = get_days_of_data(row['id'])
            data_note    = f" *(based on {days_of_data} days)*" if days_of_data < 7 else ""

            if avg_daily == 0:
                days_left = L['no_sales']
            elif row['current_stock'] <= 0:
                days_left = "⚠️ 0"
            else:
                days_left = f"{round(row['current_stock'] / avg_daily, 1)} days"

            suggest_order = max(0, round(avg_daily * 30 - row['current_stock'], 1))

            if row['current_stock'] <= 0:
                status = L['out'];           bg = "#FFE5E5"; border = "#FF4444"
            elif row['current_stock'] <= row['reorder_level']:
                status = f"🔴 {L['restock_now']}"; bg = "#FFF0F0"; border = "#FF6B6B"
            elif row['current_stock'] <= row['reorder_level'] * 1.5:
                status = L['running_low'];   bg = "#FFFBEA"; border = "#D4AF37"
            else:
                status = L['good'];          bg = "#F0FFF4"; border = "#88BDA3"

            st.markdown(f"""
            <div style="background:{bg}; border-left:5px solid {border};
                        border-radius:8px; padding:12px 16px; margin-bottom:10px;">
                <b style="font-size:16px; color:#1A3B5D;">{row['name']}</b>
                <span style="float:right; color:#1A3B5D;">{status}</span><br>
                <span style="color:#1A3B5D;">
                📦 {L['stock']}: <b>{row['current_stock']} {row['unit']}</b> &nbsp;|&nbsp;
                📊 {L['avg_day']}: <b>{avg_daily}</b>{data_note} &nbsp;|&nbsp;
                ⏳ {L['days_left']}: <b>{days_left}</b> &nbsp;|&nbsp;
                🛒 {L['suggest']}: <b>{suggest_order} {row['unit']}</b>
                </span><br>
                <span style="color:#555;">{trend}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.subheader(L['overview'])
    if not filtered_df.empty:
        chart_df = filtered_df[['name','current_stock','reorder_level']].copy()
        chart_df = chart_df.rename(columns={
            'name':'Product','current_stock':'Current Stock','reorder_level':'Reorder Level'
        }).set_index('Product')
        st.markdown('<div style="background:#C8D8C0; border-radius:12px; padding:16px;">',
                    unsafe_allow_html=True)
        st.bar_chart(chart_df, color=["#1A3B5D","#D4AF37"], height=300)
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption(f"{L['navy_label']}  &nbsp;&nbsp;  {L['gold_label']}")

# ─── ENTER SALES ─────────────────────────────────────────────────────────────
elif page == L['enter_sales']:
    st.title(L['record_title'])
    st.caption(L['record_sub'])

    product_names = products_df['name'].tolist()
    selected = st.selectbox(L['select_prod'], product_names, key="sale_product")

    current_row = products_df[products_df['name'] == selected].iloc[0]
    current_stock = float(current_row['current_stock'])
    st.caption(f"📦 Current stock: **{current_stock} {current_row['unit']}**")

    quantity = st.number_input(L['qty_sold'], min_value=0.0, step=0.5, value=0.0, key="sale_qty")

    def do_record_sale():
        qty = st.session_state.sale_qty
        prod = st.session_state.sale_product
        row = products_df[products_df['name'] == prod].iloc[0]
        stk = float(row['current_stock'])
        if qty <= 0:
            st.session_state.sale_success = ("error", "⚠️ Please enter a quantity greater than 0.")
        elif qty > stk:
            st.session_state.sale_success = ("error", f"⚠️ Cannot sell {qty} — only {stk} {row['unit']} in stock!")
        else:
            pid = int(row['id'])
            add_sale(pid, qty)
            st.session_state.sale_success = ("ok", f"✅ Recorded {qty} units of {prod}!")

    st.button(L['record_btn'], on_click=do_record_sale, key="sale_btn")

    if st.session_state.sale_success:
        kind, msg = st.session_state.sale_success
        if kind == "ok":
            st.success(msg)
            st.session_state.sale_success = None
            products_df = get_products()  # refresh stock display
        else:
            st.error(msg)
            st.session_state.sale_success = None

# ─── PRODUCTS ────────────────────────────────────────────────────────────────
elif page == L['products']:
    st.title(L['prod_title'])

    tab1, tab2 = st.tabs([L['add_tab'], L['restock_tab']])

    with tab1:
        st.subheader(L['add_tab'])
        name     = st.text_input(L['prod_name'], key="add_name")
        category = st.selectbox(L['category'],
                                 ["Grains","Pulses","Oil","Essentials",
                                  "Beverages","Snacks","Personal Care",
                                  "Dairy","Vegetables","Other"], key="add_cat")
        unit     = st.selectbox(L['unit'],
                                 ["packets","bags","bottles","bars","kg",
                                  "litres","pieces","bundles","dozen"], key="add_unit")
        stock    = st.number_input(L['curr_stock'], min_value=0.0, step=1.0, key="add_stock")
        reorder  = st.number_input(L['reorder_lvl'], min_value=0.0, step=1.0, key="add_reorder")

        st.markdown("""
        <style>
        /* Fix button text visibility */
        .stButton > button {
            background-color: #1A3B5D !important;
            color: #ffffff !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            padding: 10px 24px !important;
            border-radius: 8px !important;
            width: 100% !important;
        }
        .stButton > button:hover {
            background-color: #D4AF37 !important;
            color: #1A3B5D !important;
        }
        </style>
        """, unsafe_allow_html=True)

        def do_add_product():
            n = st.session_state.add_name
            cat = st.session_state.add_cat
            u = st.session_state.add_unit
            stk = st.session_state.add_stock
            reord = st.session_state.add_reorder
            if n:
                add_product(n, cat, stk, u, reord)
                st.session_state.add_success = ("ok", f"✅ {n} added successfully!")
            else:
                st.session_state.add_success = ("error", L['enter_name'])

        if st.button("✅ Add Product", use_container_width=True, on_click=do_add_product, key="add_btn"):
            pass

        if st.session_state.add_success:
            kind, msg = st.session_state.add_success
            if kind == "ok":
                st.success(msg)
            else:
                st.error(msg)
            st.session_state.add_success = None

        st.divider()
        st.subheader(L['all_products'])
        display_df = products_df[['name','category','current_stock','unit','reorder_level']].copy()
        display_df.columns = ['Name','Category','Stock','Unit','Reorder Level']
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # DELETE PRODUCT
        st.divider()
        st.subheader("🗑️ Delete a Product")
        st.caption("Use this to remove incorrect or duplicate entries")
        
        product_to_delete = st.selectbox("Select product to delete", 
                                          products_df['name'].tolist(),
                                          key="delete_select")
        
        # Two step confirmation so owner doesn't accidentally delete
        confirm = st.checkbox(f"⚠️ Yes, I want to delete **{product_to_delete}**")
        
        
        def do_delete_product():
            prod = st.session_state.delete_select
            row = products_df[products_df['name'] == prod].iloc[0]
            pid = int(row['id'])
            delete_product(pid)
            st.session_state.delete_success = ("ok", f"✅ {prod} deleted!")

        if confirm:
            if st.button("🗑️ Delete Product", use_container_width=True, on_click=do_delete_product, key="delete_btn"):
                pass

        if st.session_state.delete_success:
            kind, msg = st.session_state.delete_success
            st.success(msg)
            st.session_state.delete_success = None
    with tab2:
        st.subheader(L['restock_tab'])
        selected  = st.selectbox(L['select_prod'], products_df['name'].tolist(), key="restock_product")
        restock_q = st.number_input(L['qty_add'], min_value=0.1, step=1.0, key="restock_qty")

        def do_restock():
            prod = st.session_state.restock_product
            qty = st.session_state.restock_qty
            pid = int(products_df[products_df['name'] == prod]['id'].values[0])
            restock_product(pid, qty)
            st.session_state.restock_success = ("ok", f"✅ Added {qty} units to {prod}!")

        st.button(L['restock_btn'], on_click=do_restock, key="restock_btn")

        if st.session_state.restock_success:
            kind, msg = st.session_state.restock_success
            st.success(msg)
            st.session_state.restock_success = None

# ─── ALERTS ──────────────────────────────────────────────────────────────────
elif page == L['alerts']:
    st.title(L['alerts_title'])
    st.caption(L['alerts_sub'])

    critical_items = []
    low_items      = []

    for _, row in products_df.iterrows():
        avg_daily     = get_prediction(row['id'])
        suggest_order = max(0, round(avg_daily * 30 - row['current_stock'], 1))
        if row['current_stock'] <= row['reorder_level']:
            critical_items.append((row['name'], row['current_stock'], row['unit'], avg_daily, suggest_order))
        elif row['current_stock'] <= row['reorder_level'] * 1.5:
            low_items.append((row['name'], row['current_stock'], row['unit'], avg_daily, suggest_order))

    if not critical_items and not low_items:
        st.success(L['all_good'])
    else:
        if critical_items:
            st.error(f"🔴 {len(critical_items)} item(s) need URGENT restocking!")
            for name, stock, unit, avg, order in critical_items:
                st.markdown(f"""
                <div style="background:#FFF0F0; border-left:5px solid #FF6B6B;
                            border-radius:8px; padding:12px; margin-bottom:8px;">
                    <b style="color:#1A3B5D;">🔴 {name}</b><br>
                    <span style="color:#1A3B5D;">
                    {L['stock']}: {stock} {unit} &nbsp;|&nbsp;
                    {L['avg_day']}: {avg} &nbsp;|&nbsp;
                    <b>{L['suggest']}: {order} {unit}</b>
                    </span>
                </div>""", unsafe_allow_html=True)

        if low_items:
            st.warning(f"🟡 {len(low_items)} item(s) running low")
            for name, stock, unit, avg, order in low_items:
                st.markdown(f"""
                <div style="background:#FFFBEA; border-left:5px solid #D4AF37;
                            border-radius:8px; padding:12px; margin-bottom:8px;">
                    <b style="color:#1A3B5D;">🟡 {name}</b><br>
                    <span style="color:#1A3B5D;">
                    {L['stock']}: {stock} {unit} &nbsp;|&nbsp;
                    {L['avg_day']}: {avg} &nbsp;|&nbsp;
                    <b>{L['suggest']}: {order} {unit}</b>
                    </span>
                </div>""", unsafe_allow_html=True)

        st.divider()
        st.subheader(L['shopping_list'])
        all_urgent = critical_items + low_items
        shopping   = "\n".join([f"• {n}: order ~{o} {u}" for n, _, u, _, o in all_urgent])
        st.markdown(f"""
        <div style="background-color: #ffffff; border: 2px solid #88BDA3; 
                    border-radius: 10px; padding: 16px 20px; 
                    font-family: monospace; font-size: 15px; color: #1A3B5D;
                    line-height: 1.8;">
            {shopping.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        st.caption(L['copy_hint'])
        
        # WhatsApp Share Button
        whatsapp_text = "🛒 *ShelfSense Restock Alert*\n\n"
        whatsapp_text += "*Items to order today:*\n"
        for n, _, u, _, o in all_urgent:
            whatsapp_text += f"• {n}: ~{o} {u}\n"
        whatsapp_text += "\n_Sent from ShelfSense 📦_"
        
        import urllib.parse
        encoded = urllib.parse.quote(whatsapp_text)
        whatsapp_url = f"https://wa.me/?text={encoded}"
        
        st.markdown(f"""
        <div style="margin-top: 20px;">
            <a href="{whatsapp_url}" target="_blank" style="
                background-color: #25D366;
                color: white !important;
                padding: 14px 28px;
                border-radius: 10px;
                text-decoration: none;
                font-size: 18px;
                font-weight: 700;
                display: inline-block;
                box-shadow: 0 4px 12px rgba(37,211,102,0.4);">
                📱 Send to Supplier on WhatsApp
            </a>
        </div>
        <p style="color: #888; font-size: 12px; margin-top: 10px;">
            Opens WhatsApp with restock list ready to send
        </p>
        """, unsafe_allow_html=True)