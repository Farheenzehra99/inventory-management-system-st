import streamlit as st
from inventory import Inventory, Electronics, Grocery, Clothing, DuplicateProductIDError, InsufficientStockError
import datetime

# Gradient Title Style
st.markdown("""
    <h1 style='text-align: center; 
               background: linear-gradient(70deg, #007cf0, #ff0080); 
               -webkit-background-clip: text; 
               -webkit-text-fill-color: transparent;
               font-size: 3rem;'>
        Inventory Management System
    </h1>
""", unsafe_allow_html=True)

# Developer Credit
st.markdown("""
    <p style='text-align: center;
              font-size: 1.2rem;
              margin-top: -10px;
              background: linear-gradient(70deg, #ff0080, #007cf0); 
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
              font-weight: bold;'>
        Developed by Syeda Farheen Zehra
    </p>
""", unsafe_allow_html=True)

# Gradient Button CSS
st.markdown("""
    <style>
        .stButton>button {
            background: linear-gradient(to right, #007cf0, #ff0080);
            border: none;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/fluency/96/warehouse.png", width=100)
st.sidebar.title("📦 Inventory Controls")

# Create Inventory Instance
if "inventory" not in st.session_state:
    st.session_state.inventory = Inventory()

menu = st.sidebar.selectbox("Choose Action", [
    "Add Product", "Sell Product", "Restock Product", 
    "View All Products", "Search Product", "Remove Expired",
    "Total Inventory Value", "Save to File", "Load from File"
])

inventory = st.session_state.inventory

# Action Handling
if menu == "Add Product":
    st.subheader("➕ Add New Product")
    ptype = st.selectbox("Product Type", ["Electronics", "Grocery", "Clothing"])
    pid = st.text_input("Product ID")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0)
    quantity = st.number_input("Quantity", min_value=0)

    if ptype == "Electronics":
        brand = st.text_input("Brand")
        warranty = st.number_input("Warranty Years", min_value=0)
        if st.button("Add Product"):
            try:
                product = Electronics(pid, name, price, quantity, brand, warranty)
                inventory.add_product(product)
                st.success("Electronics product added successfully!")
            except DuplicateProductIDError:
                st.error("❌ Product ID already exists!")

    elif ptype == "Grocery":
        expiry = st.date_input("Expiry Date", min_value=datetime.date.today())
        if st.button("Add Product"):
            try:
                product = Grocery(pid, name, price, quantity, expiry.strftime("%Y-%m-%d"))
                inventory.add_product(product)
                st.success("Grocery product added successfully!")
            except DuplicateProductIDError:
                st.error("❌ Product ID already exists!")

    elif ptype == "Clothing":
        size = st.text_input("Size")
        material = st.text_input("Material")
        if st.button("Add Product"):
            try:
                product = Clothing(pid, name, price, quantity, size, material)
                inventory.add_product(product)
                st.success("Clothing product added successfully!")
            except DuplicateProductIDError:
                st.error("❌ Product ID already exists!")

elif menu == "Sell Product":
    st.subheader("💸 Sell Product")
    pid = st.text_input("Product ID to Sell")
    qty = st.number_input("Quantity to Sell", min_value=0)
    if st.button("Sell"):
        try:
            inventory.update_quantity(pid, -qty)
            st.success("Product sold successfully!")
        except InsufficientStockError:
            st.error("❌ Not enough stock!")
        except Exception as e:
            st.error(f"Error: {e}")

elif menu == "Restock Product":
    st.subheader("🔄 Restock Product")
    pid = st.text_input("Product ID to Restock")
    qty = st.number_input("Quantity to Restock", min_value=0)
    if st.button("Restock"):
        try:
            inventory.update_quantity(pid, qty)
            st.success("Product restocked successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

elif menu == "View All Products":
    st.subheader("📃 All Products")
    products = inventory.list_all_products()
    if not products:
        st.warning("No products found.")
    for product in products:
        st.info(product)

elif menu == "Search Product":
    st.subheader("🔍 Search by Product Name")
    name = st.text_input("Enter product name")
    if st.button("Search"):
        found = inventory.search_product(name)
        if found:
            for p in found:
                st.success(p)
        else:
            st.warning("No matching product found.")

elif menu == "Remove Expired":
    st.subheader("🗑️ Remove Expired Grocery Products")
    inventory.remove_expired_products()
    st.success("Expired groceries removed.")

elif menu == "Total Inventory Value":
    st.subheader("💰 Total Inventory Value")
    value = inventory.total_inventory_value()
    st.success(f"Total Inventory Value: ${value:.2f}")

elif menu == "Save to File":
    st.subheader("💾 Save Inventory to File")
    filename = st.text_input("Enter filename (e.g., data.json)", value="data.json")
    if st.button("Save"):
        inventory.save_to_file(filename)
        st.success("Inventory saved successfully.")

elif menu == "Load from File":
    st.subheader("📂 Load Inventory from File")
    filename = st.text_input("Enter filename (e.g., data.json)", value="data.json")
    if st.button("Load"):
        try:
            inventory.load_from_file(filename)
            st.success("Inventory loaded successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
