# Affiliate Links Setup Guide

Your AIverse site now has a centralized affiliate link management system that automatically converts tool links to affiliate links when users click "Visit" buttons.

## How It Works

All tool links are processed through a single utility file: `src/utils/affiliateLinks.ts`

When a user clicks any "Visit" or "Explore" button, the link is automatically checked against your affiliate configurations and converted if a match is found.

## Adding Affiliate Links

Edit `src/utils/affiliateLinks.ts` and add your affiliate configurations to the `affiliateConfigs` array.

### Example 1: Simple Domain Match

```typescript
{
  pattern: /grammarly\.com/i,
  convertToAffiliate: (url) => `https://www.grammarly.com/?affiliateID=YOUR_AFFILIATE_ID`
}
```

### Example 2: Preserve Original URL Parameters

```typescript
{
  pattern: /jasper\.ai/i,
  convertToAffiliate: (url) => {
    const urlObj = new URL(url)
    urlObj.searchParams.set('fpr', 'YOUR_PARTNER_ID')
    return urlObj.toString()
  }
}
```

### Example 3: Using Affiliate Network Redirect

```typescript
{
  pattern: /midjourney\.com/i,
  convertToAffiliate: (url) => {
    const encodedUrl = encodeURIComponent(url)
    return `https://impact.com/redirect?campaignId=YOUR_CAMPAIGN_ID&url=${encodedUrl}`
  }
}
```

### Example 4: String Pattern Match

```typescript
{
  pattern: 'copy.ai',
  convertToAffiliate: (url) => `https://www.copy.ai/?via=YOUR_REF_CODE`
}
```

## Popular Affiliate Networks

### Impact.com
```typescript
{
  pattern: /example\.com/i,
  convertToAffiliate: (url) => {
    return `https://example.com?irclickid=YOUR_TRACKING_ID`
  }
}
```

### ShareASale
```typescript
{
  pattern: /example\.com/i,
  convertToAffiliate: (url) => {
    return `https://www.shareasale.com/r.cfm?b=BANNER_ID&u=USER_ID&m=MERCHANT_ID&urllink=${encodeURIComponent(url)}`
  }
}
```

### CJ Affiliate (Commission Junction)
```typescript
{
  pattern: /example\.com/i,
  convertToAffiliate: (url) => {
    return `https://www.anrdoezrs.net/click-YOUR_PID/YOUR_DESTINATION_URL`
  }
}
```

### PartnerStack / First Promoter
```typescript
{
  pattern: /example\.com/i,
  convertToAffiliate: (url) => {
    return `${url}?ref=YOUR_REFERRAL_CODE`
  }
}
```

## Performance

- **Zero page load impact**: Link conversion happens instantly on click
- **Centralized management**: Update all affiliate links in one file
- **Fallback safe**: If conversion fails, original link is used
- **No external dependencies**: Pure JavaScript, no tracking pixels or scripts

## Testing Affiliate Links

1. Add your configuration to `affiliateLinks.ts`
2. Save the file (dev server auto-reloads)
3. Click a tool's "Visit" button
4. Check the opened URL in the browser address bar
5. Verify it includes your affiliate parameters

## Tracking Conversions

Most affiliate networks provide:
- Click tracking via unique IDs in the URL
- Conversion tracking via cookies
- Dashboard for monitoring performance

Make sure your affiliate network can track conversions from your domain: `ai-hub.aetherwavestudio.com`

## Best Practices

1. **Test before deploying**: Always verify links open correctly
2. **Disclose affiliate relationships**: Add a disclosure page (legally required in many jurisdictions)
3. **Monitor performance**: Track which tools generate the most revenue
4. **Keep it updated**: Regularly check that affiliate programs are still active
5. **User experience first**: Ensure links always work, even if affiliate conversion fails

## Common Patterns

### Pattern 1: Add Query Parameter
```typescript
convertToAffiliate: (url) => `${url}${url.includes('?') ? '&' : '?'}ref=YOUR_CODE`
```

### Pattern 2: Replace Domain
```typescript
convertToAffiliate: (url) => url.replace('example.com', 'partner.example.com/YOUR_ID')
```

### Pattern 3: Subdomain Redirect
```typescript
convertToAffiliate: (url) => {
  const urlObj = new URL(url)
  urlObj.hostname = `YOUR_ID.${urlObj.hostname}`
  return urlObj.toString()
}
```

## Need Help?

- Check your affiliate program's documentation for the correct link format
- Test in incognito mode to verify cookie tracking works
- Use browser dev tools to inspect the actual URL being opened
