# AetherWave Studio - Video Generation System

## Overview

AetherWave Studio features an AI-powered video generation system using **Fal.ai Seedance 1.0** for creating professional music videos, live performance clips, album art animations, and promotional content.

---

## Features

### 8 Music Industry Use Cases

1. **Band Profile** - Professional artist photos for press kits
2. **Live Photos** - Dynamic concert photography
3. **Live Video** - Concert performance footage
4. **Production Video** - Cinematic music videos
5. **Backstage Pass** - Behind-the-scenes content
6. **On The Road** - Tour life and travel scenes
7. **Album Art** - Animated album artwork
8. **News Reports** - Press-style announcement visuals

### Smart Prompt System

Each use case has optimized prompt templates that automatically enhance your creative vision:

```javascript
// Example: Band Profile
"Professional artist portrait photography: {your vision}.
Studio lighting, high quality, detailed, press kit worthy, promotional photo style."
```

### Image-to-Video Modes

- **First Frame**: Image becomes opening frame, AI animates from there
- **Reference**: AI uses image as style inspiration (supports 1-4 images)

### Advanced Settings

- **Quality**: Fast (Lite Model) or High Quality (Pro Model)
- **Resolution**: 512p, 720p, or 1080p
- **Duration**: 5 seconds or 10 seconds
- **Safety Checker**: Optional content safety filter

---

## Setup

### 1. Get Fal.ai API Key

Sign up at [https://fal.ai](https://fal.ai) and get your API key from the dashboard.

### 2. Set Environment Variables

In **Vercel Project Settings > Environment Variables**, add:

```
FAL_KEY=your_fal_ai_key_here
```

**Optional** (for image-to-video features):
```
IMGBB_API_KEY=your_imgbb_key_here
IMGUR_CLIENT_ID=your_imgur_client_id_here
```

### 3. Deploy

Push to your Vercel-connected GitHub repo or run:

```bash
vercel --prod
```

---

## How It Works

### Frontend Flow

1. User selects **Image** or **Video** media type
2. User clicks a **use case card** (e.g., "Live Photos")
3. AI generates **enhanced prompt** based on template
4. User can customize prompt and add images
5. Click **Generate** → Video returns in ~30 seconds

### Backend Flow

```
Frontend → /api/generate-video-fal → Fal.ai Seedance API → Video URL
```

**Synchronous Response** - No polling needed! Fal.ai returns video URL immediately when generation completes.

---

## API Endpoint

### `POST /api/generate-video-fal`

**Request Body:**

```json
{
  "prompt": "Professional artist portrait photography: indie rock band. Studio lighting.",
  "modelVersion": "lite",      // "lite" or "pro"
  "resolution": "720p",         // "512p", "720p", "1080p"
  "duration": "5",              // "5" or "10" (seconds)
  "enableSafetyChecker": true,
  "imageData": "data:image/png;base64,...",  // Optional
  "imageMode": "first-frame"    // Optional: "first-frame" or "reference"
}
```

**Response:**

```json
{
  "status": "complete",
  "videoUrl": "https://fal.media/files/...",
  "model": "fal-ai/bytedance/seedance/v1/lite/text-to-video",
  "seed": 12345,
  "timings": {
    "inference": 28000  // milliseconds
  }
}
```

---

## Use Case Examples

### Example 1: Live Concert Footage

**Use Case**: Live Video
**Prompt**: `Live concert performance: rock band performing on stage with dramatic purple lighting and enthusiastic crowd. Dynamic camera angles, stage lighting effects.`
**Settings**: 720p, Pro Model, 10 seconds

### Example 2: Band Promo Photo

**Use Case**: Band Profile
**Prompt**: `Professional artist portrait photography: 4-piece indie band in urban alley wearing leather jackets. Moody lighting, cinematic.`
**Settings**: 1080p, Pro Model, 5 seconds

### Example 3: Animated Album Art

**Use Case**: Album Art
**Upload**: Square album cover image
**Mode**: First Frame
**Prompt**: `Animated album artwork: geometric shapes pulsing to beat. Abstract, vibrant colors.`
**Settings**: 720p, Lite Model, 5 seconds

---

## Troubleshooting

### "Fal.ai API key not configured"

- Check that `FAL_KEY` is set in Vercel Environment Variables
- Redeploy after adding the key

### "Image upload failed"

- Add `IMGBB_API_KEY` or `IMGUR_CLIENT_ID` to environment variables
- Or provide image URL directly instead of uploading

### "Video generated but no URL returned"

- Check Vercel function logs for full response
- May indicate Fal.ai API response format changed
- Report to support@fal.ai with request ID

### Videos not generating

- **Check API credits**: Log into Fal.ai dashboard
- **Check prompt safety**: Disable safety checker if getting false rejections
- **Try lower resolution**: Start with 512p Lite model for faster/cheaper testing

---

## Cost Optimization

### Fal.ai Pricing (as of 2025)

- **Lite Model**: ~$0.05 per 5-second video
- **Pro Model**: ~$0.10 per 5-second video
- **Resolution multipliers**: 1080p costs ~2x more than 720p

### Tips to Reduce Costs

1. **Start with Lite Model** - Test prompts before using Pro
2. **Use 5-second duration** - 10s costs 2x more
3. **Use 720p** - Sweet spot for quality vs cost
4. **Batch similar prompts** - Reuse seeds for variations

---

## Legacy Code (Removed)

Previously, the system supported **KIE.AI Seedance** with async webhooks and polling. This has been removed in favor of Fal.ai's simpler synchronous API.

**Files No Longer Needed:**
- `/api/generate-video.js` - KIE.AI implementation
- `/api/video-status.js` - Polling endpoint
- `/api/video-callback.js` - Webhook handler
- `/api/video-store.js` - In-memory cache

You can safely delete these files.

---

## Future Enhancements

- [ ] Image generation (static album art)
- [ ] Batch video generation
- [ ] Video style transfer
- [ ] Custom model fine-tuning
- [ ] Video-to-video editing
- [ ] Multi-clip stitching for full music videos

---

## Support

- **Fal.ai Docs**: https://fal.ai/docs
- **Seedance 1.0 Model**: https://fal.ai/models/bytedance/seedance
- **AetherWave Support**: support@aetherwavestudio.com

---

**Last Updated**: 2025-01-19
**Claude Code**: Implemented video generation system with use-case-based workflow
