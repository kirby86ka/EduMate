# Deploy AdaptLearn to Vercel

This guide explains how to deploy your AdaptLearn platform to Vercel with both the FastAPI backend and React frontend.

## Prerequisites

- A [Vercel account](https://vercel.com/signup) (free tier works)
- Your project pushed to GitHub, GitLab, or Bitbucket
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Quick Deploy

### Method 1: GitHub Integration (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration from `vercel.json`

3. **Set Environment Variables**
   In the Vercel project settings, add:
   - `GEMINI_API_KEY` - Your Google Gemini API key
   - `SESSION_SECRET` - A secure random string (e.g., generate with `openssl rand -base64 32`)

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your app automatically

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy (from project root)
vercel

# Add environment variables
vercel env add GEMINI_API_KEY
vercel env add SESSION_SECRET

# Deploy to production
vercel --prod
```

## How It Works

### Project Structure for Vercel

```
your-project/
├── api/                    # Backend (FastAPI serverless functions)
│   ├── index.py           # Serverless function handler
│   └── requirements.txt   # Python dependencies
├── app/                   # Your FastAPI application code
│   ├── main.py
│   └── ...
├── frontend/              # React frontend
│   ├── src/
│   ├── dist/             # Built files (auto-generated)
│   └── vite.config.js
├── package.json          # Node dependencies & build scripts
├── vercel.json           # Vercel configuration
└── .vercelignore         # Files to exclude from deployment
```

### What Happens During Deployment

1. **Frontend Build**: Vercel runs `npm run build` to create optimized React files
2. **Backend Setup**: FastAPI is deployed as a serverless function at `/api/*`
3. **Routing**: All API requests go to `/api/*`, frontend routes to React app
4. **Static Files**: React build files are served via Vercel's Edge Network (CDN)

## API Routes

Once deployed, your API will be available at:

- `https://your-app.vercel.app/api/subjects`
- `https://your-app.vercel.app/api/assessment/start`
- `https://your-app.vercel.app/api/assessment/next-question`
- etc.

Frontend automatically detects Vercel deployment and uses relative URLs.

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` |
| `SESSION_SECRET` | Secret for session management | `random-secure-string` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ADMIN_API_KEY` | Admin API authentication | `admin-key-123` |
| `AI_API_KEY` | AI agent authentication | `ai-key-456` |

## Automatic Deployments

Once connected to GitHub:
- **Every push to `main`** → Automatic production deployment
- **Every pull request** → Preview deployment with unique URL
- **Rollback** → One-click rollback to any previous deployment

## Testing Your Deployment

After deployment, test these endpoints:

```bash
# Replace YOUR_APP_URL with your Vercel URL
curl https://YOUR_APP_URL/api/subjects
curl https://YOUR_APP_URL/
```

## Troubleshooting

### Issue: "Serverless Function has crashed"
**Solution**: Check Vercel logs in Dashboard → Deployments → Your deployment → Logs

### Issue: API calls fail with CORS errors
**Solution**: FastAPI CORS is configured to allow all origins. Check browser console for actual error.

### Issue: Frontend shows blank page
**Solution**: 
1. Check build logs in Vercel dashboard
2. Ensure `npm run build` works locally
3. Verify `frontend/dist` directory is created

### Issue: Environment variables not working
**Solution**:
1. Go to Vercel Dashboard → Project Settings → Environment Variables
2. Add variables for Production, Preview, and Development
3. Redeploy the application

## Monitoring & Logs

- **Deployment Logs**: Vercel Dashboard → Deployments → Your deployment
- **Runtime Logs**: Vercel Dashboard → Deployments → Your deployment → Logs
- **Analytics**: Vercel Dashboard → Analytics (Pro plan feature)

## Cost

- **Free Tier**: 
  - 100GB bandwidth/month
  - 100 hours serverless execution/month
  - Unlimited deployments
  - Perfect for demos and small projects

- **Upgrade**: Consider Pro plan for:
  - More bandwidth
  - Advanced analytics
  - Team collaboration

## Custom Domain

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. SSL certificate is automatically provisioned

## Performance Tips

1. **Enable Caching**: API responses can be cached using Vercel's Edge Network
2. **Use Edge Functions**: Consider upgrading critical endpoints to Edge Functions
3. **Optimize Images**: Use Vercel's Image Optimization (requires Pro plan)
4. **Monitor**: Check Vercel Analytics to identify slow endpoints

## Next Steps

- Set up custom domain
- Configure preview deployments for testing
- Add Vercel Analytics
- Set up error monitoring (Sentry integration)
- Configure CI/CD workflows

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI on Vercel](https://vercel.com/docs/frameworks/backend/fastapi)
- [React on Vercel](https://vercel.com/docs/frameworks/frontend/vite)
