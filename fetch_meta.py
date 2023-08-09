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
                # credentials = {
                #         "type": "service_account",
                #         "project_id": "emailtracker-393823",
                #         "private_key_id": "dd5891be6a27a0282bf76dda9401affb1ffb397e",
                #         "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDVU/zf2Im3AIyH\neBxQWDnBKS97DfSJ8DP9bHqck+o8Y8a5XNosmv7wP/dgEyyPsPXy8b968Ot3NTva\n2NYUFrKI6Y7hMuyDnn08YWz185dlvjK9BSAD8ldx3OiXnAnzIWf/FrEzwrGpToLu\n61QCrldvfxGBIKPGSitlHnk+SgfGi2UY6QHUFLyvKPB2wxrmF4dDRI7AmIsS8GRh\nkiNu1hHs2lqncT7ZWdT5oYjlGajATuqLRWLgpnODtjU7S4yxgCtMuk+GdqX7rSLe\nW/ddE3Hls9hmZ1LwibLOOVa7Uia8Sm6XLGSxoSAC3NyFmQZoxHWwVyTaNJA+Lzb0\nQtm1jxTZAgMBAAECggEACt0jmBy1arHm9jEqM/dCPbGEvv4HcYzfgOzo05d+ysOE\nB8WQQMxF5mNDjEt9rfWjmNMx3qdtPl1iJnN7d3tubSWDxrkqrUtBcnU9sMrOb3p/\np/ueVUUeqehHmgzyvsR5QNbdgFbOaGJcraEjXp2VS1LLx+krHfqB+jzSjNcFTVmN\nJtczibX8hNqj6AnCqd6Fm7zTNqN2CJH6K4iobLDWFW03Nnr0g02l6Oqf1A4Qg3Si\nIbzYu7SopM9/BidGzi6e/1IUoC6/AO1APvU6tlj+i9Huqf71flYCyOd703GDuh5M\nCEFbneC7xmssJCWFJTE5AirIroBttgVY3rH3sn3qlwKBgQDtefn5hwS9LijbJAId\n38cps7Vb+ZT9kOx8ayWN1uSy7Sa44adrujkQv3VeD8YPwb2fviuOG0NoiNscCx6k\nc6f+PRBEV/1hmmPhJNaRL5PgmF7RLWKGo4e6tbYPyHCxCMmwbvLKTb60ObjL99IQ\noNqbsCpBhByRyQN/oiFdZTu1KwKBgQDl986E6eHXyI2VGUBXELtBHzs2CkUfINSP\nrODLVhxXuunZ3dxPl7HMMxMkm0UOlI0a6MrxdFGkgWwomB/yhenhgxkTtr+XKzqE\nLDvnTZ8Z41Qlt9buBysSwcc4JoPKfMXNpbisW/UCkwe3yF3kMwp5SQWWua+Bs8uT\na4hHAezkCwKBgHFWW7V5eQuI8jrUTqZPXNBMUmwZC8CQ4CzpPj0ZqIC0qlxmZe8G\nK6IQnkVMJezzPDr3GfZykJNdbaVOsUsvX6f5IMBddjKU6sJTQIx+NodkcSxICtPT\nTD4R51hVA2OanBe2e+2NeUyul8HQ/tKs0minhSNLmA8D7sWFbYMTg5GNAoGAWBti\nR3AoM/lFrWs4SGNDqwahM+opY2y7o7RTh/Qc9cvKDsu+vcvbteWXnv3SLmzhxv6L\nyoiLQyDG5KKsEsoVum307KWmr+9DAyLDbLJDk7KSKcVOlnGuoggWIMA43BqD2m90\n2qx8qZjVaydcObMIf0Fn38CSqnnNNFUNqE7niNMCgYEA3SYVgw5sx+b9EHuKxUxj\njKEytOVlc19mn5qzFhN0/pOxkEV2r5bo7Z0USWQdAk7QqxyO9FsA/O8zaqTXXExt\nlMM1YB0GVELJ09N7htsBsxuPbEf0seELeMTnKcMNuRobketyoUeKDMLYmZkUuXyF\nSAYDhZco+1XBj/ZQ3ULIJx4=\n-----END PRIVATE KEY-----\n",
                #         "client_email": "emailtracker@emailtracker-393823.iam.gserviceaccount.com",
                #         "client_id": "118034276744647254656",
                #         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                #         "token_uri": "https://oauth2.googleapis.com/token",
                #         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                #         "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/emailtracker%40emailtracker-393823.iam.gserviceaccount.com",
                #         "universe_domain": "googleapis.com"}
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




