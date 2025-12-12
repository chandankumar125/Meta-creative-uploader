# campaigns.py
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi

def create_campaign(ad_account_id, access_token, campaign_name, objective, campaign_budget=None):
    """
    Creates a Facebook campaign.
    Supports both CBO (campaign-level budget) AND adset-level budget.

    campaign_budget = None → adsets will use their OWN budgets
    campaign_budget = value → campaign will use CBO
    """
    
    FacebookAdsApi.init(access_token=access_token)

    params = {
        "access_token": access_token,
        "name": campaign_name,
        "objective": objective,
        "status": "PAUSED",
    }

    # Enable Campaign Budget Optimization (CBO)
    if campaign_budget:
        params["daily_budget"] = int(campaign_budget)
        params["is_campaign_budget_optimization"] = True

    account = AdAccount(f"act_{ad_account_id}")
    return account.create_campaign(params=params)
