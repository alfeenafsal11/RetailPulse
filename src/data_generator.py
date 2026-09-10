"""
RetailPulse — Synthetic Retail Data Generator

Generates reproducible synthetic retail transaction data with behavioral
customer archetypes for RFM segmentation and cohort retention analysis.

Usage:
    python src/data_generator.py

Output:
    data/raw/customers.csv
    data/raw/products.csv
    data/raw/transactions.csv
"""

import os
import time
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURATION
# ============================================================================

SEED = 42
NUM_CUSTOMERS = 10_000
NUM_PRODUCTS = 500
TARGET_TRANSACTIONS = 250_000

# Analysis window: 24 months
DATE_START = datetime(2024, 7, 1)
DATE_END = datetime(2026, 6, 30)
DATE_RANGE_DAYS = (DATE_END - DATE_START).days  # ~730 days

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")

# ============================================================================
# CUSTOMER ARCHETYPES
# ============================================================================

# Each archetype defines latent behavioral parameters
ARCHETYPES = {
    "Champion": {
        "fraction": 0.10,
        "purchase_freq_range": (40, 80),     # transactions over 2 years
        "aov_range": (80, 250),              # average order value
        "preferred_category_weight": 0.35,
        "inactivity_prob": 0.02,             # very low — still active
        "last_purchase_recency_days": (0, 30),  # very recent
        "signup_period_frac": (0.0, 0.7),    # signed up earlier
    },
    "Loyal": {
        "fraction": 0.20,
        "purchase_freq_range": (25, 50),
        "aov_range": (50, 150),
        "preferred_category_weight": 0.30,
        "inactivity_prob": 0.05,
        "last_purchase_recency_days": (0, 60),
        "signup_period_frac": (0.0, 0.6),
    },
    "New": {
        "fraction": 0.20,
        "purchase_freq_range": (2, 8),
        "aov_range": (30, 120),
        "preferred_category_weight": 0.20,
        "inactivity_prob": 0.10,
        "last_purchase_recency_days": (0, 45),
        "signup_period_frac": (0.75, 1.0),   # signed up recently
    },
    "At Risk": {
        "fraction": 0.25,
        "purchase_freq_range": (15, 40),
        "aov_range": (40, 160),
        "preferred_category_weight": 0.25,
        "inactivity_prob": 0.60,             # high — stopped buying
        "last_purchase_recency_days": (120, 360),
        "signup_period_frac": (0.0, 0.5),
    },
    "Lost": {
        "fraction": 0.25,
        "purchase_freq_range": (5, 20),
        "aov_range": (25, 100),
        "preferred_category_weight": 0.20,
        "inactivity_prob": 0.85,             # very high
        "last_purchase_recency_days": (300, 700),
        "signup_period_frac": (0.0, 0.4),
    },
}

# Demographic options
CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Chandigarh", "Kochi", "Indore", "Nagpur", "Coimbatore",
]
AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
GENDERS = ["Male", "Female", "Other"]
CHANNELS_ACQ = ["Organic", "Referral", "Social Media", "Paid Ads", "Email"]

# Product configuration
CATEGORIES = {
    "Electronics": {
        "subcategories": ["Smartphones", "Laptops", "Headphones", "Tablets", "Chargers", "Cameras"],
        "price_range": (15, 800),
        "margin": 0.25,
    },
    "Fashion": {
        "subcategories": ["T-Shirts", "Jeans", "Dresses", "Jackets", "Sneakers", "Watches"],
        "price_range": (10, 200),
        "margin": 0.45,
    },
    "Beauty": {
        "subcategories": ["Skincare", "Makeup", "Perfume", "Haircare", "Nailcare"],
        "price_range": (5, 120),
        "margin": 0.55,
    },
    "Home": {
        "subcategories": ["Bedding", "Kitchenware", "Decor", "Lighting", "Storage"],
        "price_range": (8, 300),
        "margin": 0.35,
    },
    "Sports": {
        "subcategories": ["Fitness", "Yoga", "Running", "Cycling", "Swimming"],
        "price_range": (10, 250),
        "margin": 0.40,
    },
    "Grocery": {
        "subcategories": ["Snacks", "Beverages", "Organic", "Dairy", "Bakery"],
        "price_range": (2, 50),
        "margin": 0.20,
    },
    "Accessories": {
        "subcategories": ["Bags", "Wallets", "Sunglasses", "Belts", "Jewelry"],
        "price_range": (5, 150),
        "margin": 0.50,
    },
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]
TRANSACTION_CHANNELS = ["Online", "In-Store", "Mobile App"]


# ============================================================================
# GENERATORS
# ============================================================================

def generate_customers(rng: np.random.Generator) -> pd.DataFrame:
    """Generate customer records with behavioral archetype assignment."""
    print(f"  Generating {NUM_CUSTOMERS} customers...")

    customers = []
    customer_id = 1

    for archetype_name, params in ARCHETYPES.items():
        n = int(NUM_CUSTOMERS * params["fraction"])
        # Last archetype absorbs rounding remainder
        if archetype_name == list(ARCHETYPES.keys())[-1]:
            n = NUM_CUSTOMERS - (customer_id - 1)

        # Signup dates: within the archetype's signup period
        signup_start_day = int(DATE_RANGE_DAYS * params["signup_period_frac"][0])
        signup_end_day = int(DATE_RANGE_DAYS * params["signup_period_frac"][1])
        if signup_end_day <= signup_start_day:
            signup_end_day = signup_start_day + 1
        signup_offsets = rng.integers(signup_start_day, signup_end_day, size=n)
        signup_dates = [DATE_START + timedelta(days=int(d)) for d in signup_offsets]

        cities = rng.choice(CITIES, size=n)
        age_groups = rng.choice(AGE_GROUPS, size=n, p=[0.20, 0.30, 0.25, 0.15, 0.10])
        genders = rng.choice(GENDERS, size=n, p=[0.48, 0.48, 0.04])
        acq_channels = rng.choice(CHANNELS_ACQ, size=n)

        for i in range(n):
            customers.append({
                "customer_id": customer_id,
                "signup_date": signup_dates[i].strftime("%Y-%m-%d"),
                "city": cities[i],
                "age_group": age_groups[i],
                "gender": genders[i],
                "acquisition_channel": acq_channels[i],
                "customer_segment_ground_truth": archetype_name,
            })
            customer_id += 1

    df = pd.DataFrame(customers)
    print(f"  ✓ Generated {len(df)} customers")
    return df


def generate_products(rng: np.random.Generator) -> pd.DataFrame:
    """Generate product catalog across 7 categories."""
    print(f"  Generating {NUM_PRODUCTS} products...")

    products = []
    product_id = 1
    category_names = list(CATEGORIES.keys())
    products_per_category = NUM_PRODUCTS // len(category_names)
    remainder = NUM_PRODUCTS - products_per_category * len(category_names)

    for idx, (cat_name, cat_config) in enumerate(CATEGORIES.items()):
        n = products_per_category + (1 if idx < remainder else 0)
        subcats = cat_config["subcategories"]
        price_lo, price_hi = cat_config["price_range"]
        margin = cat_config["margin"]

        prices = np.round(rng.uniform(price_lo, price_hi, size=n), 2)
        costs = np.round(prices * (1 - margin) * rng.uniform(0.85, 1.05, size=n), 2)
        assigned_subcats = rng.choice(subcats, size=n)

        for i in range(n):
            products.append({
                "product_id": product_id,
                "category": cat_name,
                "subcategory": assigned_subcats[i],
                "price": prices[i],
                "cost": costs[i],
            })
            product_id += 1

    df = pd.DataFrame(products)
    print(f"  ✓ Generated {len(df)} products")
    return df


def generate_transactions(
    rng: np.random.Generator,
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
) -> pd.DataFrame:
    """Generate transactions driven by customer behavioral archetypes."""
    print(f"  Generating ~{TARGET_TRANSACTIONS} transactions...")

    # Pre-compute product arrays by category for fast lookup
    category_names = list(CATEGORIES.keys())
    products_by_cat = {}
    for cat in category_names:
        cat_products = products_df[products_df["category"] == cat]
        products_by_cat[cat] = {
            "product_ids": cat_products["product_id"].values,
            "prices": cat_products["price"].values,
        }

    all_product_ids = products_df["product_id"].values
    all_prices = products_df["price"].values

    # Build per-customer generation parameters
    records = []
    transaction_id = 1

    # Group customers by archetype for vectorized parameter generation
    for archetype_name, params in ARCHETYPES.items():
        arch_customers = customers_df[
            customers_df["customer_segment_ground_truth"] == archetype_name
        ]
        n_cust = len(arch_customers)
        if n_cust == 0:
            continue

        # Sample number of transactions per customer
        freq_lo, freq_hi = params["purchase_freq_range"]
        n_transactions_per = rng.integers(freq_lo, freq_hi + 1, size=n_cust)

        # Apply inactivity: some customers stop early
        inactivity_mask = rng.random(size=n_cust) < params["inactivity_prob"]

        # Sample AOV per customer
        aov_lo, aov_hi = params["aov_range"]
        customer_aovs = rng.uniform(aov_lo, aov_hi, size=n_cust)

        # Preferred category per customer
        pref_cats = rng.choice(category_names, size=n_cust)

        # Recency constraint
        rec_lo, rec_hi = params["last_purchase_recency_days"]

        cust_ids = arch_customers["customer_id"].values
        signup_dates = pd.to_datetime(arch_customers["signup_date"].values)

        for i in range(n_cust):
            cid = cust_ids[i]
            signup = signup_dates[i].to_pydatetime()
            n_txn = int(n_transactions_per[i])
            aov = customer_aovs[i]
            pref_cat = pref_cats[i]
            is_inactive = inactivity_mask[i]

            if n_txn == 0:
                continue

            # Determine transaction window
            earliest = signup
            if is_inactive:
                # Inactive customers stop purchasing earlier
                days_available = (DATE_END - signup).days
                if days_available <= 0:
                    continue
                cutoff_frac = rng.uniform(0.3, 0.7)
                latest = signup + timedelta(days=int(days_available * cutoff_frac))
            else:
                # Active customers have recent purchases
                recency_days = int(rng.integers(rec_lo, max(rec_lo + 1, rec_hi)))
                latest = DATE_END - timedelta(days=recency_days)

            if latest <= earliest:
                latest = earliest + timedelta(days=1)

            # Generate transaction timestamps (sorted)
            days_span = (latest - earliest).days
            if days_span <= 0:
                days_span = 1
            txn_offsets = np.sort(rng.integers(0, days_span, size=n_txn))
            hour_offsets = rng.integers(8, 22, size=n_txn)  # 8 AM to 10 PM
            minute_offsets = rng.integers(0, 60, size=n_txn)

            for j in range(n_txn):
                ts = earliest + timedelta(
                    days=int(txn_offsets[j]),
                    hours=int(hour_offsets[j]),
                    minutes=int(minute_offsets[j]),
                )
                # Clamp to analysis window
                if ts > DATE_END:
                    ts = DATE_END - timedelta(minutes=rng.integers(1, 1440))
                if ts < DATE_START:
                    ts = DATE_START + timedelta(minutes=rng.integers(1, 1440))

                # Choose product: prefer category with weight
                if rng.random() < params["preferred_category_weight"] and pref_cat in products_by_cat:
                    cat_data = products_by_cat[pref_cat]
                    pidx = rng.integers(0, len(cat_data["product_ids"]))
                    prod_id = int(cat_data["product_ids"][pidx])
                    base_price = float(cat_data["prices"][pidx])
                else:
                    pidx = rng.integers(0, len(all_product_ids))
                    prod_id = int(all_product_ids[pidx])
                    base_price = float(all_prices[pidx])

                # Quantity: mostly 1, sometimes more
                qty = int(rng.choice([1, 1, 1, 2, 2, 3], size=1)[0])

                # Unit price: slight variation around product price
                unit_price = round(base_price * rng.uniform(0.95, 1.05), 2)

                # Discount: 0–20% of subtotal, skewed low
                subtotal = qty * unit_price
                discount_rate = float(rng.choice(
                    [0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20],
                    size=1,
                )[0])
                discount = round(subtotal * discount_rate, 2)

                # Amount
                amount = round(subtotal - discount, 2)
                if amount < 0:
                    amount = 0.0
                    discount = round(subtotal, 2)

                records.append({
                    "transaction_id": transaction_id,
                    "customer_id": cid,
                    "transaction_timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "product_id": prod_id,
                    "quantity": qty,
                    "unit_price": unit_price,
                    "discount": discount,
                    "amount": amount,
                    "payment_method": str(rng.choice(PAYMENT_METHODS)),
                    "channel": str(rng.choice(TRANSACTION_CHANNELS)),
                })
                transaction_id += 1

    df = pd.DataFrame(records)
    print(f"  ✓ Generated {len(df)} transactions")
    return df


# ============================================================================
# VALIDATION
# ============================================================================

def validate_data(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
) -> bool:
    """Run comprehensive data validation. Returns True if all checks pass."""
    print("\n  Running data validation...")
    all_pass = True

    def check(name: str, condition: bool):
        nonlocal all_pass
        status = "PASS" if condition else "FAIL"
        print(f"    {name}: {status}")
        if not condition:
            all_pass = False

    # ID uniqueness
    check("customer_id uniqueness",
          customers_df["customer_id"].is_unique)
    check("product_id uniqueness",
          products_df["product_id"].is_unique)
    check("transaction_id uniqueness",
          transactions_df["transaction_id"].is_unique)

    # Foreign key integrity
    valid_cust_ids = set(customers_df["customer_id"])
    valid_prod_ids = set(products_df["product_id"])
    check("FK: transaction.customer_id → customers",
          transactions_df["customer_id"].isin(valid_cust_ids).all())
    check("FK: transaction.product_id → products",
          transactions_df["product_id"].isin(valid_prod_ids).all())

    # NULL checks
    for col in ["customer_id", "signup_date", "city", "age_group", "gender",
                "acquisition_channel", "customer_segment_ground_truth"]:
        check(f"No NULLs in customers.{col}",
              customers_df[col].notna().all())

    for col in ["product_id", "category", "subcategory", "price", "cost"]:
        check(f"No NULLs in products.{col}",
              products_df[col].notna().all())

    for col in ["transaction_id", "customer_id", "transaction_timestamp",
                "product_id", "quantity", "unit_price", "discount", "amount",
                "payment_method", "channel"]:
        check(f"No NULLs in transactions.{col}",
              transactions_df[col].notna().all())

    # Amount validity
    check("No negative amounts",
          (transactions_df["amount"] >= 0).all())
    check("Positive prices",
          (products_df["price"] > 0).all())
    check("Positive costs",
          (products_df["cost"] > 0).all())

    # Amount consistency: amount ≈ quantity * unit_price - discount
    expected = (transactions_df["quantity"] * transactions_df["unit_price"]
                - transactions_df["discount"])
    diff = (transactions_df["amount"] - expected).abs()
    check("Amount consistency (|diff| < 0.02)",
          (diff < 0.02).all())

    # Timestamp validity
    timestamps = pd.to_datetime(transactions_df["transaction_timestamp"])
    check("Timestamps within analysis window",
          (timestamps >= pd.Timestamp(DATE_START)).all()
          and (timestamps <= pd.Timestamp(DATE_END)).all())

    # Distribution sanity
    segments = customers_df["customer_segment_ground_truth"].nunique()
    check(f"Multiple customer archetypes ({segments} segments)",
          segments >= 5)

    categories_present = products_df["category"].nunique()
    check(f"All product categories ({categories_present}/7)",
          categories_present == 7)

    max_txn_per_customer = transactions_df["customer_id"].value_counts().max()
    total_txn = len(transactions_df)
    check(f"No single customer dominates (max={max_txn_per_customer}, total={total_txn})",
          max_txn_per_customer < total_txn * 0.01)

    check("Reasonable quantities (1-10)",
          (transactions_df["quantity"] >= 1).all()
          and (transactions_df["quantity"] <= 10).all())

    check("Reasonable discounts (>= 0)",
          (transactions_df["discount"] >= 0).all())

    check(f"Transaction count near target ({total_txn} vs {TARGET_TRANSACTIONS})",
          abs(total_txn - TARGET_TRANSACTIONS) / TARGET_TRANSACTIONS < 0.30)

    if all_pass:
        print("  ✓ All validation checks PASSED")
    else:
        print("  ✗ Some validation checks FAILED")

    return all_pass


# ============================================================================
# FILE I/O
# ============================================================================

def save_data(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
) -> dict:
    """Save DataFrames to CSV. Returns file sizes."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    paths = {
        "customers": os.path.join(OUTPUT_DIR, "customers.csv"),
        "products": os.path.join(OUTPUT_DIR, "products.csv"),
        "transactions": os.path.join(OUTPUT_DIR, "transactions.csv"),
    }

    customers_df.to_csv(paths["customers"], index=False)
    products_df.to_csv(paths["products"], index=False)
    transactions_df.to_csv(paths["transactions"], index=False)

    sizes = {}
    for name, path in paths.items():
        size_bytes = os.path.getsize(path)
        if size_bytes > 1_000_000:
            sizes[name] = f"{size_bytes / 1_000_000:.1f} MB"
        else:
            sizes[name] = f"{size_bytes / 1_000:.1f} KB"
        print(f"  Saved {path} ({sizes[name]})")

    return sizes


def file_md5(path: str) -> str:
    """Compute MD5 hash of a file."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("RetailPulse — Synthetic Data Generator")
    print("=" * 60)
    print(f"\nSeed: {SEED}")
    print(f"Target: {NUM_CUSTOMERS} customers, {NUM_PRODUCTS} products, ~{TARGET_TRANSACTIONS} transactions")
    print(f"Date range: {DATE_START.date()} to {DATE_END.date()}")
    print()

    # Initialize RNG
    rng = np.random.default_rng(SEED)

    # --- Generate ---
    t_start = time.time()

    print("[1/5] Generating customers...")
    customers_df = generate_customers(rng)

    print("[2/5] Generating products...")
    products_df = generate_products(rng)

    print("[3/5] Generating transactions...")
    transactions_df = generate_transactions(rng, customers_df, products_df)

    t_gen = time.time() - t_start
    print(f"\nGeneration time: {t_gen:.2f}s")

    # --- Validate ---
    print("\n[4/5] Validating data...")
    t_val_start = time.time()
    valid = validate_data(customers_df, products_df, transactions_df)
    t_val = time.time() - t_val_start
    print(f"Validation time: {t_val:.2f}s")

    if not valid:
        print("\n✗ VALIDATION FAILED — aborting save")
        return False

    # --- Save ---
    print("\n[5/5] Saving CSV files...")
    sizes = save_data(customers_df, products_df, transactions_df)

    # --- Summary ---
    print("\n" + "=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    print(f"Customers:    {len(customers_df):,}")
    print(f"Products:     {len(products_df):,}")
    print(f"Transactions: {len(transactions_df):,}")
    print(f"Date range:   {DATE_START.date()} to {DATE_END.date()}")
    print(f"Gen time:     {t_gen:.2f}s")
    print(f"Val time:     {t_val:.2f}s")
    for name, size in sizes.items():
        print(f"CSV {name}: {size}")

    # Segment distribution
    print("\nCustomer segment distribution:")
    seg_counts = customers_df["customer_segment_ground_truth"].value_counts()
    for seg, count in seg_counts.items():
        print(f"  {seg}: {count} ({count/len(customers_df)*100:.1f}%)")

    # Transactions per segment
    merged = transactions_df.merge(
        customers_df[["customer_id", "customer_segment_ground_truth"]],
        on="customer_id",
    )
    print("\nTransactions per segment:")
    txn_seg = merged["customer_segment_ground_truth"].value_counts()
    for seg, count in txn_seg.items():
        print(f"  {seg}: {count:,}")

    print("\n✓ Data generation complete")
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
