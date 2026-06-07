# Deployment Guide - Render + Supabase

This guide walks you through deploying the Project Manager application to **Render** (for hosting) and **Supabase** (for database).

## Architecture

- **Database**: Supabase PostgreSQL (managed)
- **API**: Render Web Service (Docker)
- **MCP Server**: Render Web Service (Docker) - optional
- **Dashboard**: Render Static Site

## Prerequisites

1. [Render](https://render.com) account (free tier available)
2. [Supabase](https://supabase.com) account (free tier available)
3. Git repository pushed to GitHub/GitLab

---

## Step 1: Supabase Database Setup

### 1.1 Create Supabase Project
1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click "New Project"
3. Enter project name: `project-manager`
4. Choose a region close to your users
5. Set a secure database password (save this!)
6. Wait for project creation (~2 minutes)

### 1.2 Get Database Connection URL
1. In your Supabase project dashboard, go to **Settings** → **Database**
2. Under **Connection string**, select **URI** tab
3. Copy the connection string (starts with `postgresql://`)
4. Replace `[YOUR-PASSWORD]` with your actual database password

### 1.3 Run Migrations

You need to set up the database schema using Alembic migrations:

```bash
# Set the DATABASE_URL environment variable temporarily
$env:DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"

# Run migrations
alembic upgrade head
```

Or use the Supabase SQL Editor:
1. Go to **SQL Editor** in Supabase dashboard
2. Create a new query
3. Run the SQL from your migration files to create tables

---

## Step 2: Deploy to Render

### 2.1 Connect Repository
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **Blueprint**
3. Connect your GitHub/GitLab repository
4. Render will detect the `render.yaml` file

### 2.2 Configure Environment Variables

During deployment, Render will prompt for environment variables. Set these for each service:

#### For API Service (`project-manager-api`):
```
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

#### For MCP Server (`project-manager-mcp`) - Optional:
```
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
MCP_SERVER_NAME=project-manager
MCP_SERVER_VERSION=1.0.0
```

#### For Dashboard (`project-manager-dashboard`):
```
VITE_API_URL=https://project-manager-api.onrender.com
VITE_WS_URL=wss://project-manager-api.onrender.com/ws
```

> **Note**: Replace `project-manager-api.onrender.com` with your actual Render API URL after first deploy.

### 2.3 Deploy Services

Render will deploy services in this order:
1. **API Service** (Docker web service on port 8000)
2. **MCP Server** (Docker web service) - optional
3. **Dashboard** (Static site)

---

## Step 3: Post-Deployment

### 3.1 Update Dashboard Environment Variables

After the API service is deployed:
1. Copy the API service URL from Render dashboard
2. Go to Dashboard service → **Environment** tab
3. Update:
   - `VITE_API_URL=https://your-api-url.onrender.com`
   - `VITE_WS_URL=wss://your-api-url.onrender.com/ws`
4. Redeploy the dashboard

### 3.2 Verify Deployment

1. Visit your dashboard URL (from Render dashboard)
2. Check that WebSocket connects (status indicator in top right)
3. Verify API health: `https://your-api-url.onrender.com/health`

---

## Local Development with Production Database

To test locally using the Supabase database:

```powershell
# Copy production env
cp .env.production .env

# Edit .env with your actual Supabase credentials

# Start only the dashboard (API will use Supabase)
cd dashboard
npm install
npm run dev
```

---

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL format
- Check Supabase connection settings (IPv4/IPv6)
- Ensure password is URL-encoded if it contains special characters

### WebSocket Connection Fails
- API service must be deployed and running
- Check that VITE_WS_URL uses `wss://` not `ws://` for HTTPS
- Verify CORS origins in `src/api/main.py`

### MCP Server Not Connecting
- MCP server is optional for web dashboard
- Required only for Claude Desktop integration
- Ensure Docker is running locally for MCP

---

## Costs

### Supabase (Free Tier)
- 500MB database storage
- 2GB bandwidth/month
- Suitable for small projects

### Render (Free Tier)
- Web services: 750 hours/month (spins down after 15 min inactivity)
- Static sites: Free, always available
- Suitable for development/small production

---

## Maintenance

### Database Migrations
When you update the application schema:
1. Create new migration locally
2. Test with local database
3. Apply to Supabase before deploying code changes

### Updates
1. Push code changes to Git
2. Render automatically redeploys
3. Monitor deployment logs in Render dashboard
