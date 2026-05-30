# Discord Bot Setup Guide
This guide explains how to create a Discord application, configure the bot, and invite it to your server.

## Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)

   ![developer-portal-home](https://cdn.discordapp.com/attachments/1510281058594062376/1510372232457748601/1hmz3sk.png?ex=6a1c9341&is=6a1b41c1&hm=eaffcab248d416086a66a37769454ddda6995416c4f96d903e56e3cbc62ebfd4&)
You should now see something similar to the image below.

2. Click **New Application**.

   ![create-application](https://cdn.discordapp.com/attachments/1510281058594062376/1510373617492426933/6q893sz.png?ex=6a1c948b&is=6a1b430b&hm=474e7a877bf0c3c82c9d19ac3108432a52126178ceac3cd18c9d149cc5cf9a82&)

3. Enter a name for your application

## Configure the Bot
   ![bot-tab-settings](https://cdn.discordapp.com/attachments/1510281058594062376/1510374762633756872/vk2z6qw.png?ex=6a1c959c&is=6a1b441c&hm=8b17d49b2ad8e0c8f6499397a9a1ffa0b3e1fa5c78f7d02e0ca3fb18fe4ecb18&)

Click the **Bot** tab.

   ![bot-tab-portal-home](https://cdn.discordapp.com/attachments/1510281058594062376/1510376450681868398/rwdszw4.png?ex=6a1c972f&is=6a1b45af&hm=94eb95b84f6b779b73407437ec4edc783d5f31215d233b28295dc832191c094b&)
Customize your bot by adding an icon, banner, and username.

Enable the following required intents:

- Presence Intent
- Server Members Intent
- Message Content Intent

Return to the sidebar and click the **OAuth2** tab. Scroll down until you see the following page:

   ![oauth2-bot-scope](https://cdn.discordapp.com/attachments/1510281058594062376/1510378241762791514/7b33hf7.png?ex=6a1c98da&is=6a1b475a&hm=89a82a6d390ad3b9e46a79dc4d9b288d7d77540df2c3459411609c89a27cebfa&)
  Select the scope **Bot**

   ![oauth2-permissions](https://cdn.discordapp.com/attachments/1510281058594062376/1510379142539903126/s2qs84v.png?ex=6a1c99b1&is=6a1b4831&hm=19e7136924d753dcd13151c03a392a66dfd036a97904c2f577256ad4b17e91f5&)

Grant the following permissions:
- Send Messages
- Manage Messages
- Kick Members
- Ban Members
- View Audit Log
- Moderate Members
- Manage Server
- Use Slash Commands

## Invite the Bot
First, store your Discord bot token in a `.env` file so the bot can come online.

⚠️ Never share your Discord bot token with anyone.

Anyone with your token can control your bot and perform actions using its permissions.

Your `.env` file should look like this:
`DISCORD_TOKEN=YOUR_TOKEN HERE`

Discord will generate an invite URL. Open the URL in your browser and select the server where you want to add the bot.

## Support the Project 

If you enjoy this project, consider supporting it:

[![YouTube](https://img.shields.io/badge/YouTube-Brentley%20the%20Dev-red?logo=youtube)](https://www.youtube.com/@BrentleytheDev)
[![X](https://img.shields.io/badge/X-@BrentleytheDev-black?logo=x&logoColor=white)](https://x.com/BrentleytheDev)
