# Azure Deployment Guide for Mass Lottery Flask App

## What You Need

This is a **Python Flask backend application**, not a static web app. It needs a server that runs 24/7.

| Service | Use Case |
|---------|----------|
| Azure Static Web Apps | ❌ NOT for this (frontend only) |
| Azure App Service (F1 Free) | ✅ YES - FREE tier for Python backends |
| Azure Container Instances | ✅ Also good but more complex |
| Azure Functions | ❌ Not ideal (lottery generation needs resources) |

---

## Step-by-Step Deployment

### 1. Create Azure App Service

```bash
# Login to Azure
az login

# Create resource group
az group create --name mass-lottery-rg --location eastus

# Create App Service Plan (F1 = FREE tier, includes Linux support)
az appservice plan create \
  --name mass-lottery-plan \
  --resource-group mass-lottery-rg \
  --sku F1 \
  --is-linux

# Create Web App for Python
az webapp create \
  --resource-group mass-lottery-rg \
  --plan mass-lottery-plan \
  --name mass-lottery-flask \
  --runtime "PYTHON|3.11"
```

Or use **Azure Portal**:
1. Create Resource → App Service
2. Choose **Linux** (not Windows)
3. Python 3.11
4. **F1 (Free)** pricing tier - $0/month ✅

### 2. Configure Startup Command in Azure Portal

Navigate to: **App Service** → **Configuration** → **General Settings**

Set **Startup Command**:
```
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Set **Stack**: Python 3.11

### 3. Get Your Publish Profile

In Azure Portal:
1. Go to your **App Service**
2. Click **Download publish profile** (top right)
3. This is an XML file with deployment credentials

### 4. Add Publish Profile to GitHub Secrets

In your GitHub repository:
1. **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
4. Value: (paste the entire XML from the publish profile)

### 5. The GitHub Actions Workflow

The workflow file `.github/workflows/azure-deploy.yml` is already created and will:
- Trigger on every push to `main`
- Install Python 3.11 and dependencies
- Deploy to Azure App Service
- Use the publish profile secret

### 6. Deploy!

Just push to main:
```bash
git add .
git commit -m "Add Azure deployment configuration"
git push origin main
```

GitHub Actions will automatically:
- Build your app
- Test it (optional)
- Deploy to Azure App Service

Check the **Actions** tab in GitHub to see deployment progress.

---

## Verify Your Deployment

Once deployed, test the API:

```bash
# Replace with your actual app name
curl -X POST https://mass-lottery-flask.azurewebsites.net/api/lottery \
  -H "Content-Type: application/json" \
  -d '{"game":"millionaire_for_life","consecutive_pairs":1}'
```

Expected response:
```json
{
  "game": "millionaire_for_life",
  "game_name": "Millionaire For Life",
  "numbers": [12, 13, 34, 41, 48],
  "bonus": {"name": "Lucky Ball", "value": 7},
  "bonus_color": "#047841",
  "consecutive_pairs": 1
}
```

---

## View Live Logs

```bash
# Real-time logs from Azure
az webapp log tail --resource-group mass-lottery-rg --name mass-lottery-flask

# Or in Azure Portal:
# App Service → Log stream
```

---

## Environment Variables (If Needed Later)

In Azure Portal → **Configuration** → **Application settings**:

Add new settings like:
- `FLASK_ENV` = `production`
- `FLASK_DEBUG` = `false`

---

## Custom Domain (Optional)

To use your own domain instead of `.azurewebsites.net`:

1. In Azure Portal → **Custom domains**
2. Add your domain
3. Azure will give you DNS records to add to your domain registrar
4. Free SSL certificate automatically included

---

## Pricing

- **F1 App Service Plan**: **$0/month (FREE!)** ✅
- **Custom domain with SSL**: Free (automatic)
- **Database (if added)**: $5-100+/month
- **Total**: Starting at $0/month

---

## Troubleshooting

### App won't start
```bash
# Check logs
az webapp log tail --resource-group mass-lottery-rg --name mass-lottery-flask

# Common issues:
# - Missing startup command
# - requirements.txt not found
# - Python version mismatch
```

### Deployment fails from GitHub Actions
1. Check that publish profile secret is set
2. Re-download publish profile if it's old
3. Check GitHub Actions logs for errors

### 502 Bad Gateway
- Check startup command is correct
- Make sure `gunicorn` is in requirements.txt
- View logs to see what failed

---

## Next Steps

1. ✅ Create App Service (done via CLI or Portal)
2. ✅ Add publish profile to GitHub secrets
3. ✅ Push `.github/workflows/azure-deploy.yml` to main
4. ✅ Watch GitHub Actions deploy automatically
5. ✅ Test your app at `https://mass-lottery-flask.azurewebsites.net`
6. ✅ (Optional) Add custom domain
7. ✅ (Optional) Set up monitoring/alerts

---

## Comparison with Firebase (Your Old Setup)

| Feature | Firebase Hosting | Azure App Service (F1 Free) |
|---------|---|---|
| Cost | $1-100+ | $0/month |
| Deployment | Firebase CLI | GitHub Actions |
| Backend logic | Limited | Full Python |
| Database | Firestore ($$$) | Much cheaper options |
| Custom domain | Included | Included |
| SSL/HTTPS | Automatic | Automatic |
| Scalability | Auto | Manual scaling options |

---

## Questions?

See:
- Azure App Service docs: https://learn.microsoft.com/en-us/azure/app-service/
- Flask deployment: https://flask.palletsprojects.com/en/2.3.x/deploying/
- GitHub Actions: https://docs.github.com/en/actions
