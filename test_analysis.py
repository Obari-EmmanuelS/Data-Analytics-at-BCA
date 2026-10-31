"""Run with: python -m unittest discover -s tests -v"""
import unittest,sys,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from analyze import compute,load,summarize

class AnalyticsChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.result=compute();cls.rows=load()
    def test_unique_order_ids(self):
        self.assertEqual(len({r['order_id'] for r in self.rows}),len(self.rows))
    def test_revenue_margin_identity(self):
        x=summarize(self.rows)
        self.assertAlmostEqual(x['revenue_ngn']-x['cogs_ngn'],x['gross_profit_ngn'])
    def test_rejected_orders_have_zero_revenue(self):
        self.assertTrue(all(r['revenue_ngn']==0 for r in self.rows if r['order_status']!='Completed'))
    def test_all_reconciliations(self):
        self.assertTrue(self.result['category_revenue_total_matches'])
        self.assertTrue(self.result['monthly_revenue_total_matches'])
        self.assertTrue(self.result['segment_revenue_total_matches'])
    def test_90day_rate_bounded(self):
        self.assertGreaterEqual(self.result['metrics']['eligible_90d_repeat_rate_pct'],0)
        self.assertLessEqual(self.result['metrics']['eligible_90d_repeat_rate_pct'],100)
    def test_cleaning_actions(self):
        q=self.result['qa'];self.assertEqual(q['duplicate_order_ids_removed'],17)
        self.assertEqual(q['clean_records'],1450)
    def test_no_missing_region_channel_after_clean(self):
        self.assertTrue(all(r['region'] and r['acquisition_channel'] for r in self.rows))

if __name__=='__main__':unittest.main()
