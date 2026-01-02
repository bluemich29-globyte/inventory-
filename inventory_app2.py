
# import streamlit as st
# import pandas as pd
# import altair as alt
# from datetime import date
# from databricks import sql

# # ============================================================
# # HARD-CODED DATABRICKS CONFIG (EDIT THESE 3 VALUES)
# # ============================================================
# DATABRICKS_SERVER_HOSTNAME = "dbc-092f61e4-3cd9.cloud.databricks.com"
# DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/343faa8c987d55bf"
# DATABRICKS_TOKEN = "dapi547b1a6593c11731c34ca3f4c1b63f26"
# # ============================================================

# INVENTORY_TABLE = "test.poc.inventory"
# SALES_TABLE = "test.poc.sales"

# st.set_page_config(page_title="Inventory & Sales", layout="wide")
# st.markdown(
#     """
#     <style>
#     /* ===== Brand Header ===== */
#     .brand-header {
#         display: flex;
#         align-items: center;
#         gap: 14px;
#         padding: 18px 24px;
#         background: linear-gradient(90deg, #3f2a1d, #5c3d2e);
#         border-radius: 14px;
#         margin-bottom: 24px;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.3);
#     }

#     .brand-logo {
#         font-size: 38px;
#     }

#     .brand-title {
#         font-size: 34px;
#         font-weight: 800;
#         color: #fef3c7;
#         letter-spacing: 1px;
#     }

#     .brand-subtitle {
#         font-size: 14px;
#         color: #fde68a;
#         margin-top: -6px;
#     }
#     </style>

#     <div class="brand-header">
#         <div class="brand-logo">🪵</div>
#         <div>
#             <div class="brand-title">EthioWoods</div>
#             <div class="brand-subtitle">Inventory & Sales Management</div>
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <style>
#     /* ===== Page background ===== */
#     .stApp {
#         background-color: #ff8d00; /* dark navy */
#         color: #e5e7eb;
#     }

#     /* ===== Titles ===== */
#     h1, h2, h3, h4 {
#         color: #38bdf8; /* cyan-blue */
#     }

#     /* ===== Sidebar ===== */
#     section[data-testid="stSidebar"] {
#         background-color: #020617;
#         border-right: 1px solid #1e293b;
#     }

#     /* ===== Tabs ===== */
#     button[data-baseweb="tab"] {
#         background-color: #020617;
#         color: #cbd5e1;
#         border-radius: 6px;
#         padding: 8px 14px;
#         margin-right: 6px;
#     }

#     button[data-baseweb="tab"][aria-selected="true"] {
#         background-color: #2563eb; /* blue */
#         color: white;
#         font-weight: 600;
#     }

#     /* ===== DataFrame header ===== */
#     thead tr th {
#         background-color: #1e293b !important;
#         color: #f8fafc !important;
#         font-weight: 600;
#         text-align: left;
#     }

#     /* ===== DataFrame rows ===== */
#     tbody tr:nth-child(even) {
#         background-color: #020617;
#     }

#     tbody tr:nth-child(odd) {
#         background-color: #020617;
#     }

#     tbody tr:hover {
#         background-color: #1e293b !important;
#     }

#     /* ===== Metric cards ===== */
#     div[data-testid="metric-container"] {
#         background-color: #020617;
#         border: 1px solid #1e293b;
#         border-radius: 10px;
#         padding: 12px;
#     }

#     /* ===== Buttons ===== */
#     button[kind="primary"] {
#         background-color: #2563eb !important;
#         color: white !important;
#         border-radius: 8px;
#     }

#     button[kind="secondary"] {
#         border-radius: 8px;
#     }

#     /* ===== Inputs ===== */
#     input, textarea {
#         background-color: #020617 !important;
#         color: #f8fafc !important;
#         border: 1px solid #1e293b !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.title("Inventory Tracking + Sales")

# @st.cache_resource
# def get_connection():
#     return sql.connect(
#         server_hostname=DATABRICKS_SERVER_HOSTNAME,
#         http_path=DATABRICKS_HTTP_PATH,
#         access_token=DATABRICKS_TOKEN,
#     )

# def fetch_df(conn, query: str, params=None) -> pd.DataFrame:
#     with conn.cursor() as cur:
#         cur.execute(query, params or [])
#         rows = cur.fetchall()
#         cols = [c[0] for c in cur.description] if cur.description else []
#     return pd.DataFrame(rows, columns=cols)

# def exec_sql(conn, query: str, params=None) -> None:
#     with conn.cursor() as cur:
#         cur.execute(query, params or [])

# def safe_int(x, default=0):
#     try:
#         return int(x)
#     except Exception:
#         return default

# def safe_float(x, default=0.0):
#     try:
#         return float(x)
#     except Exception:
#         return default

# conn = get_connection()

# # ------------------------------------------------------------
# # Sidebar: global search
# # ------------------------------------------------------------
# with st.sidebar:
#     st.header("Search")
#     search_text = st.text_input("Search product name", value="", placeholder="e.g., coke, chips...")
#     st.caption("Search applies to Inventory and Sales views.")

# # ------------------------------------------------------------
# # Tabs
# # ------------------------------------------------------------
# tab_inv, tab_add, tab_sales = st.tabs(["View Inventory", "Add Product", "View Sales"])

# # ------------------------------------------------------------
# # TAB 1: View Inventory
# # ------------------------------------------------------------
# with tab_inv:
#     st.subheader("Current Inventory")

#     c1, c2, c3 = st.columns([2, 1, 1])
#     with c1:
#         low_stock_only = st.checkbox("Low stock only (<= 5)", value=False)
#     with c2:
#         if st.button("Refresh inventory", use_container_width=True):
#             st.rerun()
#     with c3:
#         st.write("")

#     where = []
#     params = []

#     if search_text.strip():
#         where.append("LOWER(name) LIKE ?")
#         params.append(f"%{search_text.strip().lower()}%")

#     if low_stock_only:
#         where.append("quantity <= 5")

#     where_sql = f"WHERE {' AND '.join(where)}" if where else ""

#     inv_q = f"""
#         SELECT id, name, description, quantity, price
#         FROM {INVENTORY_TABLE}
#         {where_sql}
#         ORDER BY name
#     """
#     inv_df = fetch_df(conn, inv_q, params)

#     # st.dataframe(inv_df, use_container_width=True)
#     def highlight_low_stock(row):
#         if row["quantity"] <= 5:
#             return ["background-color: #7f1d1d"] * len(row)  # red
#         return [""] * len(row)

#     st.dataframe(
#         inv_df.style.apply(highlight_low_stock, axis=1),
#         use_container_width=True
#     )


#     # KPIs
#     if inv_df.empty:
#         k1, k2, k3 = st.columns(3)
#         k1.metric("Products", "0")
#         k2.metric("Total Units", "0")
#         k3.metric("Inventory Value", "0.00")
#     else:
#         qty = pd.to_numeric(inv_df["quantity"], errors="coerce").fillna(0)
#         price = pd.to_numeric(inv_df["price"], errors="coerce").fillna(0)
#         inventory_value = float((qty * price).sum())

#         k1, k2, k3 = st.columns(3)
#         k1.metric("Products", f"{len(inv_df):,}")
#         k2.metric("Total Units", f"{int(qty.sum()):,}")
#         k3.metric("Inventory Value", f"{inventory_value:,.2f}")

# # ------------------------------------------------------------
# # TAB 2: Add Product
# # ------------------------------------------------------------
# with tab_add:
#     st.subheader("Add a Product")

#     with st.form("add_product_form", clear_on_submit=True):
#         name = st.text_input("Name", value="")
#         description = st.text_area("Description", value="", height=80)
#         c1, c2 = st.columns(2)
#         with c1:
#             quantity = st.number_input("Quantity", min_value=0, step=1, value=0)
#         with c2:
#             price = st.number_input("Price", min_value=0.0, step=0.5, value=0.0)

#         submitted = st.form_submit_button("Add Product", use_container_width=True)

#     if submitted:
#         if not name.strip():
#             st.error("Name is required.")
#         else:
#             try:
#                 # Insert with generated id if the table supports it; otherwise use a MAX(id)+1 fallback.
#                 # Community Edition tables sometimes have id as INT; we will compute next id safely.
#                 id_df = fetch_df(conn, f"SELECT COALESCE(MAX(id), 0) AS max_id FROM {INVENTORY_TABLE}")
#                 next_id = safe_int(id_df.loc[0, "max_id"], 0) + 1

#                 ins_q = f"""
#                     INSERT INTO {INVENTORY_TABLE} (id, name, description, quantity, price)
#                     VALUES (?, ?, ?, ?, ?)
#                 """
#                 exec_sql(conn, ins_q, [next_id, name.strip(), description.strip(), int(quantity), float(price)])

#                 st.success(f"Product added (id={next_id}).")
#             except Exception as e:
#                 st.error(f"Failed to add product: {e}")

# # ------------------------------------------------------------
# # TAB 3: View Sales
# # ------------------------------------------------------------
# with tab_sales:
#     st.subheader("Sales of Products")

#     c1, c2 = st.columns([2, 1])
#     with c1:
#         # Optional date filter (works if sale_date is DATE/TIMESTAMP)
#         start_d = st.date_input("Start date", value=date.today().replace(day=1))
#     with c2:
#         end_d = st.date_input("End date", value=date.today())

#     # Sales query with join to inventory for product name/description
#     # Also supports name search via inventory.name (your requirement: product search)
#     where = ["CAST(s.sale_date AS DATE) BETWEEN ? AND ?"]
#     params = [start_d, end_d]

#     if search_text.strip():
#         where.append("LOWER(i.name) LIKE ?")
#         params.append(f"%{search_text.strip().lower()}%")

#     where_sql = f"WHERE {' AND '.join(where)}"

#     sales_q = f"""
#         SELECT
#             s.id              AS sale_id,
#             s.product_id      AS product_id,
#             i.name            AS product_name,
#             s.quantity        AS quantity_sold,
#             s.sale_price      AS sale_price,
#             s.sale_date       AS sale_date,
#             (CAST(s.quantity AS DOUBLE) * CAST(s.sale_price AS DOUBLE)) AS revenue
#         FROM {SALES_TABLE} s
#         LEFT JOIN {INVENTORY_TABLE} i
#           ON s.product_id = i.id
#         {where_sql}
#         ORDER BY s.sale_date DESC
#     """
#     sales_df = fetch_df(conn, sales_q, params)

#     st.dataframe(sales_df, use_container_width=True)

#     if sales_df.empty:
#         k1, k2, k3 = st.columns(3)
#         k1.metric("Transactions", "0")
#         k2.metric("Units Sold", "0")
#         k3.metric("Revenue", "0.00")
#     else:
#         qty = pd.to_numeric(sales_df["quantity_sold"], errors="coerce").fillna(0)
#         rev = pd.to_numeric(sales_df["revenue"], errors="coerce").fillna(0)

#         k1, k2, k3 = st.columns(3)
#         k1.metric("Transactions", f"{len(sales_df):,}")
#         k2.metric("Units Sold", f"{int(qty.sum()):,}")
#         k3.metric("Revenue", f"{float(rev.sum()):,.2f}")

#         st.divider()
#         st.subheader("Daily Revenue Trend")

#         # Normalize sale_date for charting
#         tmp = sales_df.copy()
#         tmp["sale_day"] = pd.to_datetime(tmp["sale_date"], errors="coerce").dt.date
#         daily = tmp.groupby("sale_day", dropna=True)["revenue"].sum().reset_index()

#         if not daily.empty:
#             chart = (
#                 alt.Chart(daily)
#                 .mark_line(point=True)
#                 .encode(
#                     x="sale_day:T",
#                     y="revenue:Q",
#                     tooltip=["sale_day:T", "revenue:Q"],
#                 )
#                 .properties(height=280)
#             )
#             st.altair_chart(chart, use_container_width=True)

#         st.subheader("Top Products by Revenue")
#         top = (
#             tmp.groupby("product_name", dropna=True)["revenue"]
#             .sum()
#             .reset_index()
#             .sort_values("revenue", ascending=False)
#             .head(10)
#         )
#         st.dataframe(top, use_container_width=True)

import streamlit as st
import pandas as pd
import altair as alt
from datetime import date
from databricks import sql

# --- Live barcode scanning deps ---
import cv2
import numpy as np
import json
import time
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from pyzbar.pyzbar import decode

# ============================================================
# HARD-CODED DATABRICKS CONFIG (EDIT THESE 3 VALUES)
# ============================================================
DATABRICKS_SERVER_HOSTNAME = "dbc-092f61e4-3cd9.cloud.databricks.com"
DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/343faa8c987d55bf"
DATABRICKS_TOKEN = "dapi547b1a6593c11731c34ca3f4c1b63f26"
# ============================================================

INVENTORY_TABLE = "test.poc.inventory"
SALES_TABLE = "test.poc.sales"

st.set_page_config(page_title="Inventory & Sales", layout="wide")

# -----------------------------
# Branding Header (EthioWoods)
# -----------------------------
st.markdown(
    """
    <style>
    .brand-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 18px 24px;
        background: linear-gradient(90deg, #3f2a1d, #5c3d2e);
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .brand-logo { font-size: 38px; }
    .brand-title {
        font-size: 34px;
        font-weight: 800;
        color: #fef3c7;
        letter-spacing: 1px;
    }
    .brand-subtitle {
        font-size: 14px;
        color: #fde68a;
        margin-top: -6px;
    }
    </style>

    <div class="brand-header">
        <div class="brand-logo">🪵</div>
        <div>
            <div class="brand-title">EthioWoods</div>
            <div class="brand-subtitle">Inventory & Sales Management</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Theme / Colors
# -----------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #ff8d00; color: #e5e7eb; }
    h1, h2, h3, h4 { color: #38bdf8; }

    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }

    button[data-baseweb="tab"] {
        background-color: #020617;
        color: #cbd5e1;
        border-radius: 6px;
        padding: 8px 14px;
        margin-right: 6px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
    }

    thead tr th {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        font-weight: 600;
        text-align: left;
    }

    tbody tr:nth-child(even) { background-color: #020617; }
    tbody tr:nth-child(odd)  { background-color: #020617; }
    tbody tr:hover { background-color: #1e293b !important; }

    div[data-testid="metric-container"] {
        background-color: #020617;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 12px;
    }

    button[kind="primary"] {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 8px;
    }

    input, textarea {
        background-color: #020617 !important;
        color: #f8fafc !important;
        border: 1px solid #1e293b !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Inventory Tracking + Sales")

# ============================================================
# Databricks connection helpers
# ============================================================
@st.cache_resource
def get_connection():
    return sql.connect(
        server_hostname=DATABRICKS_SERVER_HOSTNAME,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN,
    )

def fetch_df(conn, query: str, params=None) -> pd.DataFrame:
    with conn.cursor() as cur:
        cur.execute(query, params or [])
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description] if cur.description else []
    return pd.DataFrame(rows, columns=cols)

def exec_sql(conn, query: str, params=None) -> None:
    with conn.cursor() as cur:
        cur.execute(query, params or [])

def safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default

def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

conn = get_connection()

# ============================================================
# Inventory helpers
# ============================================================
def get_inventory_row(conn, product_id: int) -> pd.DataFrame:
    return fetch_df(
        conn,
        f"SELECT id, name, description, quantity, price FROM {INVENTORY_TABLE} WHERE id = ? LIMIT 1",
        [int(product_id)]
    )

def upsert_inventory(conn, product_id: int, name: str, description: str, quantity: int, price: float):
    exists = fetch_df(conn, f"SELECT 1 AS x FROM {INVENTORY_TABLE} WHERE id = ? LIMIT 1", [int(product_id)])
    if exists.empty:
        exec_sql(
            conn,
            f"""
            INSERT INTO {INVENTORY_TABLE} (id, name, description, quantity, price)
            VALUES (?, ?, ?, ?, ?)
            """,
            [int(product_id), name, description, int(quantity), float(price)]
        )
    else:
        exec_sql(
            conn,
            f"""
            UPDATE {INVENTORY_TABLE}
            SET name = ?, description = ?, quantity = ?, price = ?
            WHERE id = ?
            """,
            [name, description, int(quantity), float(price), int(product_id)]
        )

def parse_barcode_payload(barcode_text: str) -> dict:
    """
    Accept barcode formats:
    - "123" (plain product ID)
    - "id=123"
    - JSON: {"id":123,"name":"...","price":12.3,"description":"..."}
    - Colon format: "13: Wood Plank : Oak wood plank 2x4 : 10 Price: 25.50"
    Returns dict: {id, name, description, price}
    """
    out = {"id": None, "name": "", "description": "", "price": None}
    if not barcode_text:
        return out

    # JSON
    try:
        obj = json.loads(barcode_text)
        if isinstance(obj, dict) and "id" in obj:
            out["id"] = int(obj.get("id"))
            out["name"] = str(obj.get("name", "") or "")
            out["description"] = str(obj.get("description", "") or "")
            if obj.get("price") is not None:
                out["price"] = float(obj.get("price"))
            return out
    except Exception:
        pass

    # Colon-separated format: "ID: Name : Description : Qty Price: XX.XX"
    # Example: "13: Wood Plank : Oak wood plank 2x4 : 10 Price: 25.50"
    if ":" in barcode_text and "price:" in barcode_text.lower():
        try:
            parts = barcode_text.split(":")
            if len(parts) >= 4:
                # Extract ID (first part before first colon)
                out["id"] = int(parts[0].strip())

                # Extract name (second part)
                out["name"] = parts[1].strip()

                # Extract description and price from remaining parts
                # Join all parts after name, then split by "Price:"
                rest = ":".join(parts[2:])
                if "price:" in rest.lower():
                    desc_price = rest.lower().split("price:")
                    # Description is everything before "Price:"
                    desc_parts = rest[:rest.lower().find("price:")].strip().split(":")
                    out["description"] = desc_parts[0].strip()

                    # Price is after "Price:"
                    price_str = rest[rest.lower().find("price:") + 6:].strip()
                    out["price"] = float(price_str)

                return out
        except Exception:
            pass

    # id=123
    low = barcode_text.strip().lower()
    if "id=" in low:
        try:
            out["id"] = int(low.split("id=")[1].split("&")[0].strip())
            return out
        except Exception:
            pass

    # plain int (most common for barcodes)
    try:
        out["id"] = int(barcode_text.strip())
    except Exception:
        out["id"] = None

    return out

# ============================================================
# Live barcode scanner state + transformer
# ============================================================
if "pending_barcode" not in st.session_state:
    st.session_state.pending_barcode = None
if "pending_barcode_ts" not in st.session_state:
    st.session_state.pending_barcode_ts = 0.0
if "barcode_candidate" not in st.session_state:
    st.session_state.barcode_candidate = None
if "barcode_hits" not in st.session_state:
    st.session_state.barcode_hits = 0
if "last_barcode_value" not in st.session_state:
    st.session_state.last_barcode_value = None
if "last_barcode_ts" not in st.session_state:
    st.session_state.last_barcode_ts = 0.0

class BarcodeVideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.last_detection_time = 0

    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        # Add status text on video feed
        height, width = img.shape[:2]

        # Add scanning indicator
        cv2.putText(img, "SCANNING FOR BARCODES...", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Decode barcodes using pyzbar
        barcodes = decode(img)

        if len(barcodes) == 0:
            # No barcode detected - add helpful message
            cv2.putText(img, "No barcode detected", (10, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        else:
            # Process detected barcodes
            for barcode in barcodes:
                # Extract barcode data
                try:
                    barcode_data = barcode.data.decode('utf-8').strip()
                except:
                    barcode_data = str(barcode.data)

                # Draw filled rectangle background for better visibility
                x, y, w, h = barcode.rect
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

                # Draw barcode polygon outline
                points = barcode.polygon
                if len(points) == 4:
                    pts = [(point.x, point.y) for point in points]
                    pts = [(int(px), int(py)) for px, py in pts]
                    cv2.polylines(img, [np.array(pts)], True, (255, 0, 255), 2)

                # Draw barcode type and data with background
                barcode_type = barcode.type
                text = f"{barcode_type}: {barcode_data}"

                # Add background rectangle for text
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                cv2.rectangle(img, (x, y - 35), (x + text_size[0] + 10, y - 5), (0, 0, 0), -1)
                cv2.putText(img, text, (x + 5, y - 15),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Add detection confirmation
                cv2.putText(img, "BARCODE DETECTED!", (10, height - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                # Only set pending_barcode if something is decoded
                if barcode_data:
                    st.session_state.pending_barcode = barcode_data
                    st.session_state.pending_barcode_ts = time.time()
                    self.last_detection_time = time.time()
                    break  # Only process first barcode

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# ------------------------------------------------------------
# Sidebar: global search
# ------------------------------------------------------------
with st.sidebar:
    st.header("Search")
    search_text = st.text_input("Search product name", value="", placeholder="e.g., coke, chips...")
    st.caption("Search applies to Inventory and Sales views.")

# ------------------------------------------------------------
# Tabs
# ------------------------------------------------------------
tab_inv, tab_add, tab_sales, tab_scan_usb = st.tabs(
    ["View Inventory", "Add Product", "View Sales", "Scan Barcode (USB Scanner)"]
)

# ------------------------------------------------------------
# TAB 1: View Inventory
# ------------------------------------------------------------
with tab_inv:
    st.subheader("Current Inventory")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        low_stock_only = st.checkbox("Low stock only (<= 5)", value=False)
    with c2:
        if st.button("Refresh inventory", use_container_width=True):
            st.rerun()
    with c3:
        st.write("")

    where = []
    params = []

    if search_text.strip():
        where.append("LOWER(name) LIKE ?")
        params.append(f"%{search_text.strip().lower()}%")

    if low_stock_only:
        where.append("quantity <= 5")

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    inv_q = f"""
        SELECT id, name, description, quantity, price
        FROM {INVENTORY_TABLE}
        {where_sql}
        ORDER BY name
    """
    inv_df = fetch_df(conn, inv_q, params)

    def highlight_low_stock(row):
        if safe_int(row.get("quantity", 0), 0) <= 5:
            return ["background-color: #7f1d1d"] * len(row)
        return [""] * len(row)

    st.dataframe(inv_df.style.apply(highlight_low_stock, axis=1), use_container_width=True)

    if inv_df.empty:
        k1, k2, k3 = st.columns(3)
        k1.metric("Products", "0")
        k2.metric("Total Units", "0")
        k3.metric("Inventory Value", "0.00")
    else:
        qty = pd.to_numeric(inv_df["quantity"], errors="coerce").fillna(0)
        price = pd.to_numeric(inv_df["price"], errors="coerce").fillna(0)
        inventory_value = float((qty * price).sum())

        k1, k2, k3 = st.columns(3)
        k1.metric("Products", f"{len(inv_df):,}")
        k2.metric("Total Units", f"{int(qty.sum()):,}")
        k3.metric("Inventory Value", f"{inventory_value:,.2f}")

# ------------------------------------------------------------
# TAB 2: Add Product
# ------------------------------------------------------------
with tab_add:
    st.subheader("Add a Product")

    with st.form("add_product_form", clear_on_submit=True):
        name = st.text_input("Name", value="")
        description = st.text_area("Description", value="", height=80)
        c1, c2 = st.columns(2)
        with c1:
            quantity = st.number_input("Quantity", min_value=0, step=1, value=0)
        with c2:
            price = st.number_input("Price", min_value=0.0, step=0.5, value=0.0)

        submitted = st.form_submit_button("Add Product", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Name is required.")
        else:
            try:
                id_df = fetch_df(conn, f"SELECT COALESCE(MAX(id), 0) AS max_id FROM {INVENTORY_TABLE}")
                next_id = safe_int(id_df.loc[0, "max_id"], 0) + 1

                exec_sql(
                    conn,
                    f"INSERT INTO {INVENTORY_TABLE} (id, name, description, quantity, price) VALUES (?, ?, ?, ?, ?)",
                    [next_id, name.strip(), description.strip(), int(quantity), float(price)]
                )
                st.success(f"Product added (id={next_id}).")
            except Exception as e:
                st.error(f"Failed to add product: {e}")

# ------------------------------------------------------------
# TAB 3: View Sales
# ------------------------------------------------------------
with tab_sales:
    st.subheader("Sales of Products")

    c1, c2 = st.columns([2, 1])
    with c1:
        start_d = st.date_input("Start date", value=date.today().replace(day=1))
    with c2:
        end_d = st.date_input("End date", value=date.today())

    where = ["CAST(s.sale_date AS DATE) BETWEEN ? AND ?"]
    params = [start_d, end_d]

    if search_text.strip():
        where.append("LOWER(i.name) LIKE ?")
        params.append(f"%{search_text.strip().lower()}%")

    where_sql = f"WHERE {' AND '.join(where)}"

    sales_q = f"""
        SELECT
            s.id              AS sale_id,
            s.product_id      AS product_id,
            i.name            AS product_name,
            s.quantity        AS quantity_sold,
            s.sale_price      AS sale_price,
            s.sale_date       AS sale_date,
            (CAST(s.quantity AS DOUBLE) * CAST(s.sale_price AS DOUBLE)) AS revenue
        FROM {SALES_TABLE} s
        LEFT JOIN {INVENTORY_TABLE} i
          ON s.product_id = i.id
        {where_sql}
        ORDER BY s.sale_date DESC
    """
    sales_df = fetch_df(conn, sales_q, params)

    st.dataframe(sales_df, use_container_width=True)

    if sales_df.empty:
        k1, k2, k3 = st.columns(3)
        k1.metric("Transactions", "0")
        k2.metric("Units Sold", "0")
        k3.metric("Revenue", "0.00")
    else:
        qty = pd.to_numeric(sales_df["quantity_sold"], errors="coerce").fillna(0)
        rev = pd.to_numeric(sales_df["revenue"], errors="coerce").fillna(0)

        k1, k2, k3 = st.columns(3)
        k1.metric("Transactions", f"{len(sales_df):,}")
        k2.metric("Units Sold", f"{int(qty.sum()):,}")
        k3.metric("Revenue", f"{float(rev.sum()):,.2f}")

        st.divider()
        st.subheader("Daily Revenue Trend")

        tmp = sales_df.copy()
        tmp["sale_day"] = pd.to_datetime(tmp["sale_date"], errors="coerce").dt.date
        daily = tmp.groupby("sale_day", dropna=True)["revenue"].sum().reset_index()

        if not daily.empty:
            chart = (
                alt.Chart(daily)
                .mark_line(point=True)
                .encode(
                    x="sale_day:T",
                    y="revenue:Q",
                    tooltip=["sale_day:T", "revenue:Q"],
                )
                .properties(height=280)
            )
            st.altair_chart(chart, use_container_width=True)

        st.subheader("Top Products by Revenue")
        top = (
            tmp.groupby("product_name", dropna=True)["revenue"]
            .sum()
            .reset_index()
            .sort_values("revenue", ascending=False)
            .head(10)
        )
        st.dataframe(top, use_container_width=True)

# ------------------------------------------------------------
# TAB 4: Scan Barcode (USB Scanner)
# ------------------------------------------------------------
with tab_scan_usb:
    st.subheader("🔍 Scan Barcode (USB Scanner) → Auto Update Inventory")

    st.info(
        "📌 **How to use:** Click in the barcode input field below, then scan with your USB barcode scanner. "
        "The scanner will automatically enter the barcode and trigger the update."
    )

    # Mode selection: Scanner or Manual Entry
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        use_manual_mode = st.toggle("📝 Manual Entry Mode", value=False, help="Switch to manual entry if scanner isn't working")
    with c2:
        auto_save = st.toggle("Auto-save", value=True, help="Automatically add scanned items to inventory")
    with c3:
        add_qty = st.number_input("Qty per scan", min_value=1, step=1, value=1)

    st.divider()

    # Manual Entry Mode
    if use_manual_mode:
        st.info("📝 **Manual Entry Mode Active** - Enter product details below without scanning")

        with st.form("manual_product_entry_form", clear_on_submit=True):
            st.subheader("Enter Product Information")

            manual_id = st.number_input("Product ID", min_value=1, step=1, value=1, help="Enter the product barcode ID")
            manual_name = st.text_input("Product Name", value="", placeholder="e.g., Oak Wood Plank")
            manual_description = st.text_area("Description", value="", placeholder="e.g., Premium oak wood plank 2x4", height=80)

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                manual_quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
            with col_m2:
                manual_price = st.number_input("Price ($)", min_value=0.0, step=0.5, value=0.0, format="%.2f")

            manual_submit = st.form_submit_button("Add Product to Inventory", use_container_width=True, type="primary")

            if manual_submit:
                if not manual_name.strip():
                    st.error("❌ Product name is required!")
                elif manual_price <= 0:
                    st.error("❌ Price must be greater than 0!")
                else:
                    # Check if product already exists
                    existing = exec_sql(
                        conn,
                        f"SELECT id, name, quantity FROM {INVENTORY_TABLE} WHERE id = ?",
                        [int(manual_id)]
                    )

                    if existing and len(existing) > 0:
                        # Product exists - update quantity
                        old_qty = existing[0][2]
                        new_qty = old_qty + manual_quantity
                        exec_sql(
                            conn,
                            f"UPDATE {INVENTORY_TABLE} SET quantity = ? WHERE id = ?",
                            [new_qty, int(manual_id)]
                        )
                        st.success(f"✅ **Updated existing product!** ID: {manual_id}, Name: {existing[0][1]}, Old Qty: {old_qty} → New Qty: {new_qty}")
                    else:
                        # Product doesn't exist - create new
                        exec_sql(
                            conn,
                            f"INSERT INTO {INVENTORY_TABLE} (id, name, description, quantity, price) VALUES (?, ?, ?, ?, ?)",
                            [int(manual_id), manual_name.strip(), manual_description.strip(), manual_quantity, float(manual_price)]
                        )
                        st.success(f"✅ **Product added!** ID: {manual_id}, Name: {manual_name}, Qty: {manual_quantity}, Price: ${manual_price:.2f}")

                    st.balloons()

    else:
        # Scanner Mode
        # Initialize session state for USB scanner
        if "last_scanned_barcode" not in st.session_state:
            st.session_state.last_scanned_barcode = ""
        if "scan_history" not in st.session_state:
            st.session_state.scan_history = []
        if "usb_cooldown_ts" not in st.session_state:
            st.session_state.usb_cooldown_ts = 0.0

        # Barcode input field - USB scanners work like keyboard input
        barcode_input = st.text_input(
            "Scan Barcode Here",
            value="",
            placeholder="Click here and scan with your USB scanner...",
            key="barcode_scanner_input",
            help="Focus this field and use your USB barcode scanner. It will auto-submit when scanned."
        )

        st.caption("💡 **Tip:** Most USB scanners automatically press Enter after scanning, triggering the update instantly.")

        st.divider()

        # Process the barcode if entered
        if barcode_input and barcode_input.strip():
            barcode_text = barcode_input.strip()

            # Update last scanned to prevent re-processing
            st.session_state.last_scanned_barcode = barcode_text

            # Add to scan history
            now = time.time()
            st.session_state.scan_history.insert(0, {
                "barcode": barcode_text,
                "timestamp": now
            })
            # Keep only last 10 scans
            st.session_state.scan_history = st.session_state.scan_history[:10]

            st.success(f"✅ Scanned: **{barcode_text}**")

            # Parse the barcode
            parsed = parse_barcode_payload(barcode_text)

            if parsed["id"] is None:
                st.error("❌ Barcode does not contain a valid numeric product ID.")
                st.info("💡 Make sure the barcode contains a product ID number.")
            else:
                product_id = int(parsed["id"])

                # Show what was scanned
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Product ID", product_id)

                # Get existing inventory data
                existing = get_inventory_row(conn, product_id)
                if not existing.empty:
                    row = existing.iloc[0].to_dict()
                    current_qty = safe_int(row.get("quantity", 0), 0)
                    name = parsed["name"] or str(row.get("name", "") or "")
                    description = parsed["description"] or str(row.get("description", "") or "")
                    price = float(parsed["price"]) if parsed["price"] is not None else safe_float(row.get("price", 0.0), 0.0)

                    with col2:
                        st.metric("Product Name", name)
                    with col3:
                        st.metric("Current Qty", current_qty)
                else:
                    current_qty = 0
                    name = parsed["name"] or ""
                    description = parsed["description"] or ""
                    price = float(parsed["price"]) if parsed["price"] is not None else 0.0

                    with col2:
                        st.metric("Product Name", name if name else "Not in system")
                    with col3:
                        st.metric("Current Qty", "0 (New)")

                # Check if we can save OR automatically add new product
                if not name.strip():
                    # Product doesn't exist - check if barcode has full info
                    if parsed["name"] and parsed["price"] is not None:
                        # Barcode contains full product info - auto-add!
                        st.info(f"🆕 **New product detected in barcode!** Auto-adding to inventory...")

                        try:
                            # Add the new product automatically
                            exec_sql(
                                conn,
                                f"INSERT INTO {INVENTORY_TABLE} (id, name, description, quantity, price) VALUES (?, ?, ?, ?, ?)",
                                [product_id, parsed["name"], parsed["description"], int(add_qty), float(parsed["price"])]
                            )
                            st.success(f"✅ **Product auto-added!** ID: {product_id}, Name: {parsed['name']}, Qty: {add_qty}, Price: ${parsed['price']}")
                            st.info("🔄 Scan again to add more quantity to this product")

                            # Show what was added
                            with st.expander("📊 View Added Product", expanded=True):
                                st.dataframe(get_inventory_row(conn, product_id), use_container_width=True)

                        except Exception as e:
                            st.error(f"❌ Failed to auto-add product: {e}")
                    else:
                        # Barcode only has ID - show manual form
                        st.warning(
                            "⚠️ **Product ID {0} not found in inventory.**".format(product_id)
                        )
                        st.info("💡 **Tip:** Use a JSON barcode to auto-add products, or fill in the form below:")

                        # Show form to add new product on the fly
                        with st.form(f"quick_add_product_{product_id}", clear_on_submit=False):
                            st.subheader("➕ Add New Product Manually")
                            st.caption("Fill in the details to add this product to inventory:")

                            new_name = st.text_input("Product Name", value="", placeholder="e.g., Wood Plank")
                            new_description = st.text_area("Description", value="", placeholder="e.g., Oak wood plank 2x4", height=80)

                            col_a, col_b = st.columns(2)
                            with col_a:
                                new_quantity = st.number_input("Initial Quantity", min_value=0, step=1, value=int(add_qty))
                            with col_b:
                                new_price = st.number_input("Price", min_value=0.0, step=0.5, value=0.0)

                            submitted = st.form_submit_button("Add Product to Inventory", use_container_width=True)

                        if submitted:
                            if not new_name.strip():
                                st.error("❌ Product name is required!")
                            else:
                                try:
                                    # Add the new product with the scanned ID
                                    exec_sql(
                                        conn,
                                        f"INSERT INTO {INVENTORY_TABLE} (id, name, description, quantity, price) VALUES (?, ?, ?, ?, ?)",
                                        [product_id, new_name.strip(), new_description.strip(), int(new_quantity), float(new_price)]
                                    )
                                    st.success(f"✅ **Product added successfully!** ID: {product_id}, Name: {new_name}, Qty: {new_quantity}")
                                    st.info("🔄 Refresh the page or scan again to update inventory")
                                except Exception as e:
                                    st.error(f"❌ Failed to add product: {e}")
                else:
                    # Auto-save if enabled
                    if auto_save:
                        # Cooldown check (3 second cooldown)
                        can_write = True
                        if (now - st.session_state.usb_cooldown_ts) < 3.0:
                            can_write = False
                            time_left = 3.0 - (now - st.session_state.usb_cooldown_ts)
                            st.caption(f"⏳ Cooldown active... {time_left:.1f}s remaining")

                        if can_write:
                            try:
                                new_qty = int(current_qty) + int(add_qty)
                                upsert_inventory(
                                    conn=conn,
                                    product_id=product_id,
                                    name=name.strip(),
                                    description=description.strip(),
                                    quantity=new_qty,
                                    price=float(price),
                                )
                                st.session_state.usb_cooldown_ts = now
                                st.success(f"✅ **Auto-saved!** Product {product_id} quantity updated: {current_qty} → **{new_qty}**")

                                # Show updated record
                                with st.expander("📊 View Updated Inventory Record", expanded=True):
                                    st.dataframe(get_inventory_row(conn, product_id), use_container_width=True)
                            except Exception as e:
                                st.error(f"❌ Auto-save failed: {e}")
                    else:
                        st.info(
                            f"ℹ️ **Auto-save is OFF.** Would add {add_qty} unit(s) to product {product_id}. "
                            f"New quantity would be: {int(current_qty) + int(add_qty)}"
                        )

                        # Show current record
                        with st.expander("📊 Current Inventory Record", expanded=False):
                            if not existing.empty:
                                st.dataframe(existing, use_container_width=True)
                            else:
                                st.info("Product not yet in inventory")

    # Show scan history
    if st.session_state.scan_history:
        st.divider()
        st.subheader("📜 Recent Scans")
        history_df = pd.DataFrame(st.session_state.scan_history)
        history_df["timestamp"] = pd.to_datetime(history_df["timestamp"], unit="s").dt.strftime("%H:%M:%S")
        st.dataframe(history_df, use_container_width=True, hide_index=True)

