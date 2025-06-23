import streamlit as st
import pandas as pd
import os
from datetime import datetime

# CSV file path - use data directory if it exists, otherwise current directory
DATA_DIR = "../../data" if os.path.exists("../../data") else "../data"
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
    # Clear session state
    st.session_state.shopping_list = []
    
    # Clear cart items if it exists in session state
    if 'cart_items' in st.session_state:
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

def show_shopping_list_page():
    """Display the shopping list page"""
    # Main app
    st.markdown('<div class="header"><h1>🛒 Shopping List</h1></div>', unsafe_allow_html=True)

    # Statistics
    total_items = len(st.session_state.shopping_list)
    total_quantity = sum(item['quantity'] for item in st.session_state.shopping_list)

    st.markdown(f'''
    <div class="stats">
        <h3>📊 Statistics</h3>
        <p><strong>Total Items:</strong> {total_items} | <strong>Total Quantity:</strong> {total_quantity}</p>
    </div>
    ''', unsafe_allow_html=True)

    # Input section
    st.markdown("### ➕ Add New Item")

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        new_item = st.text_input("Item name", key="new_item_input", placeholder="Enter item name...")

    with col2:
        quantity = st.number_input("Qty", min_value=1, value=1, key="quantity_input")

    with col3:
        if st.button("Add Item", key="add_button"):
            add_item(new_item, quantity)
            st.rerun()

    # Display items
    st.markdown("### 📝 Your Shopping List")

    if st.session_state.shopping_list:
        # Create columns for better layout
        cols = st.columns(3)
        
        for i, item in enumerate(st.session_state.shopping_list):
            col_index = i % 3
            with cols[col_index]:
                # Create custom HTML for tag-like display
                tag_html = f'''
                <div class="item-tag">
                    {item['item']}
                    <span class="quantity-badge">{item['quantity']}</span>
                    <button class="remove-btn" onclick="removeItem({i})">×</button>
                </div>
                '''
                st.markdown(tag_html, unsafe_allow_html=True)
                
                # Add remove button functionality
                if st.button(f"Remove", key=f"remove_{i}"):
                    remove_item(i)
                    st.rerun()
    else:
        st.markdown("### 🛍️ No items in your shopping list yet!")
        st.markdown("Add some items above to get started!")

    # Clear all button
    st.markdown("---")
    st.markdown("### 🗑️ Clear All Items")
    st.markdown("⚠️ **Warning:** This will clear all items from your shopping list.")
    
    if st.button("🗑️ Clear All Items", key="clear_all"):
        st.write("🔄 Clearing all items...")  # Debug message
        st.write(f"Items before clear: {len(st.session_state.shopping_list)}")  # Debug message
        clear_all_items()
        st.write("✅ Clear operation completed!")  # Debug message
        st.write(f"Items after clear: {len(st.session_state.shopping_list)}")  # Debug message
        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; margin-top: 50px;">
        <p>🛒 Shopping List App | Built with Streamlit & Docker</p>
        <p>Your list is automatically saved to shopping_list.csv</p>
    </div>
    """, unsafe_allow_html=True) 