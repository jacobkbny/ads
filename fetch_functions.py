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


def get_campaigns(camps):
    for campaign in camps :
        # Fetch the Campaign details
        campaign.api_get(fields=[Campaign.Field.name])
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
                    print(f"Campaign: {campaign_name}, Impressions: {impressions}, Clicks: {clicks}, Spend: {spends}, Conversion: {installs}")
                    
                    
                    
def load_campaigns():
    camps = []
    In = Campaign(os.getenv("ASIA_AOS_IN_RENEW"))
    camps.append(In)
    vn = Campaign(os.getenv("ASIA_AOS_VN_renew"))
    camps.append(vn)
    id = Campaign(os.getenv("ASIA_AOS_ID_renew"))
    camps.append(id)
    ph = Campaign(os.getenv("ASIA_AOS_PH_renew"))
    camps.append(ph)
    th = Campaign(os.getenv("ASIA_AOS_TH_renew"))
    camps.append(th)
    return camps