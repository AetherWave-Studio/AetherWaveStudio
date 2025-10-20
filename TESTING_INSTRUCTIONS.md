# Video Generation Testing Instructions

## Quick Test

### Option 1: Use Test Suite (Automated)

1. Deploy to Vercel or access your deployed site
2. Navigate to: `https://aetherwavestudio.com/test-video-generation.html`
3. Click **"🚀 Test All 8 Use Cases"** button
4. Wait ~5 minutes for all tests to complete
5. Review results and videos

### Option 2: Manual Testing on Main Site

1. Go to `https://aetherwavestudio.com/`
2. Find **🎬 AI Media Generator** panel
3. Click **Video** button
4. Click each use case card and test:

#### Test Checklist

- [ ] **Band Profile** - Portrait photography
- [ ] **Live Photos** - Concert photography
- [ ] **Live Video** - Performance footage
- [ ] **Production Video** - Music video
- [ ] **Backstage Pass** - BTS content
- [ ] **On The Road** - Tour scenes
- [ ] **Album Art** - Animated cover
- [ ] **News Reports** - Press announcements

### Expected Results

✅ **Success Criteria:**
- Video generates in 20-60 seconds
- Video URL returned immediately
- Video plays in browser
- 720p resolution, 5 seconds duration
- Matches use case prompt template

❌ **Common Issues:**

**"Fal.ai API key not configured"**
- Solution: Add `FAL_KEY` to Vercel env vars

**"Failed to generate video"**
- Check Fal.ai credits/quota
- Try disabling safety checker
- Check browser console for errors

**Video too slow**
- Expected: 20-60 seconds for 720p
- Use "lite" model for faster generation
- Lower resolution to 512p if needed

## Testing Each Use Case

### 1. Band Profile 👤
```
Prompt: "Professional artist portrait photography: indie rock band in urban setting. Studio lighting, high quality, detailed, press kit worthy, promotional photo style."
Expected: Professional looking artist portraits
```

### 2. Live Photos 🎸
```
Prompt: "Live concert photography: rock band performing on stage with dramatic lighting. Dynamic stage lighting, energetic performance, crowd atmosphere, professional music photography."
Expected: Dynamic concert photography feel
```

### 3. Live Video 🎤
```
Prompt: "Live concert performance: energetic band performing with dynamic camera angles. Stage lights, live music energy, performance intensity, concert film quality."
Expected: Concert footage with energy
```

### 4. Production Video 🎬
```
Prompt: "Professional music video production: cinematic shots of band in moody urban environment. Cinematic camera work, artistic storytelling, high-quality cinematography, music video style."
Expected: Cinematic music video quality
```

### 5. Backstage Pass 🎭
```
Prompt: "Behind-the-scenes music photography: band relaxing in green room with instruments. Candid backstage moments, authentic artist life, documentary photography style."
Expected: Candid, authentic BTS feel
```

### 6. On The Road 🚐
```
Prompt: "Tour life photography: band on tour bus traveling through scenic landscape. Travel documentary style, authentic road moments, touring musician lifestyle."
Expected: Travel/tour documentary vibe
```

### 7. Album Art 💿
```
Prompt: "Album cover art design: abstract geometric shapes in vibrant neon colors. Square format, artistic composition, professional album artwork, high-quality graphic design."
Expected: Abstract artistic animation
```

### 8. News Reports 📰
```
Prompt: "Music news press image: band announcement with professional presentation. Professional news photography, press release quality, announcement graphic style."
Expected: Press/news style imagery
```

## Performance Benchmarks

| Model | Resolution | Duration | Avg Time | Cost |
|-------|-----------|----------|----------|------|
| Lite | 512p | 5s | 15-25s | ~$0.03 |
| Lite | 720p | 5s | 25-40s | ~$0.05 |
| Lite | 1080p | 5s | 45-70s | ~$0.08 |
| Pro | 720p | 5s | 35-55s | ~$0.10 |

## Troubleshooting

### Test Suite Not Loading
- Check that file is deployed to Vercel
- Verify API endpoint `/api/generate-video-fal` exists
- Check browser console for errors

### All Tests Failing
- Verify `FAL_KEY` environment variable is set
- Check Fal.ai account has credits
- Try manual test on main site first

### Some Tests Pass, Some Fail
- Could be prompt safety issues
- Try disabling safety checker
- Some prompts may trigger content filters

### Videos Generate But Don't Play
- Check video URL is accessible
- Verify CORS headers are correct
- Try downloading video instead

## Next Steps After Testing

1. **If all tests pass**: Deploy to production ✅
2. **If some fail**: Review failed prompts and adjust
3. **Performance issues**: Switch to lite model or lower resolution
4. **Quality issues**: Try pro model with higher resolution

## Report Issues

If you encounter issues:
1. Note which use case failed
2. Copy the full error message
3. Check Vercel function logs
4. Check Fal.ai dashboard for API errors
5. Report to: support@aetherwavestudio.com

---

**Last Updated**: 2025-01-19
**Test Suite**: `test-video-generation.html`
