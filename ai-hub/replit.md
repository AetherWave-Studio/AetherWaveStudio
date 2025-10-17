# AIverse - Replit Project Documentation

## Project Overview
AIverse is a comprehensive AI tools directory application featuring 1000+ AI tools across multiple categories. The application allows users to discover, search, filter, and explore various AI tools with features like ratings, recommendations, and user authentication.

**Last Updated**: October 3, 2025

## Technology Stack
- **Frontend Framework**: React 18.3.1 with TypeScript
- **Build Tool**: Vite 6.2.6
- **Styling**: Tailwind CSS v3.4.16
- **UI Library**: Radix UI components + shadcn/ui
- **Backend/Database**: Supabase (PostgreSQL + Authentication)
- **Package Manager**: pnpm
- **Routing**: React Router v6
- **Node Version**: Node.js 20

## Project Structure
```
/
├── aiverse/              # Main application directory
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Route pages (HomePage, AboutPage, etc.)
│   │   ├── hooks/        # Custom hooks (useAuth, useMobile)
│   │   ├── lib/          # Utilities and Supabase client
│   │   └── main.tsx      # Application entry point
│   ├── public/           # Static assets and logo files
│   ├── package.json      # Dependencies and scripts
│   └── vite.config.ts    # Vite configuration
├── supabase/             # Database migrations and functions
├── data/                 # JSON data files
├── code/                 # Python scripts for data processing
└── docs/                 # Documentation
```

## Replit Setup

### Workflow Configuration
- **Name**: AIverse Frontend
- **Command**: `cd aiverse && pnpm run dev`
- **Port**: 5000
- **Type**: Webview (frontend)
- **Status**: Active and running

### Vite Configuration
The Vite config has been properly configured for Replit's proxy environment:
- Server host: `0.0.0.0` (binds to all interfaces)
- Server port: `5000`
- HMR client port: `443` (for Replit's proxy)

This configuration is **critical** for the application to work in Replit's iframe-based preview.

### Deployment Configuration
- **Target**: Autoscale (stateless web application)
- **Build Command**: `cd aiverse && pnpm install && pnpm run build:prod`
- **Run Command**: `cd aiverse && pnpm install && pnpm run preview --host 0.0.0.0 --port 5000`

## Key Features
1. **Tool Discovery**: Browse 1000+ AI tools with pagination
2. **Search & Filter**: Advanced search with category filtering
3. **Recommendations**: Daily tool recommendations
4. **User Features**: Authentication, favorites, tool submissions
5. **Accessibility**: Dark mode, high contrast mode
6. **Responsive Design**: Mobile-friendly interface

## Database Schema (Supabase)
- `tools` - AI tool listings with metadata
- `categories` - Tool categories
- `profiles` - User profiles
- `user_favorites` - User favorite tools
- `user_submissions` - User-submitted tools pending approval

## Development Commands
```bash
# Install dependencies
cd aiverse && pnpm install

# Start dev server
cd aiverse && pnpm run dev

# Build for production
cd aiverse && pnpm run build

# Production build (with BUILD_MODE=prod)
cd aiverse && pnpm run build:prod

# Preview production build
cd aiverse && pnpm run preview
```

## Known Issues
- Some external tool logos may return 404 errors (non-critical)
- WebSocket HMR warnings in Replit environment (expected, doesn't affect functionality)
- LSP diagnostics for React imports (doesn't affect runtime)

## Recent Changes
- **Oct 3, 2025**: Initial Replit setup
  - Installed Node.js 20
  - Configured Vite for Replit proxy (host, port, HMR)
  - Created .gitignore
  - Set up workflow for frontend dev server
  - Configured deployment settings
  - Created README.md and replit.md

## Environment Variables
Supabase credentials are currently hardcoded in `src/lib/supabase.ts`:
- Supabase URL: `https://ncfqyasvfvrtpoaqfegl.supabase.co`
- Supabase Anon Key: (public key, safe to expose)

For production, consider moving to environment variables.

## Important Notes
- Always use pnpm (not npm or yarn)
- Port 5000 is the only allowed frontend port in Replit
- The Vite config must maintain host: '0.0.0.0' for Replit preview to work
- HMR is configured for Replit's HTTPS proxy (clientPort: 443)

## Future Considerations
- Add environment variable support for Supabase credentials
- Implement additional tool submission moderation features
- Add analytics for tool popularity tracking
- Consider adding tool comparison features
