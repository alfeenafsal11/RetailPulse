"""
RetailPulse — Data Validation Tests

Validates the generated CSV files for integrity, consistency, and distribution sanity.

Usage:
    python tests/test_data.py
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
CUSTOMERS_PATH = os.path.join(DATA_DIR, "customers.csv")
PRODUCTS_PATH = os.path.join(DATA_DIR, "products.csv")
TRANSACTIONS_PATH = os.path.join(DATA_DIR, "transactions.csv")

# Expected constants
DATE_START = datetime(2024, 7, 1)
DATE_END = datetime(2026, 6, 30)
EXPECTED_CATEGORIES = {"Electronics", "Fashion", "Beauty", "Home", "Sports", "Grocery", "Accessories"}
EXPECTED_SEGMENTS = {"Champion", "Loyal", "New", "At Risk", "Lost"}


class ValidationResult:
    def __init__(self):
        self.results = []
        self.all_pass = True

    def check(self, name: str, condition: bool, detail: str = ""):
        status = "PASS" if condition else "FAIL"
        self.results.append((name, status, detail))
        print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
        if not condition:
            self.all_pass = False

    def summary(self):
        passed = sum(1 for _, s, _ in self.results if s == "PASS")
        failed = sum(1 for _, s, _ in self.results if s == "FAIL")
        total = len(self.results)
        return passed, failed, total


def run_validation():
    """Run all validation checks on generated CSV files."""
    print("=" * 60)
    print("RetailPulse — Data Validation")
    print("=" * 60)

    v = ValidationResult()

    # --- Check files exist ---
    print("\n[1] File existence checks")
    v.check("customers.csv exists", os.path.exists(CUSTOMERS_PATH))
    v.check("products.csv exists", os.path.exists(PRODUCTS_PATH))
    v.check("transactions.csv exists", os.path.exists(TRANSACTIONS_PATH))

    if not v.all_pass:
        print("\n✗ CSV files not found. Run 'python src/data_generator.py' first.")
        return v

    # --- Load data ---
    print("\n[2] Loading data...")
    customers = pd.read_csv(CUSTOMERS_PATH)
    products = pd.read_csv(PRODUCTS_PATH)
    transactions = pd.read_csv(TRANSACTIONS_PATH)

    print(f"  Loaded: {len(customers)} customers, {len(products)} products, {len(transactions)} transactions")

    # --- Row counts ---
    print("\n[3] Row count checks")
    v.check("Customers ~10,000", 9_000 <= len(customers) <= 11_000,
            f"actual={len(customers)}")
    v.check("Products ~500", 400 <= len(products) <= 600,
            f"actual={len(products)}")
    v.check("Transactions ~250,000", 150_000 <= len(transactions) <= 350_000,
            f"actual={len(transactions)}")

    # --- ID uniqueness ---
    print("\n[4] ID uniqueness")
    v.check("customer_id unique", customers["customer_id"].is_unique)
    v.check("product_id unique", products["product_id"].is_unique)
    v.check("transaction_id unique", transactions["transaction_id"].is_unique)

    # --- Foreign key integrity ---
    print("\n[5] Foreign key integrity")
    valid_cids = set(customers["customer_id"])
    valid_pids = set(products["product_id"])
    fk_cust = transactions["customer_id"].isin(valid_cids).all()
    fk_prod = transactions["product_id"].isin(valid_pids).all()
    v.check("transactions.customer_id → customers", fk_cust)
    v.check("transactions.product_id → products", fk_prod)

    # --- NULL checks ---
    print("\n[6] Required fields (no NULLs)")
    for col in customers.columns:
        v.check(f"customers.{col} not null", customers[col].notna().all())
    for col in products.columns:
        v.check(f"products.{col} not null", products[col].notna().all())
    for col in transactions.columns:
        v.check(f"transactions.{col} not null", transactions[col].notna().all())

    # --- Amount validity ---
    print("\n[7] Amount validity")
    v.check("All amounts >= 0", (transactions["amount"] >= 0).all())
    v.check("All prices > 0", (products["price"] > 0).all())
    v.check("All costs > 0", (products["cost"] > 0).all())
    v.check("All quantities >= 1", (transactions["quantity"] >= 1).all())
    v.check("All discounts >= 0", (transactions["discount"] >= 0).all())
    v.check("All unit_prices > 0", (transactions["unit_price"] > 0).all())

    # Amount consistency
    expected_amount = transactions["quantity"] * transactions["unit_price"] - transactions["discount"]
    diff = (transactions["amount"] - expected_amount).abs()
    max_diff = diff.max()
    v.check("Amount = qty × unit_price − discount (tol=0.02)",
            (diff < 0.02).all(),
            f"max_diff={max_diff:.4f}")

    # --- Timestamp validity ---
    print("\n[8] Timestamp validity")
    ts = pd.to_datetime(transactions["transaction_timestamp"])
    v.check("All timestamps >= DATE_START",
            (ts >= pd.Timestamp(DATE_START)).all())
    v.check("All timestamps <= DATE_END",
            (ts <= pd.Timestamp(DATE_END)).all())

    # --- Distribution sanity ---
    print("\n[9] Distribution sanity")
    segments = set(customers["customer_segment_ground_truth"].unique())
    v.check(f"All 5 segments present",
            EXPECTED_SEGMENTS.issubset(segments),
            f"found={segments}")

    cats = set(products["category"].unique())
    v.check(f"All 7 categories present",
            EXPECTED_CATEGORIES.issubset(cats),
            f"found={cats}")

    txn_per_cust = transactions["customer_id"].value_counts()
    max_txn = txn_per_cust.max()
    v.check(f"No customer dominates transactions",
            max_txn < len(transactions) * 0.01,
            f"max={max_txn}")

    v.check("Quantity range reasonable (1-10)",
            transactions["quantity"].between(1, 10).all())

    discount_rate = transactions["discount"] / (transactions["quantity"] * transactions["unit_price"])
    v.check("Discount rates reasonable (0-50%)",
            (discount_rate <= 0.50).all())

    # Payment methods
    pm_count = transactions["payment_method"].nunique()
    v.check(f"Multiple payment methods ({pm_count})", pm_count >= 3)

    # Channels
    ch_count = transactions["channel"].nunique()
    v.check(f"Multiple channels ({ch_count})", ch_count >= 2)

    # Signup dates
    signup_dates = pd.to_datetime(customers["signup_date"])
    v.check("Signup dates within window",
            (signup_dates >= pd.Timestamp(DATE_START)).all()
            and (signup_dates <= pd.Timestamp(DATE_END)).all())

    # --- Summary ---
    passed, failed, total = v.summary()
    print("\n" + "=" * 60)
    print(f"VALIDATION SUMMARY: {passed}/{total} passed, {failed} failed")
    print("=" * 60)

    if v.all_pass:
        print("✓ All validation checks PASSED")
    else:
        print("✗ Some checks FAILED")
        for name, status, detail in v.results:
            if status == "FAIL":
                print(f"  FAILED: {name} {detail}")

    return v


if __name__ == "__main__":
    result = run_validation()
    sys.exit(0 if result.all_pass else 1)
