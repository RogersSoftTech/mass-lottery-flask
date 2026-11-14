# Azure Manual Deployment Guide (No CLI Required)

This guide walks you through deploying to Azure App Service using just the Azure Portal (web interface).

---

## Step 1: Create a Resource Group

1. Go to **https://portal.azure.com**
2. Click **Resource groups** (or search for it)
3. Click **+ Create**
4. Fill in:
   - **Subscription**: Choose your free tier subscription
   - **Resource group name**: `mass-lottery-rg`
   - **Region**: `East US` (or closest to you)
5. Click **Review + create** → **Create**

**Wait for it to complete** (usually 10-20 seconds)

---

## Step 2: Create an App Service Plan

1. In Azure Portal, click **+ Create a resource**
2. Search for **App Service Plan**
3. Click **Create**
4. Fill in:
   - **Subscription**: Your free tier subscription
   - **Resource group**: Select `mass-lottery-rg` (from Step 1)
   - **Name**: `mass-lottery-plan`
   - **Publish**: **Code** (not Docker)
   - **Operating System**: **Linux** (important!)
   - **Region**: `East US` (same as resource group)
   - **Pricing plan**: Click **Change plan**
     - Select **Free F1**
     - Click **Apply**

5. Click **Review + create** → **Create**

**Wait for it to complete**

---

## Step 3: Create a Web App

1. In Azure Portal, click **+ Create a resource**
2. Search for **Web App**
3. Click **Create**
4. Fill in:
   - **Subscription**: Your free tier subscription
   - **Resource group**: Select `mass-lottery-rg`
   - **Name**: `mass-lottery-flask` (this will be your URL: `mass-lottery-flask.azurewebsites.net`)
   - **Publish**: **Code** (not Docker)
   - **Runtime stack**: **Python 3.11**
   - **Operating System**: **Linux**
   - **App Service plan**: Click **Create new**
     - Enter: `mass-lottery-plan`
     - Region: `East US`
     - Pricing plan: **Free F1**
     - Click **OK**

5. Click **Review + create** → **Create**

**Wait for deployment to complete (1-2 minutes)**

---

## Step 4: Configure Startup Command

Once deployment finishes:

1. Go to your **Web App** resource (search for `mass-lottery-flask`)
2. Click on it to open the overview
3. In the left menu, click **Configuration**
4. Click the **General settings** tab
5. Find **Startup Command** field
6. Enter:
   ```
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
7. Click **Save** at the top

**Wait for changes to take effect** (usually 1-2 minutes)

---

## Step 5: Get Your Publish Profile

1. In your **Web App** overview page, click **Download publish profile** (top right button)
2. A file called `mass-lottery-flask.publishSettings` will download
3. **Keep this file safe** - it contains your deployment credentials

---

## Step 6: Add Publish Profile to GitHub Secrets

1. Go to your GitHub repository: https://github.com/RogersSoftTech/mass-lottery-flask
2. Click **Settings** (top menu)
3. In left menu, click **Secrets and variables** → **Actions**
4. Click **New repository secret** (green button)
5. Fill in:
   - **Name**: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - **Secret**: Open the `mass-lottery-flask.publishSettings` file you downloaded
     - Copy ALL the content (the entire XML)
     - Paste it into the Secret field
6. Click **Add secret**

---

## Step 7: Deploy Your Code

Now push your code to GitHub, and it will automatically deploy:

```bash
cd C:\repos\mass-lottery-flask
git add .
git commit -m "Ready for Azure deployment"
git push origin main
```

**GitHub Actions will automatically:**
1. Build your app
2. Install dependencies from `requirements.txt`
3. Deploy to Azure

**Check deployment status:**
1. Go to your GitHub repo
2. Click **Actions** tab
3. You'll see the deployment running
4. Wait for it to complete (usually 2-3 minutes)

---

## Step 8: Test Your Deployment

Once GitHub Actions completes:

1. Open your browser and go to:
   ```
   https://mass-lottery-flask.azurewebsites.net
   ```

2. You should see the Mass Lottery app! 🎉

3. Test the API:
   ```
   https://mass-lottery-flask.azurewebsites.net/api/games
   ```
   You should see JSON with all the games.

---

## Step 9: Verify Logs (If Something Goes Wrong)

If your app doesn't work, check the logs:

1. Go to your **Web App** in Azure Portal
2. In left menu, click **App Service logs**
3. Toggle **Application logging**: ON
4. Toggle **Web server logging**: ON
5. Click **Save**

Then check logs:
1. In left menu, click **Log stream**
2. You'll see real-time logs of what's happening

---

## Troubleshooting

### App shows "Application Error"

**Solution**: Check the startup command
1. Go to **Configuration** → **General settings**
2. Make sure **Startup Command** is exactly:
   ```
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
3. Click **Save**
4. Wait 1-2 minutes, then refresh your browser

### GitHub Actions deployment failed

**Check logs**:
1. Go to your GitHub repo
2. Click **Actions** tab
3. Click on the failed workflow
4. Look for error messages
5. Common issues:
   - Publish profile secret not set correctly
   - Typo in secret name (must be `AZURE_WEBAPP_PUBLISH_PROFILE`)
   - Publish profile is outdated (download a new one)

### "502 Bad Gateway" error

**Solutions**:
1. Check startup command in Azure Portal
2. Make sure `gunicorn` is in `requirements.txt` (it is!)
3. Check logs in **App Service logs** → **Log stream**
4. Restart the app: **Restart** button in top menu

### App is very slow or times out

**Normal behavior for free tier:**
- F1 tier has limited CPU (60 min/day)
- First request after inactivity may be slow (app "wakes up")
- This is fine for a lottery app

**To improve**: Upgrade to B1 tier (costs $7.50/month)

---

## Redeploying After Code Changes

Every time you want to update your app:

```bash
# Make your changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Your change description"
git push origin main
```

GitHub Actions will automatically redeploy to Azure. Done! ✅

---

## Custom Domain (Optional)

To use your own domain instead of `mass-lottery-flask.azurewebsites.net`:

1. Go to your **Web App** in Azure Portal
2. In left menu, click **Custom domains**
3. Click **+ Add custom domain**
4. Enter your domain name (e.g., `lottery.rogers-soft-tech.com`)
5. Azure will tell you what DNS records to add
6. Go to your domain registrar (Porkbun, etc.)
7. Add the DNS records Azure shows
8. Come back to Azure and click **Validate**
9. SSL certificate is automatically created ✅

---

## Summary

| Step | What to Do | Time |
|------|-----------|------|
| 1 | Create Resource Group | 1 min |
| 2 | Create App Service Plan | 1 min |
| 3 | Create Web App | 2 min |
| 4 | Configure Startup Command | 2 min |
| 5 | Download Publish Profile | 1 min |
| 6 | Add to GitHub Secrets | 1 min |
| 7 | Push Code to GitHub | 3 min |
| 8 | Test Your App | 1 min |
| **Total** | | **15 minutes** |

---

## What's Running Now?

- **Frontend**: HTML/CSS/JavaScript (served by Flask)
- **Backend**: Python Flask app (running on Azure)
- **API**: `/api/lottery`, `/api/games` endpoints
- **Database**: None (not needed for lottery generation)
- **Cost**: $0/month (F1 free tier)

---

## Next Steps

✅ Deploy and test  
🎯 Add custom domain (optional)  
📊 Add monitoring/alerts (optional)  
📈 Scale to B1 tier if you get lots of traffic (costs money)

Enjoy your deployed Flask app! 🚀
