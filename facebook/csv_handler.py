import pandas as pd
import io
from .ads import create_campaign, create_adset, create_creative, create_ad
from .auth import get_access_token

# AD_ACCOUNT_ID should ideally be dynamic.
AD_ACCOUNT_ID = "1324697116076599"

def clean_id(value):
    """Cleans ID strings by removing prefixes like 'tp:', 'v:', etc."""
    if pd.isna(value):
        return None
    return str(value).split(':')[-1]

def map_objective(objective):
    """Maps CSV objective names to API constants."""
    mapping = {
        "Outcome Sales": "OUTCOME_SALES",
        # Add other mappings as needed
    }
    return mapping.get(objective, "OUTCOME_SALES") # Default or error?

async def process_csv(file):
    access_token = get_access_token()
    if not access_token:
        return [{"error": "No access token found. Please login via /facebook/auth/login first.", "status": "failed"}]

    # Ensure we are at the start of the file
    await file.seek(0)
    content = await file.read()
    
    # Use pandas to read the CSV content
    # Using 'utf-8' encoding and handling potential errors if needed, but pandas is usually good.
    # If the user had issues with Google Sheets, we can try to decode first or just pass bytes.
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        # Fallback: try decoding with errors='ignore' if direct bytes fail (rare for pd.read_csv but possible with bad encodings)
        decoded = content.decode("utf-8", errors="ignore")
        df = pd.read_csv(io.StringIO(decoded))

    results = []
    
    # Track created IDs to avoid duplicates if multiple rows belong to same campaign/adset
    # Structure: {campaign_name: {id: campaign_id, adsets: {adset_name: adset_id}}}
    created_structure = {}

    for index, row in df.iterrows():
        try:
            # --- Campaign ---
            campaign_name = row.get("Campaign Name")
            if not campaign_name:
                continue # Skip empty rows

            if campaign_name not in created_structure:
                campaign_id = create_campaign(
                    access_token=access_token,
                    account_id=AD_ACCOUNT_ID,
                    name=campaign_name,
                    objective=map_objective(row.get("Campaign Objective"))
                )
                created_structure[campaign_name] = {"id": campaign_id, "adsets": {}}
            else:
                campaign_id = created_structure[campaign_name]["id"]

            # --- Ad Set ---
            adset_name = row.get("Ad Set Name")
            if adset_name not in created_structure[campaign_name]["adsets"]:
                # Budget: CSV might be in dollars, API needs cents.
                daily_budget = row.get("Ad Set Daily Budget", 0)
                if pd.notna(daily_budget):
                    daily_budget = int(float(daily_budget) * 100)
                
                pixel_id = clean_id(row.get("Optimized Conversion Tracking Pixels"))
                
                adset_id = create_adset(
                    access_token=access_token,
                    account_id=AD_ACCOUNT_ID,
                    name=adset_name,
                    daily_budget=daily_budget,
                    optimization_goal=row.get("Optimization Goal", "OFFSITE_CONVERSIONS"), # Default?
                    pixel_id=pixel_id,
                    campaign_id=campaign_id,
                    start_time=row.get("Ad Set Time Start"),
                    end_time=row.get("Ad Set Time Stop")
                )
                created_structure[campaign_name]["adsets"][adset_name] = adset_id
            else:
                adset_id = created_structure[campaign_name]["adsets"][adset_name]

            # --- Creative ---
            ad_name = row.get("Ad Name")
            page_id = clean_id(row.get("Campaign Page ID"))
            video_id = clean_id(row.get("Video ID"))
            image_hash = row.get("Image Hash") # Assuming this is already a hash or URL we treat as hash for now based on previous code
            
            creative_id = create_creative(
                access_token=access_token,
                account_id=AD_ACCOUNT_ID,
                ad_name=ad_name,
                image_hash=image_hash,
                video_id=video_id,
                primary_text=row.get("Body"),
                headline=row.get("Title"),
                call_to_action=row.get("Call to Action"),
                website_url=row.get("Link"),
                page_id=page_id
            )

            # --- Ad ---
            ad_id = create_ad(
                access_token=access_token,
                account_id=AD_ACCOUNT_ID,
                ad_name=ad_name,
                adset_id=adset_id,
                creative_id=creative_id
            )

            results.append({
                "row_index": index,
                "campaign_name": campaign_name,
                "ad_name": ad_name,
                "campaign_id": campaign_id,
                "adset_id": adset_id,
                "creative_id": creative_id,
                "ad_id": ad_id,
                "status": "success"
            })

        except Exception as e:
            results.append({
                "row_index": index,
                "error": str(e),
                "status": "failed"
            })

    return results
