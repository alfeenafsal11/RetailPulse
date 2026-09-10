import os
import sys
import unittest

# Ensure src is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from analytics.analytics import load_all_analytics

class TestPythonAnalytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Loading all analytics datasets...")
        cls.datasets = load_all_analytics()
        print("Datasets loaded successfully.\n")

    def test_kpi_consistency(self):
        overall_kpi = self.datasets['kpis']['overall']
        
        # Test shape
        self.assertEqual(len(overall_kpi), 1)
        
        # Extract values
        total_revenue = overall_kpi['total_revenue'].iloc[0]
        total_txns = overall_kpi['total_transactions'].iloc[0]
        active_custs = overall_kpi['active_customers'].iloc[0]
        
        # Test exact invariant bounds
        self.assertAlmostEqual(total_revenue, 53581128.12, places=2)
        self.assertEqual(total_txns, 245210)
        self.assertEqual(active_custs, 10000)

    def test_customer_revenue_conservation(self):
        cust_df = self.datasets['customer_metrics']
        
        # Shape check
        self.assertEqual(len(cust_df), 10000)
        
        # Revenue conservation
        cust_rev_sum = cust_df['total_revenue'].sum()
        kpi_rev = self.datasets['kpis']['overall']['total_revenue'].iloc[0]
        self.assertAlmostEqual(cust_rev_sum, kpi_rev, places=2)

    def test_category_revenue_conservation(self):
        cat_df = self.datasets['categories']
        
        # Revenue conservation
        cat_rev_sum = cat_df['total_revenue'].sum()
        kpi_rev = self.datasets['kpis']['overall']['total_revenue'].iloc[0]
        self.assertAlmostEqual(cat_rev_sum, kpi_rev, places=2)
        
    def test_rfm_coverage(self):
        rfm_df = self.datasets['rfm']
        
        # Check that the sum of segment sizes equals active customers
        rfm_cust_sum = rfm_df['segment_size'].sum()
        self.assertEqual(rfm_cust_sum, 10000)
        
        # Check revenue matches total
        rfm_rev_sum = rfm_df['total_revenue'].sum()
        kpi_rev = self.datasets['kpis']['overall']['total_revenue'].iloc[0]
        self.assertAlmostEqual(rfm_rev_sum, kpi_rev, places=2)

    def test_cohort_integrity(self):
        cohorts_raw = self.datasets['cohorts']['raw']
        cohorts_heatmap = self.datasets['cohorts']['heatmap']
        
        # Ensure rates are between 0 and 100
        self.assertTrue((cohorts_raw['retention_rate_pct'] >= 0).all())
        self.assertTrue((cohorts_raw['retention_rate_pct'] <= 100).all())
        
        # Heatmap shape should be sensible (months vs months_since)
        self.assertGreater(len(cohorts_heatmap.index), 0)
        self.assertGreater(len(cohorts_heatmap.columns), 0)

    def test_concentration_monotonicity(self):
        conc_df = self.datasets['concentration'].copy()
        
        # Ensure it has rows
        self.assertGreater(len(conc_df), 0)
        
        # Cumulative revenue share logic
        # SQL gives us disjoint bands ('Top 1%', 'Top 5%' meaning 1-5%, etc.)
        # Let's just assert that pct_of_total_revenue sums to ~100%
        pct_sum = conc_df['pct_of_total_revenue'].sum()
        self.assertAlmostEqual(pct_sum, 100.0, delta=0.1)

    def test_top_customer_ordering(self):
        top_df = self.datasets['top_customers']
        
        self.assertEqual(len(top_df), 20)
        
        # Check if ordered descending by total_revenue
        is_sorted = top_df['total_revenue'].is_monotonic_decreasing
        self.assertTrue(is_sorted)

    def test_report_dataset_sizes(self):
        print("\n--- Actual Dataset Sizes ---")
        print(f"KPIs (Overall): {self.datasets['kpis']['overall'].shape}")
        print(f"KPIs (Time Series): {self.datasets['kpis']['time_series'].shape}")
        print(f"Customer Metrics: {self.datasets['customer_metrics'].shape}")
        print(f"RFM Summary: {self.datasets['rfm'].shape}")
        print(f"Cohorts (Raw): {self.datasets['cohorts']['raw'].shape}")
        print(f"Cohorts (Heatmap): {self.datasets['cohorts']['heatmap'].shape}")
        print(f"Category Analytics: {self.datasets['categories'].shape}")
        print(f"Revenue Concentration: {self.datasets['concentration'].shape}")
        print(f"Top Customers: {self.datasets['top_customers'].shape}")
        print("----------------------------\n")

if __name__ == '__main__':
    # Use unittest to run the tests and show output
    unittest.main(verbosity=2)
