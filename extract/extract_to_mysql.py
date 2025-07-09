import os
import json
import mysql.connector
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables from .env
load_dotenv("../.env")

# MySQL credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL successfully!")
except mysql.connector.Error as err:
    print("❌ MySQL connection failed:", err)
    exit()

# -------------------------------
# Create TABLES if not exists
# -------------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_transaction (
        state VARCHAR(100),
        year INT,
        quarter INT,
        transaction_type VARCHAR(100),
        count BIGINT,
        amount DOUBLE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_user (
        state VARCHAR(100),
        year INT,
        quarter INT,
        brand VARCHAR(100),
        count BIGINT,
        percentage FLOAT
    );
""")

conn.commit()

# -------------------------------
# Function: Extract aggregated_transaction
# -------------------------------
def extract_aggregated_transaction():
    base_path = "../data/pulse/data/aggregated/transaction/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="📥 Extracting Transaction Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            txn_data = data.get("data", {}).get("transactionData", [])

                            for txn in txn_data:
                                txn_type = txn.get("name")
                                instrument = txn.get("paymentInstruments", [{}])[0]
                                count = instrument.get("count", 0)
                                amount = instrument.get("amount", 0.0)

                                cursor.execute("""
                                    INSERT INTO aggregated_transaction 
                                    (state, year, quarter, transaction_type, count, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, txn_type, count, amount))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)
    conn.commit()
    print("✅ Data inserted into aggregated_transaction successfully.")

# -------------------------------
# Function: Extract aggregated_user
# -------------------------------
def extract_aggregated_user():
    base_path = "../data/pulse/data/aggregated/user/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="📥 Extracting User Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            user_data = data.get("data", {}).get("usersByDevice")
                            
                            if user_data is None:
                                continue  # 🛑 Skip if no user data

                            for entry in user_data:
                                brand = entry.get("brand", "Unknown")
                                count = entry.get("count", 0)
                                percentage = entry.get("percentage", 0.0)

                                cursor.execute("""
                                    INSERT INTO aggregated_user 
                                    (state, year, quarter, brand, count, percentage)
                                    VALUES (%s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, brand, count, percentage))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)

    conn.commit()
    print("✅ Data inserted into aggregated_user successfully.")

# -------------------------------
# Function: Extract aggregated_insurance
# -------------------------------
def extract_aggregated_insurance():
    base_path = "../data/pulse/data/aggregated/insurance/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="📥 Extracting Insurance Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            ins_data = data.get("data", {}).get("transactionData")
                            
                            if ins_data is None:
                                continue

                            for entry in ins_data:
                                ins_type = entry.get("name", "Unknown")
                                instrument = entry.get("paymentInstruments", [{}])[0]
                                count = instrument.get("count", 0)
                                amount = instrument.get("amount", 0.0)

                                cursor.execute("""
                                    INSERT INTO aggregated_insurance 
                                    (state, year, quarter, insurance_type, count, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, ins_type, count, amount))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)

    conn.commit()
    print("✅ Data inserted into aggregated_insurance successfully.")
# -------------------------------
# Function: extract_map_user()
# -------------------------------
def extract_map_user():
    base_path = "../data/pulse/data/map/user/hover/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="📍 Extracting Map User Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            user_data = data.get("data", {}).get("hoverData", {})

                            for district, stats in user_data.items():
                                registered = stats.get("registeredUsers", 0)
                                app_opens = stats.get("appOpens", 0)

                                cursor.execute("""
                                    INSERT INTO map_user 
                                    (state, year, quarter, district, registered_users, app_opens)
                                    VALUES (%s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, district, registered, app_opens))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)

    conn.commit()
    print("✅ Data inserted into map_user successfully.")

# -------------------------------
# Function: extract_map_transaction()
# -------------------------------
def extract_map_transaction():
    base_path = "../data/pulse/data/map/transaction/hover/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="🗺️ Extracting Map Transaction Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            districts = data.get("data", {}).get("hoverDataList", [])

                            for entry in districts:
                                district = entry.get("name", "Unknown")
                                stats = entry.get("metric", [{}])[0]
                                count = stats.get("count", 0)
                                amount = stats.get("amount", 0.0)

                                cursor.execute("""
                                    INSERT INTO map_transaction 
                                    (state, year, quarter, district, count, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, district, count, amount))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)

    conn.commit()
    print("✅ Data inserted into map_transaction successfully.")

# -------------------------------
# Function: extract_map_insurance()
# -------------------------------
def extract_map_insurance():
    base_path = "../data/pulse/data/map/insurance/hover/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="📌 Extracting Map Insurance Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            districts = data.get("data", {}).get("hoverDataList", [])

                            for entry in districts:
                                district = entry.get("name", "Unknown")
                                stats = entry.get("metric", [{}])[0]
                                count = stats.get("count", 0)
                                amount = stats.get("amount", 0.0)

                                cursor.execute("""
                                    INSERT INTO map_insurance 
                                    (state, year, quarter, district, count, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, district, count, amount))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)

    conn.commit()
    print("✅ Data inserted into map_insurance successfully.")

# -------------------------------
# Function: extract_top_user()
# -------------------------------
def extract_top_user():
    base_path = "../data/pulse/data/top/user/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="👤 Extracting Top User Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            top_users = data.get("data", {}).get("pincodes", [])

                            for entry in top_users:
                                pincode = entry.get("name", "Unknown")
                                registered_users = entry.get("registeredUsers", 0)

                                cursor.execute("""
                                    INSERT INTO top_user 
                                    (state, year, quarter, pincode, registered_users)
                                    VALUES (%s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, pincode, registered_users))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)

    conn.commit()
    print("✅ Data inserted into top_user successfully.")

# -------------------------------
# Function: extract_top_map()
# -------------------------------
def extract_top_map():
    base_path = "../data/pulse/data/top/transaction/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="📍 Extracting Top Map Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            districts = data.get("data", {}).get("districts", [])
                            pincodes = data.get("data", {}).get("pincodes", [])

                            # District entries
                            for entry in districts:
                                name = entry.get("entityName", "Unknown")
                                stats = entry.get("metric", {})
                                count = stats.get("count", 0)
                                amount = stats.get("amount", 0.0)

                                cursor.execute("""
                                    INSERT INTO top_map 
                                    (state, year, quarter, name, entity_type, count, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, name, "district", count, amount))

                            # Pincode entries
                            for entry in pincodes:
                                name = entry.get("entityName", "Unknown")
                                stats = entry.get("metric", {})
                                count = stats.get("count", 0)
                                amount = stats.get("amount", 0.0)

                                cursor.execute("""
                                    INSERT INTO top_map 
                                    (state, year, quarter, name, entity_type, count, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, name, "pincode", count, amount))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)

    conn.commit()
    print("✅ Data inserted into top_map successfully.")

# -------------------------------
# Function: extract_top_insurance()
# -------------------------------
def extract_top_insurance():
    base_path = "../data/pulse/data/top/insurance/country/india/state"
    for state in tqdm(os.listdir(base_path), desc="🛡️ Extracting Top Insurance Data"):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file_name in os.listdir(year_path):
                if file_name.endswith(".json"):
                    quarter = int(file_name.strip(".json"))
                    file_path = os.path.join(year_path, file_name)

                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                            districts = data.get("data", {}).get("districts", [])
                            pincodes = data.get("data", {}).get("pincodes", [])

                            # District entries
                            for entry in districts:
                                name = entry.get("entityName", "Unknown")
                                stats = entry.get("metric", {})
                                count = stats.get("count", 0)
                                amount = stats.get("amount", 0.0)

                                cursor.execute("""
                                    INSERT INTO top_insurance 
                                    (state, year, quarter, name, entity_type, count, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, name, "district", count, amount))

                            # Pincode entries
                            for entry in pincodes:
                                name = entry.get("entityName", "Unknown")
                                stats = entry.get("metric", {})
                                count = stats.get("count", 0)
                                amount = stats.get("amount", 0.0)

                                cursor.execute("""
                                    INSERT INTO top_insurance 
                                    (state, year, quarter, name, entity_type, count, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                                """, (state, int(year), quarter, name, "pincode", count, amount))
                    except Exception as e:
                        print(f"❌ Error processing {file_path}:", e)

    conn.commit()
    print("✅ Data inserted into top_insurance successfully.")

# -------------------------------
# Run All Extraction Functions
# -------------------------------

extract_aggregated_transaction()
extract_aggregated_user()
extract_aggregated_insurance()
extract_map_user()
extract_map_transaction()
extract_map_insurance()
extract_top_user()
extract_top_map()
extract_top_insurance()

# Close MySQL connection
cursor.close()
conn.close()
print("🔒 MySQL connection closed.")
