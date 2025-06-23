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

def show_shopping_mode_page():
    """Display the shopping mode page"""
    # Shopping Mode
    st.markdown('<div class="header"><h1>🛍️ Shopping Mode</h1></div>', unsafe_allow_html=True)

    # Statistics for shopping mode
    total_items = len(st.session_state.shopping_list)
    items_in_cart = len(st.session_state.cart_items)
    remaining_items = total_items - items_in_cart

    st.markdown(f'''
    <div class="stats">
        <h3>📊 Shopping Progress</h3>
        <p><strong>Total Items:</strong> {total_items} | <strong>In Cart:</strong> {items_in_cart} | <strong>Remaining:</strong> {remaining_items}</p>
    </div>
    ''', unsafe_allow_html=True)

    if st.session_state.shopping_list:
        st.markdown("### 🛒 Shopping List Table")
        
        # Create table data with checkboxes
        table_data = []
        for i, item in enumerate(st.session_state.shopping_list):
            item_name = item['item']
            in_cart = item_name in st.session_state.cart_items
            status = "✅ In Cart" if in_cart else "⏳ Pending"
            
            table_data.append({
                "In Cart": in_cart,
                "Item": item['item'],
                "Quantity": item['quantity'],
                "Status": status
            })
        
        # Display interactive table with checkboxes
        df = pd.DataFrame(table_data)
        
        # Use data_editor for interactive table with checkboxes
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "In Cart": st.column_config.CheckboxColumn(
                    "In Cart",
                    width="small",
                    help="Check to mark item as added to cart"
                ),
                "Item": st.column_config.TextColumn("Item", width="medium"),
                "Quantity": st.column_config.NumberColumn("Quantity", width="small"),
                "Status": st.column_config.TextColumn("Status", width="medium")
            }
        )
        
        # Handle checkbox changes
        for i, (original_row, edited_row) in enumerate(zip(df.iterrows(), edited_df.iterrows())):
            original_in_cart = original_row[1]['In Cart']
            edited_in_cart = edited_row[1]['In Cart']
            
            if original_in_cart != edited_in_cart:
                item_name = st.session_state.shopping_list[i]['item']
                if edited_in_cart:
                    add_to_cart(item_name)
                else:
                    remove_from_cart(item_name)
                st.rerun()
        
        # Reset section
        st.markdown("---")
        st.markdown("### 🔄 Reset Shopping List")
        st.markdown("⚠️ **Warning:** This will clear all items from your shopping list.")
        
        # Password input
        password = st.text_input("Enter password to confirm reset:", type="password", key="reset_password")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🗑️ Reset All Items", key="reset_button"):
                if reset_shopping_list(password):
                    st.success("✅ Shopping list has been reset successfully!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password! Shopping list was not reset.")
        
        with col2:
            st.markdown("💡 **Hint:** The password is 'shopping'")
    
    else:
        st.markdown("### 🛍️ No items in your shopping list!")
        st.markdown("Go to the Shopping List page to add some items first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; margin-top: 50px;">
        <p>🛍️ Shopping Mode | Track your shopping progress</p>
        <p>Check items as added to cart and reset when done</p>
    </div>
    """, unsafe_allow_html=True) 