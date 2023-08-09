import requests
import sys
sys.path.append("/opt/homebrew/lib/python3.11/site-packages")
sys.path.append("/opt/homebrew/lib/python3.11/site-packages/facebook_business-17.0.2.dist-info")
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.adobjects.adset import AdSet
from datetime import date, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
from .week_month import week_of_month_corrected
from datetime import datetime
load_dotenv()
my_app_id = os.getenv("MY_APP_ID")
my_app_secret = os.getenv("MY_APP_SECRET")
my_access_token = os.getenv("MY_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")


FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

my_account = AdAccount('act_'+AD_ACCOUNT_ID)
#     campaign.remote_read(fields=[Campaign.Field.name])
#     if str.startswith(campaign[Campaign.Field.name],"ASIA_AOS"):
#         print(f"Campaign ID: {campaign[Campaign.Field.id]}, Name: {campaign[Campaign.Field.name]}")

# campaigns = my_account.get_campaigns()

# for campaign in campaigns :
campaign = Campaign(os.getenv("ASIA_AOS_IN_NEW")) #ASIA_AOS_IN_NEW
        # Fetch the Campaign details
campaign.remote_read(fields=[Campaign.Field.name])

    # print(f"Campaign ID: {campaign[Campaign.Field.id]}, Name: {campaign[Campaign.Field.name]}")
if str.startswith(campaign[Campaign.Field.name],"ASIA_AOS"):
    campaign_name = campaign[Campaign.Field.name]
            # Get the Ad Sets of the Campaign
    adsets = campaign.get_ad_sets(fields=[AdSet.Field.name])

            # For each Ad Set, get the insights
    for adset in adsets:
        params = {
                    'time_range': {
                        'since': (date.today() - timedelta(1)).isoformat(),
                        'until': (date.today() - timedelta(1)).isoformat(),
                    },
                }
        insights = adset.get_insights(params=params, fields=[AdsInsights.Field.impressions, AdsInsights.Field.clicks, AdsInsights.Field.spend, AdsInsights.Field.actions])
        if insights:
            impressions = insights[0][AdsInsights.Field.impressions] if AdsInsights.Field.impressions in insights[0] else 0
            clicks = insights[0][AdsInsights.Field.clicks] if AdsInsights.Field.clicks in insights[0] else 0
            spends = insights[0][AdsInsights.Field.spend] if AdsInsights.Field.spend in insights[0] else 0
            conversions = insights[0][AdsInsights.Field.actions] if AdsInsights.Field.actions in insights[0] else 0
            installs = 0
            for conversion in conversions:
                if conversion['action_type'] == 'mobile_app_install':
                    installs = int(conversion['value'])
                #\t\t
            if installs != 0:
                    # print(f"\tAd Set ID: {adset[AdSet.Field.id]}, Name: {adset[AdSet.Field.name]}")
                    # print(f"Impressions: {impressions}, Clicks: {clicks}, Spend: {spends}, Conversion: {installs}")
                print((date.today() - timedelta(1)).isoformat(),campaign_name,adset[AdSet.Field.name],impressions,clicks,spends,installs)
                credentials = {
                        "type": os.getenv("CREDENTIAL_TYPE"),
                        "project_id": os.getenv("CREDENTIAL_PROJECT_ID"),
                        "private_key_id": os.getenv("CREDENTIAL_PRIVATE_KEY_ID"),
                        "private_key": os.getenv("CREDENTIAL_PRIVATE_KEY"),
                        "client_email": os.getenv("CREDENTIAL_CLIENT_EMAIL"),
                        "client_id": os.getenv("CREDENTIAL_CLIENT_ID"),
                        "auth_uri": os.getenv("CREDENTIAL_AUTH_URI"),
                        "token_uri": os.getenv("CREDENTIAL_TOKEN_URI"),
                        "auth_provider_x509_cert_url": os.getenv("CREDENTIAL_AUTH_PROVIDER_X509_CERT_URL"),
                        "client_x509_cert_url": os.getenv("CREDENTIAL_CLIENT_X509_CERT_URL"),
                        "universe_domain": os.getenv("CREDENTIAL_UNIVERSE_DOMAIN")}
                gc = gspread.service_account_from_dict(credentials)
                spreadsheet = gc.open('ReachOutTracker')
                worksheet = spreadsheet.get_worksheet(1)
                yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%m/%d')
                week , month = week_of_month_corrected(yesterday_date)
                worksheet.append_row([week,month,(date.today() - timedelta(1)).isoformat(),campaign_name,adset[AdSet.Field.name],impressions,clicks,spends,installs])
            

# for campaign in campaigns :
#     campaign.remote_read(fields=[Campaign.Field.name])
#     if str.startswith(campaign[Campaign.Field.name],"ASIA_AOS"):
#         print(f"Campaign ID: {campaign[Campaign.Field.id]}, Name: {campaign[Campaign.Field.name]}")


# print(campaigns)
# camp = Campaign('23855434919500430')
# camp.remote_read(fields=[Campaign.Field.name])
# print(camp[Campaign.Field.name])
# print("Ad Set",camp.get_ad_sets())
# insights = camp.get_insights()
# print(insights)
# print("item",insights.get_one())
# print(campaigns)




