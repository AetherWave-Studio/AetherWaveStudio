/**
 * Affiliate Link Management Utility
 * 
 * This utility handles converting regular tool links to affiliate links.
 * Add your affiliate partnerships here to automatically monetize tool visits.
 */

interface AffiliateConfig {
  pattern: string | RegExp;
  convertToAffiliate: (originalUrl: string) => string;
}

// Configure your affiliate links here
const affiliateConfigs: AffiliateConfig[] = [
  // Example: Grammarly affiliate
  // {
  //   pattern: /grammarly\.com/i,
  //   convertToAffiliate: (url) => `https://www.grammarly.com/?affiliateNetwork=impact&affiliateID=YOUR_ID`
  // },

  // Example: Using impact.com or other affiliate networks
  // {
  //   pattern: /jasper\.ai/i,
  //   convertToAffiliate: (url) => `https://jasper.ai?fpr=YOUR_PARTNER_ID`
  // },

  // Example: Generic affiliate network redirect
  // {
  //   pattern: /example\.com/i,
  //   convertToAffiliate: (url) => {
  //     const encodedUrl = encodeURIComponent(url)
  //     return `https://affiliate-network.com/redirect?url=${encodedUrl}&id=YOUR_ID`
  //   }
  // },

  {
    pattern: /elevenlabs\.io/i,
    convertToAffiliate: (url) => {
      return `https://try.elevenlabs.io/5nlkb0r3t02z`
    }
  },
  {
    pattern: /pollo\.ai/i,
    convertToAffiliate: (url) => {
      return `https://pollo.ai?ref=ndk1mgu`
    }
  },
  {
    pattern: /synthesia\.io/i,
    convertToAffiliate: (url) => {
      return `https://www.synthesia.io/?via=andrew-froehlich`
    }
  }
]

/**
 * Converts a tool link to its affiliate version if configured
 * @param originalLink - The original tool website link
 * @returns The affiliate link if configured, otherwise the original link
 */
export function getAffiliateLink(originalLink: string): string {
  // Find matching affiliate config
  for (const config of affiliateConfigs) {
    const matches = typeof config.pattern === 'string' 
      ? originalLink.includes(config.pattern)
      : config.pattern.test(originalLink)
    
    if (matches) {
      try {
        return config.convertToAffiliate(originalLink)
      } catch (error) {
        console.error('Error converting to affiliate link:', error)
        return originalLink
      }
    }
  }
  
  // Return original link if no affiliate config found
  return originalLink
}

/**
 * Opens a tool link (with affiliate conversion if configured)
 * @param link - The tool's website link
 */
export function openToolLink(link: string): void {
  const affiliateLink = getAffiliateLink(link)
  window.open(affiliateLink, '_blank', 'noopener,noreferrer')
}
