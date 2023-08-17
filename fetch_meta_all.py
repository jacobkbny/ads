import requests as rq
import logging
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
from week_month import week_of_month_corrected
from datetime import datetime
import time
from facebook_business.exceptions import FacebookRequestError
load_dotenv()
my_app_id = os.getenv("MY_APP_ID")
my_app_secret = os.getenv("MY_APP_SECRET")
my_access_token = os.getenv("MY_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")
sleepy_time = 300
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_'+AD_ACCOUNT_ID)
campaigns = my_account.get_campaigns()
for campaign in campaigns :
        # Fetch the Campaign details
    campaign.api_get(fields=[Campaign.Field.name])
    if str.endswith(campaign[Campaign.Field.name],"_renew"):
        print(f"Campaign ID: {campaign[Campaign.Field.id]}, Name: {campaign[Campaign.Field.name]}")
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
                if installs != 0:
                    # print(f"\tAd Set ID: {adset[AdSet.Field.id]}, Name: {adset[AdSet.Field.name]}")
                    # print(f"Impressions: {impressions}, Clicks: {clicks}, Spend: {spends}, Conversion: {installs}")
                    print((date.today() - timedelta(1)).isoformat(),campaign_name,adset[AdSet.Field.name],impressions,clicks,spends,installs)
                    # credentials = {
                    #     "type": os.getenv("CREDENTIAL_TYPE"),
                    #     "project_id": os.getenv("CREDENTIAL_PROJECT_ID"),
                    #     "private_key_id": os.getenv("CREDENTIAL_PRIVATE_KEY_ID"),
                    #     "private_key": os.getenv("CREDENTIAL_PRIVATE_KEY"),
                    #     "client_email": os.getenv("CREDENTIAL_CLIENT_EMAIL"),
                    #     "client_id": os.getenv("CREDENTIAL_CLIENT_ID"),
                    #     "auth_uri": os.getenv("CREDENTIAL_AUTH_URI"),
                    #     "token_uri": os.getenv("CREDENTIAL_TOKEN_URI"),
                    #     "auth_provider_x509_cert_url": os.getenv("CREDENTIAL_AUTH_PROVIDER_X509_CERT_URL"),
                    #     "client_x509_cert_url": os.getenv("CREDENTIAL_CLIENT_X509_CERT_URL"),
                    #     "universe_domain": os.getenv("CREDENTIAL_UNIVERSE_DOMAIN")
                    #              }
                    # gc = gspread.service_account_from_dict(credentials)
                    # spreadsheet = gc.open('Paid Report_IN')
                    # worksheet = spreadsheet.get_worksheet(5)
                    # yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%m/%d')
                    # week , month = week_of_month_corrected(yesterday_date)
                    # worksheet.append_row([week,month,(date.today() - timedelta(1)).isoformat(),"","META","Facebook Ads",campaign_name,adset[AdSet.Field.name],impressions,clicks,spends,installs])
    else :
        print("exited")
        break


