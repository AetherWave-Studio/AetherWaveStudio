# AetherWave Studio Deployment Checklist

## Environment Variables Setup (Vercel)

Before deploying, ensure these environment variables are configured in your Vercel project settings:

### Required API Keys

1. **OPENAI_API_KEY**
   - Get from: https://platform.openai.com/api-keys
   - Used for: Chat API and Album Art generation (DALL-E)
   - Required for: `/api/chat` and `/api/generate-art`

2. **ANTHROPIC_API_KEY** (Optional)
   - Get from: https://console.anthropic.com/
   - Used for: Alternative chat provider (Claude)
   - Required for: `/api/chat` with `provider: 'anthropic'`

3. **SUNO_API_KEY**
   - Get from: https://kie.ai/ (SUNO API via KIE.AI)
   - Used for: Music generation
   - Required for: `/api/generate-music`

### Setting Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to: **Settings** → **Environment Variables**
3. Add each variable:
   - Variable Name: `OPENAI_API_KEY`
   - Value: `sk-...your-key...`
   - Environment: Select **Production**, **Preview**, and **Development**
4. Click **Save**
5. Repeat for all required keys

## CORS Configuration Check

CORS is already configured in:
- `vercel.json` (lines 13-35)
- Each API file (`api/chat.js`, `api/generate-music.js`, `api/generate-art.js`)

### Verify CORS Headers

The following headers are set:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET,POST,OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

## Testing Before Deployment

### 1. Test Locally (if using Vercel CLI)

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to project directory
cd E:/Gits/AetherWaveStudio

# Create .env file for local testing
echo "OPENAI_API_KEY=your-key" > .env
echo "SUNO_API_KEY=your-key" >> .env

# Run local development server
vercel dev
```

### 2. Browser Console Checks

Open browser DevTools (F12) and check:

- **No CORS errors** when making API calls
- **Character counter works** when typing in Song Description field
- **All form fields populate correctly**:
  - Song Description
  - Custom Lyrics (optional)
  - Genre dropdown
  - Model Version dropdown
  - Instrumental checkbox

### 3. API Endpoint Tests

Test each endpoint manually:

#### Chat API
```bash
curl -X POST https://your-domain.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "provider": "openai"}'
```

Expected response:
```json
{
  "message": "...",
  "provider": "openai",
  "model": "gpt-4o-mini"
}
```

#### Music Generation API
```bash
curl -X POST https://your-domain.vercel.app/api/generate-music \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "uplifting synthwave track",
    "genre": "synthwave",
    "model": "V5",
    "instrumental": false
  }'
```

Expected response:
```json
{
  "audioUrl": "...",
  "imageUrl": "...",
  "title": "...",
  "duration": 180,
  "taskId": "..."
}
```

#### Album Art API
```bash
curl -X POST https://your-domain.vercel.app/api/generate-art \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "neon cityscape",
    "style": "cyberpunk"
  }'
```

Expected response:
```json
{
  "imageUrl": "...",
  "prompt": "...",
  "style": "cyberpunk",
  "revisedPrompt": "..."
}
```

## Common Errors and Solutions

### CORS Errors

**Error:**
```
Access to fetch at 'https://...' from origin '...' has been blocked by CORS policy
```

**Solution:**
1. Verify `vercel.json` contains CORS headers
2. Check that API files return CORS headers in responses
3. Ensure OPTIONS requests are handled (preflight)

### API Key Not Configured

**Error:**
```json
{ "error": "SUNO API key not configured" }
```

**Solution:**
1. Add the missing environment variable in Vercel dashboard
2. Redeploy after adding variables

### Character Counter Not Working

**Error:**
```
Cannot read properties of null (reading 'textContent')
```

**Solution:**
Already fixed in latest code (E:\Gits\AetherWaveStudio\index.html:686-690)

### Music Generation Timeout

**Error:**
```json
{ "error": "Music generation timeout" }
```

**Solution:**
1. Check `vercel.json` maxDuration is set to 60s for `generate-music.js`
2. SUNO API may be slow - this is expected for complex generations
3. Consider implementing webhook callbacks for long-running tasks

## Deployment Steps

### Deploy to Vercel

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Navigate to project**:
   ```bash
   cd E:/Gits/AetherWaveStudio
   ```

4. **Deploy**:
   ```bash
   vercel --prod
   ```

5. **Or use GitHub integration**:
   - Push code to GitHub
   - Import project in Vercel dashboard
   - Vercel will auto-deploy on every push to main branch

## Post-Deployment Verification

### 1. Check All Pages Load
- [ ] Landing page (index.html) loads correctly
- [ ] No 404 errors in console
- [ ] All CSS and fonts load properly

### 2. Test Each Feature
- [ ] Chat panel sends messages and receives responses
- [ ] Music generation panel accepts input
- [ ] Album art panel accepts input
- [ ] Character counter updates in real-time
- [ ] Model version dropdown works
- [ ] Instrumental checkbox toggles
- [ ] Custom lyrics field is optional

### 3. Monitor Vercel Logs
```bash
vercel logs <deployment-url>
```

Look for:
- API key configuration confirmations
- SUNO API responses
- Any error messages

### 4. Performance Check
- [ ] Page loads in < 3 seconds
- [ ] API responses are reasonable
- [ ] No memory leaks in long sessions

## API Rate Limits

Be aware of rate limits for each service:

### OpenAI
- Free tier: Very limited
- Pay-as-you-go: Based on usage
- Monitor at: https://platform.openai.com/usage

### SUNO (via KIE.AI)
- Check your plan limits at: https://kie.ai/
- V5 model is fastest
- Up to 8-minute tracks

### Best Practices
- Implement request queuing for high traffic
- Add user-facing rate limit messages
- Consider caching common requests

## Security Notes

✅ **Good Practices Already Implemented:**
- API keys stored in environment variables (not in code)
- CORS configured to allow browser access
- Input validation on all API endpoints
- Rate limiting checks (character limits)

⚠️ **Consider Adding:**
- User authentication for production
- Request rate limiting per IP
- API key rotation schedule
- Error message sanitization (don't expose internal details)

## Monitoring and Maintenance

### Vercel Analytics
Enable in: Project Settings → Analytics

### Error Tracking
Consider adding:
- Sentry for error tracking
- LogRocket for session replay
- Custom logging dashboard

### Regular Checks
- [ ] Weekly: Check API usage and costs
- [ ] Monthly: Rotate API keys
- [ ] Monthly: Review error logs
- [ ] Quarterly: Update dependencies

---

## Quick Reference

**Project Root:** `E:\Gits\AetherWaveStudio`

**Key Files:**
- `index.html` - Main landing page
- `vercel.json` - Vercel configuration
- `api/chat.js` - Chat API endpoint
- `api/generate-music.js` - Music generation endpoint
- `api/generate-art.js` - Album art endpoint

**Vercel Dashboard:** https://vercel.com/dashboard

**Support Links:**
- Vercel Docs: https://vercel.com/docs
- OpenAI API Docs: https://platform.openai.com/docs
- KIE.AI Docs: https://kie.ai/docs
- Anthropic Docs: https://docs.anthropic.com/

---

Last Updated: 2025-10-17
