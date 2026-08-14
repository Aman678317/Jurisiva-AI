# SaaS Financial Engine & Unit Economics Test Suite

import pytest
from app.finance.financial_engine import financial_engine

def test_fin_001_gross_margin_calculation():
    margin = financial_engine.calculate_gross_margin(1000000, 100000, 80000, 20000)
    assert margin["total_cogs_inr"] == 200000
    assert margin["gross_profit_inr"] == 800000
    assert margin["gross_margin_percent"] == 80.0

def test_fin_002_cash_runway_calculation():
    runway = financial_engine.calculate_runway(12000000, 1500000, 500000)
    assert runway["net_monthly_burn_inr"] == 1000000
    assert runway["runway_months"] == 12.0

def test_fin_003_cash_flow_positive_runway():
    profitable = financial_engine.calculate_runway(5000000, 400000, 600000)
    assert profitable["net_monthly_burn_inr"] == -200000
    assert profitable["runway_months"] == 999.0
