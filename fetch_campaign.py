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
    print(f"Campaign ID: {campaign[Campaign.Field.id]}, Name: {campaign[Campaign.Field.name]}")