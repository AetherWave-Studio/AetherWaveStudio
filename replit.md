# AetherWave Studio

## Overview

AetherWave Studio is an AI-powered music and media generation platform with the tagline "All Intelligence is Welcome Here". The application enables users to generate music through AI services, specifically integrating with the KIE.ai API (referenced as SUNO in configuration). The platform features a modern, dark-optimized creative tool aesthetic inspired by professional AI creative platforms like Runway ML, Midjourney, and ElevenLabs.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: React with TypeScript running on Vite
- **UI Library**: shadcn/ui components built on Radix UI primitives
- **Styling**: Tailwind CSS with custom design system using CSS variables
- **State Management**: TanStack Query (React Query) for server state
- **Routing**: Wouter for lightweight client-side routing
- **Form Handling**: React Hook Form with Zod validation

**Design System**:
- Dark-mode-first approach with optional light mode support
- Custom color palette featuring vibrant purple (primary) and cyan (secondary) accents
- Comprehensive component library with consistent styling via class-variance-authority
- Content-first philosophy putting generated media at center stage

### Backend Architecture

**Server**: Express.js with TypeScript (ESM modules)
- **API Pattern**: RESTful endpoints under `/api` prefix
- **Build System**: esbuild for production bundling, tsx for development
- **Development**: Vite integration for HMR and asset serving
- **Session Management**: express-session with PostgreSQL storage via connect-pg-simple

**Key Architectural Decisions**:
- Monorepo structure with shared TypeScript types between client and server
- Type-safe API communication using shared schemas
- Middleware-based request logging for API routes
- Raw body capture for webhook/special request handling

### Authentication & Authorization

**Provider**: Replit Authentication (OpenID Connect)
- OIDC discovery for dynamic configuration
- Passport.js strategy integration
- Session-based authentication with PostgreSQL-backed session store
- User profile includes: email, first name, last name, profile image, username
- Vocal gender preference stored per user (defaults to 'm')

**Security Considerations**:
- HTTP-only, secure cookies for session management
- 1-week session TTL
- CSRF protection through session secret
- Authentication middleware (`isAuthenticated`) guards protected routes

### Data Storage

**Database**: PostgreSQL via Neon serverless driver
- **ORM**: Drizzle ORM with type-safe schema definitions
- **Migration Strategy**: Push-based schema updates (`drizzle-kit push`)
- **Connection Pooling**: Neon serverless connection pool with WebSocket support

**Schema Design**:
- `users` table: Stores user profiles with vocal preference customization
- `sessions` table: Required for Replit Auth session persistence
- `uploaded_audio` table: Stores user-uploaded audio files for Cover Audio feature (base64-encoded)
- UUID-based primary keys with automatic generation
- Automatic timestamp tracking (createdAt, updatedAt)

**Rationale**: Neon serverless provides auto-scaling PostgreSQL without connection overhead, ideal for Replit deployments. Drizzle offers excellent TypeScript integration and flexible schema management.

**Recent Changes (Oct 23, 2025)**:
- Fixed user preference persistence bug where `/api/user/preferences` routes were accessing `req.user?.sub` instead of `req.user?.claims?.sub`
- Added file upload functionality for Cover Audio feature using multer and PostgreSQL storage
- Changed "Audio URL to Cover" from text input to file upload button with database-backed storage
- Audio files stored as base64 in PostgreSQL and served via `/api/audio/:id` endpoint
- Implemented comprehensive credit management system with three-tier monetization (Free, Studio Member $20/mo, All Access Pass $50/mo)
- Added server-side credit enforcement to all music generation endpoints
- Free users receive 50 credits daily with automatic reset after 24 hours
- Credits are deducted atomically on the server (5 credits per music generation)
- Payment modal displays upgrade options when users run out of credits
- Credits display shows real-time balance for authenticated users, hides for unauthenticated

### External Dependencies

**Third-Party APIs**:
- **KIE.ai Music Generation API** (SUNO_API_KEY): Primary music generation service
  - Supports multiple models (V3_5, V4, V4_5, V4_5PLUS, V5)
  - Vocal gender selection (male/female)
  - Instrumental/vocal mode toggle
  - Custom mode for advanced users (title, style parameters)
  - Upload & Cover Audio: Transform existing audio into new style while preserving melody
  - Advanced parameters: styleWeight, weirdnessConstraint, audioWeight
  - RESTful integration pattern with async taskId polling

**Authentication**:
- **Replit OIDC Provider**: Enterprise authentication service
  - Issuer URL: `https://replit.com/oidc` (configurable)
  - Client credentials via REPL_ID
  - Token refresh and session management

**Development Tools**:
- **Replit Vite Plugins**: Runtime error overlay, cartographer (development mapping), dev banner
- **Fonts**: Google Fonts (Inter, Architects Daughter, DM Sans, Fira Code, Geist Mono)

**Storage Abstraction**:
- `IStorage` interface allows switching between in-memory (MemStorage) and database implementations
- Currently uses in-memory storage with planned migration to Drizzle-based persistence
- Supports user CRUD operations, vocal preference updates, and credit management

### Credit Management System

**Monetization Strategy**: Three-tier subscription model
- **Free Plan**: 50 credits/day with automatic 24-hour reset, basic music generation
- **Studio Member ($20/month)**: Unlimited music credits, high-quality audio, priority generation, commercial license
- **All Access Pass ($50/month)**: Everything in Studio + unlimited video/image generation, 4K video, API access

**Credit System Architecture**:
- **Server-Side Enforcement**: All music generation endpoints (`/api/generate-music`, `/api/upload-cover-music`) require authentication and check credits before processing
- **Atomic Deduction**: 5 credits deducted per music generation, happens on server before calling external APIs
- **Daily Reset Logic**: Free users automatically receive 50 credits every 24 hours (tracked via `lastCreditReset` timestamp)
- **Plan-Based Access**: Paid users (`studio`, `all_access`) bypass credit checks and enjoy unlimited generation
- **Frontend Integration**: 
  - Real-time credits display in header for authenticated users
  - Payment modal with plan comparison shown when credits are insufficient
  - Credits automatically refresh after generation completes
  - Unauthenticated users see hidden credits indicator

**Credit Management Routes**:
- `GET /api/user/credits`: Fetch current credit balance and plan type
- `POST /api/user/credits/check-reset`: Check and execute daily reset if 24+ hours elapsed
- `POST /api/user/credits/deduct`: Manually deduct credits (internal use, mostly server-side now)

**Security Features**:
- All credit routes protected by `isAuthenticated` middleware
- Credit checks happen server-side, preventing client-side bypass
- 403 responses trigger payment modal, 401 responses hide credits display
- No path exists for unauthenticated or unpaid users to invoke generation endpoints

**Environment Requirements**:
- `DATABASE_URL`: PostgreSQL connection string (required)
- `SESSION_SECRET`: Session encryption key (required)
- `SUNO_API_KEY`: Music generation API key (required)
- `REPLIT_DOMAINS`: Allowed domains for OIDC (required in production)
- `ISSUER_URL`: OIDC provider URL (optional, defaults to Replit)