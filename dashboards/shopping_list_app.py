import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Shopping List App",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark mode and bright colors
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #fafafa;
        border: 2px solid #00ff88;
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00ffff;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    .stButton > button {
        background-color: #ff6b6b;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #ff5252;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
    }
    
    .item-tag {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b, #ff8e53);
        color: white;
        padding: 8px 15px;
        margin: 5px;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        position: relative;
        animation: fadeIn 0.3s ease-in;
    }
    
    .item-tag .remove-btn {
        background: rgba(255,255,255,0.2);
        border: none;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        margin-left: 8px;
        cursor: pointer;
        font-size: 12px;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    
    .item-tag .remove-btn:hover {
        background: rgba(255,255,255,0.4);
        transform: scale(1.1);
    }
    
    .quantity-badge {
        background: #00ff88;
        color: #0e1117;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: bold;
        margin-left: 5px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .header h1 {
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        font-size: 3rem;
        margin-bottom: 10px;
    }
    
    .stats {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
    }
    
    .status-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #00ff88;
        color: #0e1117;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        z-index: 1000;
    }
    
    .cart-button {
        background: linear-gradient(135deg, #00ff88, #00cc6a) !important;
        color: #0e1117 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .cart-button:hover {
        background: linear-gradient(135deg, #00cc6a, #00aa55) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0, 255, 136, 0.3) !important;
    }
    
    .reset-button {
        background: linear-gradient(135deg, #ff6b6b, #ff5252) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        margin-top: 20px !important;
    }
    
    .reset-button:hover {
        background: linear-gradient(135deg, #ff5252, #ff3838) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = []

if 'cart_items' not in st.session_state:
    st.session_state.cart_items = set()

# CSV file path - use data directory if it exists, otherwise current directory
DATA_DIR = "../data" if os.path.exists("../data") else "data"
CSV_FILE = os.path.join(DATA_DIR, "shopping_list.csv")

def load_shopping_list():
    """Load shopping list from CSV file"""
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df.to_dict('records')
        except Exception as e:
            st.error(f"Error loading shopping list: {e}")
            return []
    return []

def save_shopping_list():
    """Save shopping list to CSV file"""
    try:
        if st.session_state.shopping_list:
            # Ensure data directory exists
            os.makedirs(DATA_DIR, exist_ok=True)
            df = pd.DataFrame(st.session_state.shopping_list)
            df.to_csv(CSV_FILE, index=False)
            return True
        return False
    except Exception as e:
        st.error(f"Error saving shopping list: {e}")
        return False

def add_item(item_name, quantity):
    """Add item to shopping list"""
    if item_name.strip():
        # Check if item already exists
        for item in st.session_state.shopping_list:
            if item['item'].lower() == item_name.strip().lower():
                item['quantity'] += quantity
                save_shopping_list()
                return
        
        # Add new item
        new_item = {
            'item': item_name.strip(),
            'quantity': quantity,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.shopping_list.append(new_item)
        save_shopping_list()

def remove_item(index):
    """Remove item from shopping list"""
    if 0 <= index < len(st.session_state.shopping_list):
        st.session_state.shopping_list.pop(index)
        save_shopping_list()

def clear_all_items():
    """Clear all items from shopping list and clear CSV file contents"""
    st.session_state.shopping_list = []
    st.session_state.cart_items = set()
    
    # Clear the CSV file by saving an empty list
    try:
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        # Save empty DataFrame to clear the CSV file
        empty_df = pd.DataFrame(columns=['item', 'quantity', 'added_date'])
        empty_df.to_csv(CSV_FILE, index=False)
        st.success("✅ All items have been cleared from shopping_list.csv!")
    except Exception as e:
        st.error(f"Error clearing CSV file: {e}")

def add_to_cart(item_name):
    """Add item to cart"""
    st.session_state.cart_items.add(item_name)

def remove_from_cart(item_name):
    """Remove item from cart"""
    st.session_state.cart_items.discard(item_name)

def reset_shopping_list(password):
    """Reset shopping list with password protection"""
    if password == "shopping":
        clear_all_items()
        return True
    return False

# Load existing data
if not st.session_state.shopping_list:
    st.session_state.shopping_list = load_shopping_list()

# Status indicator for Docker/ngrok
if os.path.exists("/app/data"):
    st.markdown('<div class="status-indicator">🐳 Docker</div>', unsafe_allow_html=True)

# Navigation
st.sidebar.title("🛒 Navigation")
page = st.sidebar.radio("Choose a page:", ["📝 Shopping List", "🛍️ Shopping Mode"])

if page == "📝 Shopping List":
    # Import and run the shopping list page
    from pages.shopping_list_page import show_shopping_list_page
    show_shopping_list_page()

elif page == "🛍️ Shopping Mode":
    # Import and run the shopping mode page
    from pages.shopping_mode_page import show_shopping_mode_page
    show_shopping_mode_page() 