# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

AetherWave Audio Player is a web-based music streaming showcase for the track "You Didn't Need to Bring Him" by Ghosts Online. This is a single-page application built with vanilla HTML, CSS, and JavaScript that integrates with multiple music platforms (Spotify, Apple Music, YouTube Music) and provides download functionality.

## Architecture

### Single-Page Application Structure
The application is built as a single HTML file (`index.html`) with embedded styles and JavaScript. It follows a component-based design within the HTML structure:

- **Main Container**: `#wrapper` → `#main` → `.inner` - provides responsive layout structure
- **Music Player Interface**: Two main embed sections (`#embed01`, `#embed02`) containing:
  - Hero section with album cover and track information
  - Call-to-action buttons for streaming platforms
  - Embedded Spotify and YouTube iframes
  - Download modal with email gate functionality

### Key Components

#### Email Gate System
- **Modal Interface**: Accessible modal dialog for email collection
- **Toggle System**: `EMAIL_GATE_ENABLED` flag allows bypassing email requirement
- **Download Flow**: Validates email → triggers direct download
- **External Integration**: Supports Netlify proxy for email collection (via `PROXY_URL`)

#### Platform Integration
- **Spotify Embed**: Direct iframe integration for track playback
- **YouTube Embed**: Direct iframe integration for music video
- **Platform Links**: Direct links to Spotify, Apple Music, and YouTube Music
- **Schema.org Metadata**: Structured data for music recording information

#### Responsive Design
- **CSS Custom Properties**: Extensive use of CSS variables for theming
- **Mobile-First**: Responsive breakpoints from 360px to 1920px
- **Device Detection**: JavaScript client detection for iOS/Android optimizations
- **Touch Support**: Special handling for touch devices

## Development Workflows

### Local Development
```powershell
# Start local development server (any method)
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (if you have http-server installed)
npx http-server

# Navigate to http://localhost:8000
```

### File Structure
```
AudioWave-Player - gitpush/
├── index.html                 # Main application file
├── Audiowave-Player-copy.html # Enhanced version with Netlify integration
├── index.back.html            # Backup version with debug features
├── downloads/
│   └── ghosts-online.mp3     # Audio file for direct download
├── .netlify/
│   ├── netlify.toml          # Netlify configuration
│   └── state.json            # Netlify state file
├── _headers                  # Netlify headers configuration
├── _redirects               # Netlify redirects configuration
└── .gitignore              # Git ignore rules
```

### Deployment with Netlify

#### Configuration Files
- **netlify.toml**: Main Netlify configuration with custom headers for downloads
- **_headers**: HTTP headers for proper MP3 file serving with download attribute
- **_redirects**: SPA routing configuration (all routes → index.html)

#### Environment Setup
The application supports different configurations:
- **Email Gate**: Toggle via `EMAIL_GATE_ENABLED` JavaScript constant
- **Download URLs**: Configurable via `DOWNLOAD_URL` constant
- **Proxy Integration**: External email collection via `PROXY_URL`

### Content Management

#### Music Track Updates
To update the featured track, modify these elements in `index.html`:
1. **Track Title**: Update `h1` text content
2. **Album Art**: Replace `img src` URLs for cover images
3. **Platform URLs**: Update Spotify, Apple Music, YouTube Music links
4. **Embed Codes**: Replace iframe `src` attributes for Spotify/YouTube
5. **Schema.org Data**: Update structured data in JSON-LD script
6. **Download File**: Replace MP3 file in `/downloads/` directory

#### Styling Customization
The application uses CSS custom properties for consistent theming:
- **Color Scheme**: Dark theme with purple/pink accent colors
- **Brand Colors**: `--accent: #ff2a9e` (AetherWave Pink)
- **Responsive Variables**: Automatic viewport height and background adjustments
- **Component Styling**: Modular CSS for buttons, modals, and layouts

### Testing & Debugging

#### Local Testing
```powershell
# Test download functionality
# Ensure downloads/ directory contains the correct MP3 file
# Test modal functionality in browser dev tools
# Verify responsive design across different screen sizes
```

#### Platform Integration Testing
- **Spotify**: Verify embed iframe loads and plays correctly
- **YouTube**: Confirm video embed functionality
- **External Links**: Test all platform redirect URLs
- **Mobile Testing**: Test touch interactions and responsive layout

#### Email Gate Testing
The application includes debug functionality:
- Toggle `EMAIL_GATE_ENABLED` to test both direct download and email gate flows
- Use browser dev tools to inspect network requests for email submission
- Test modal accessibility features (keyboard navigation, screen readers)

## Important Implementation Details

### JavaScript Architecture
- **Vanilla JavaScript**: No external dependencies or frameworks
- **Event-Driven**: Uses addEventListener for clean event handling
- **Modular Functions**: Separate functions for download, modal, toast, and platform detection
- **Error Handling**: Comprehensive error handling for network requests and user interactions

### Accessibility Features
- **ARIA Labels**: Proper aria-hidden, aria-labelledby attributes
- **Keyboard Navigation**: Full keyboard support for modals and forms
- **Semantic HTML**: Proper heading hierarchy and form structure
- **Focus Management**: Automatic focus handling for modal interactions

### Performance Optimizations
- **Lazy Loading**: Iframe loading optimization
- **CSS Optimization**: Minimal, inline CSS for fastest loading
- **Image Optimization**: External CDN for album artwork
- **Script Loading**: Inline JavaScript eliminates additional HTTP requests

### External Dependencies
- **Dropbox**: Primary storage for album artwork
- **Google Cloud Storage**: Alternative download source
- **Netlify Functions**: Email collection proxy (optional)
- **Platform Embeds**: Spotify and YouTube iframe embeds

## Browser Support
- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile Support**: iOS Safari, Android Chrome
- **Legacy Support**: Basic functionality for older browsers
- **Feature Detection**: JavaScript client detection for browser-specific optimizations
i need to add this navigation at the top of the page 
<nav class="aether-nav">
  <ul>
    <li><a href="https://player.aetherwavestudio.com/" target="_blank">Global Playlist</a></li>
    <li><a class="active" href="#">Featured Artist</a></li>
    <li><a href="https://docs.google.com/forms/d/e/1FAIpQLSfHYRDb7iRmNFIneGJNsEhQ1wpi5QQYbXKy9mwFUMP4htvOoQ/viewform?usp=header" target="_blank">Submit Music</a></li>
    <li><a href="https://theme-packs.aetherwavestudio.com/" target="_blank">Theme Collections</a></li>
    <li><a href="https://aetherwavestudio.com/" target="_blank">Custom Music</a></li>
    <li><a href="https://privacy.aetherwavestudio.com/" target="_blank">Privacy</a></li>
  </ul>
</nav>
