# yahoo_fantasy
Generates interesting stats from a Yahoo Fantasy football league using yfpy

# Yahoo Fantasy app setup
 Create a Yahoo developer app at https://developer.yahoo.com/apps/. I used the following parameters
 - **Application name**: yfpy
 - **Description**: track stats for fantasy football
 - **Homepage URL**: [blank]
 - **Redirect URI(s)**: https://localhost:8080
 - **OAuth Client Type**: Confidential Client
 - **API Permissions**: Fantasy Sports - Read

 The Client ID (Consumer Key) and Client Secret (Consumer Secret) are always available to copy from the app page after you create it. Create a `.env` file in a folder named `env` and add `YAHOO_CONSUMER_KEY` and `YAHOO_CONSUMER_SECRET` entries.