# SaaS Financial Operating Engine & Unit Economics Calculator

class SaaSFinancialEngine:
    """Calculates SaaS financial metrics: Gross Margin %, Net Monthly Burn, Cash Runway, and CAC Payback months."""

    @staticmethod
    def calculate_gross_margin(monthly_revenue_inr: float, cogs_cloud_inr: float, cogs_llm_tokens_inr: float, cogs_ocr_inr: float) -> Dict[str, Any]:
        total_cogs = cogs_cloud_inr + cogs_llm_tokens_inr + cogs_ocr_inr
        gross_profit = monthly_revenue_inr - total_cogs
        margin_percent = (gross_profit / monthly_revenue_inr * 100) if monthly_revenue_inr > 0 else 0.0

        return {
            "monthly_revenue_inr": monthly_revenue_inr,
            "total_cogs_inr": total_cogs,
            "gross_profit_inr": gross_profit,
            "gross_margin_percent": round(margin_percent, 2)
        }

    @staticmethod
    def calculate_runway(current_cash_balance_inr: float, monthly_opex_inr: float, monthly_revenue_inr: float) -> Dict[str, Any]:
        net_monthly_burn = monthly_opex_inr - monthly_revenue_inr
        if net_monthly_burn <= 0:
            runway_months = 999.0  # Profitable / Default cash-flow positive
        else:
            runway_months = current_cash_balance_inr / net_monthly_burn

        return {
            "current_cash_balance_inr": current_cash_balance_inr,
            "net_monthly_burn_inr": net_monthly_burn,
            "runway_months": round(runway_months, 1)
        }

financial_engine = SaaSFinancialEngine()
