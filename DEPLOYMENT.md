# Deployment Guide - Render

This guide will help you deploy the Contract Review & Risk Analysis Agent to Render.

## 🚀 Quick Start

### Prerequisites

1. **Render Account**: Sign up at https://render.com (free tier available)
2. **GitHub/GitLab Repository**: Push your code to a Git repository
3. **Groq API Key**: Get your free API key from https://console.groq.com/

## 📋 Deployment Steps

### Option 1: Deploy Using Render Dashboard (Recommended)

1. **Connect Your Repository**
   - Log in to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your Git repository
   - Select the repository containing this project

2. **Configure the Service**
   - **Name**: `contract-review-gradio-ui` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m app.gradio_ui`
   - **Plan**: Select `Free` (or upgrade for production)

3. **Set Environment Variables**
   - Click on "Environment" tab
   - Add the following variables:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     GROQ_MODEL=llama-3.1-8b-instant
     ```
   - Click "Save Changes"

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your application
   - Wait for the build to complete (usually 5-10 minutes)

5. **Access Your App**
   - Once deployed, you'll get a URL like: `https://contract-review-gradio-ui.onrender.com`
   - Your Gradio UI will be accessible at this URL

### Option 2: Deploy Using render.yaml (Advanced)

If you've pushed `render.yaml` to your repository:

1. **Connect Repository to Render**
   - Log in to Render dashboard
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will automatically detect `render.yaml`

2. **Configure Environment Variables**
   - Before deploying, set `GROQ_API_KEY` in Render dashboard
   - Go to your service → Environment → Add `GROQ_API_KEY`

3. **Deploy**
   - Click "Apply" to deploy all services defined in `render.yaml`

## 🔧 Configuration

### Environment Variables

Set these in Render dashboard under your service's "Environment" tab:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | - | Your Groq API key from https://console.groq.com/ |
| `GROQ_MODEL` | ❌ No | `llama-3.1-8b-instant` | Groq model to use |
| `PORT` | ❌ No | Auto | Port number (automatically set by Render) |

### Groq Model Options

- `llama-3.3-70b-versatile` - Best quality (recommended for production)
- `llama-3.1-8b-instant` - Fastest, good for development (default)
- `llama-3.2-90b-text-preview` - Very high quality
- `mixtral-8x7b-32768` - Good balance
- `gemma-7b-it` - Fast and efficient

## 📝 Deployment Checklist

- [ ] Code pushed to Git repository (GitHub/GitLab/Bitbucket)
- [ ] Render account created
- [ ] Groq API key obtained
- [ ] Web service created in Render
- [ ] Environment variables set (`GROQ_API_KEY`, `GROQ_MODEL`)
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `python -m app.gradio_ui`
- [ ] Service deployed successfully
- [ ] Application accessible via Render URL

## 🐛 Troubleshooting

### Build Fails

**Issue**: Build fails with dependency errors

**Solution**:
- Ensure `requirements.txt` is in the root directory
- Check Python version (Render uses Python 3.11+ by default)
- Review build logs in Render dashboard

### Application Won't Start

**Issue**: Service shows "Unhealthy" or won't start

**Solution**:
- Check that `GROQ_API_KEY` is set correctly
- Verify start command: `python -m app.gradio_ui`
- Check logs in Render dashboard for error messages
- Ensure port is set correctly (Render sets `PORT` automatically)

### Timeout Issues

**Issue**: Requests timeout during contract analysis

**Solution**:
- Render free tier has request timeout limits
- Consider upgrading to a paid plan for longer timeouts
- Or optimize processing time (use faster model like `llama-3.1-8b-instant`)

### Environment Variables Not Working

**Issue**: `GROQ_API_KEY not found` error

**Solution**:
- Verify environment variables are set in Render dashboard
- Ensure variable names match exactly (case-sensitive)
- Redeploy after adding environment variables

## 💰 Pricing

### Free Tier
- ✅ 750 hours/month (enough for always-on service)
- ✅ 100GB bandwidth/month
- ✅ Automatic SSL certificates
- ⚠️ Services spin down after 15 minutes of inactivity
- ⚠️ Limited request timeout

### Paid Plans
- **Starter**: $7/month - No spin-down, longer timeouts
- **Standard**: $25/month - Better performance, more resources

**Note**: For production use, consider upgrading to avoid spin-down delays.

## 🔄 Updating Your Deployment

1. **Push Changes to Git**
   ```bash
   git add .
   git commit -m "Update application"
   git push
   ```

2. **Render Auto-Deploys**
   - Render automatically detects changes
   - Triggers a new build and deployment
   - Monitor progress in Render dashboard

3. **Manual Deploy**
   - Go to Render dashboard
   - Click "Manual Deploy" → "Deploy latest commit"

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-python-apps)
- [Groq API Documentation](https://console.groq.com/docs)

## 🎉 Success!

Once deployed, your application will be available at:
`https://your-service-name.onrender.com`

You can now:
- Share the URL with others
- Use it for contract analysis
- Monitor usage in Render dashboard
- Scale up as needed

