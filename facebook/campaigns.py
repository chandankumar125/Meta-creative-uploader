from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi

def create_campaign(ad_account_id, access_token, name, objective):
    FacebookAdsApi.init(access_token=access_token)
    
    params = {
        "name": name,
        "objective": objective,
        "status": "PAUSED"   # Recommended
    }

    account = AdAccount(f"act_{ad_account_id}")
    return account.create_campaign(params=params)
