import requests
import json

# --------------------------
# 1. Create Campaign
# --------------------------
def create_campaign(access_token, account_id, name, objective, special_ad_categories=None):
    """
    Create a Facebook campaign.
    special_ad_categories: list, required by Meta API even if empty.
    """
    if not account_id.startswith('act_'):
        account_id = f"act_{account_id}"

    if special_ad_categories is None:
        special_ad_categories = []

    url = f"https://graph.facebook.com/v21.0/{account_id}/campaigns"
    payload = {
        "access_token": access_token,
        "name": name,
        "objective": objective,
        "status": "PAUSED",
        "special_ad_categories": json.dumps(special_ad_categories)
    }
    
    print(f"DEBUG - Creating campaign with payload: {payload}")
    res = requests.post(url, data=payload).json()
    print(f"DEBUG - Response: {res}")
    if "error" in res:
        raise Exception(f"Error creating campaign: {res['error']['message']}")
    return res["id"]


# --------------------------
# 2. Create Ad Set
# --------------------------
def create_adset(access_token, account_id, name, daily_budget,
                 optimization_goal, pixel_id, campaign_id, start_time, end_time):
    if not account_id.startswith('act_'):
        account_id = f"act_{account_id}"
    url = f"https://graph.facebook.com/v21.0/{account_id}/adsets"

    payload = {
        "access_token": access_token,
        "name": name,
        "daily_budget": int(daily_budget),
        "billing_event": "IMPRESSIONS",
        "optimization_goal": optimization_goal,
        "campaign_id": campaign_id,
        "promoted_object": {"pixel_id": pixel_id},
        "start_time": start_time,
        "end_time": end_time,
        "status": "PAUSED"
    }

    res = requests.post(url, data=payload).json()
    if "error" in res:
        raise Exception(f"Error creating adset: {res['error']['message']}")
    return res["id"]


# --------------------------
# 3. Create Creative
# --------------------------
def create_creative(access_token, account_id, ad_name, image_hash, video_id,
                    primary_text, headline, call_to_action, website_url, page_id):
    if not account_id.startswith('act_'):
        account_id = f"act_{account_id}"
    url = f"https://graph.facebook.com/v21.0/{account_id}/adcreatives"

    link_data = {
        "message": primary_text,
        "headline": headline,
        "call_to_action": {"type": call_to_action, "value": {"link": website_url}}
    }

    if video_id:
        link_data["video_id"] = video_id
    elif image_hash:
        link_data["image_hash"] = image_hash
    else:
        raise Exception("Either image_hash or video_id must be provided")

    payload = {
        "access_token": access_token,
        "name": ad_name,
        "object_story_spec": {
            "page_id": page_id,
            "link_data": link_data
        }
    }

    res = requests.post(url, json=payload).json()
    if "error" in res:
        raise Exception(f"Error creating creative: {res['error']['message']}")
    return res["id"]


# --------------------------
# 4. Create Ad
# --------------------------
def create_ad(access_token, account_id, ad_name, adset_id, creative_id):
    if not account_id.startswith('act_'):
        account_id = f"act_{account_id}"
    url = f"https://graph.facebook.com/v21.0/{account_id}/ads"

    payload = {
        "access_token": access_token,
        "name": ad_name,
        "adset_id": adset_id,
        "creative": {"creative_id": creative_id},
        "status": "PAUSED"
    }

    res = requests.post(url, data=payload).json()
    if "error" in res:
        raise Exception(f"Error creating ad: {res['error']['message']}")
    return res["id"]
