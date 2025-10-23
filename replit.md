# AetherWave Studio

## Overview

AetherWave Studio is an AI-powered music and media generation platform with the tagline "All Intelligence is Welcome Here". It enables users to generate music through AI services, specifically integrating with the KIE.ai API (referenced as SUNO in configuration). The platform features a modern, dark-optimized creative tool aesthetic inspired by professional AI creative platforms like Runway ML, Midjourney, and ElevenLabs, aiming to provide a comprehensive creative environment for AI-generated content.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend

The frontend is built with React and TypeScript, using Vite for development. It leverages `shadcn/ui` (built on Radix UI) for components, Tailwind CSS for styling, and TanStack Query for server state management. Wouter handles client-side routing, and React Hook Form with Zod provides form handling and validation. The design emphasizes a dark-mode-first approach with a custom color palette (vibrant purple and cyan accents) and a content-first philosophy.

### Backend

The backend utilizes Express.js with TypeScript (ESM modules). It features a RESTful API, with `esbuild` for production bundling and `tsx` for development. `express-session` with PostgreSQL storage manages sessions. Key architectural decisions include a monorepo structure with shared TypeScript types, type-safe API communication, and middleware-based request logging.

### Authentication & Authorization

Authentication is handled via Replit Authentication (OpenID Connect) integrated with Passport.js. Session-based authentication uses a PostgreSQL-backed store. User profiles include basic information and a vocal gender preference. Security measures include HTTP-only, secure cookies, a 1-week session TTL, and CSRF protection.

### Data Storage

PostgreSQL, accessed via the Neon serverless driver, serves as the primary database. Drizzle ORM is used for type-safe schema definitions and push-based schema updates. The database stores user profiles, sessions, and uploaded audio files (base64 encoded) for the Cover Audio feature. UUID-based primary keys and automatic timestamp tracking are implemented.

### Credit Management & Feature Restrictions

AetherWave Studio implements a four-tier subscription model (Free, Studio, Creator, All Access) and one-time credit bundles. A centralized credit deduction system (`storage.deductCredits()`) is used for all paid services (e.g., music generation, WAV conversion), with atomic operations and plan-based unlimited access where applicable. Server-side validation and frontend filtering (`usePlanFeatures` hook) enforce feature restrictions (e.g., music models, WAV conversion, video resolution, image engines) based on the user's plan. An `UpgradeTooltip` component provides non-intrusive upgrade prompts.

## External Dependencies

### Third-Party APIs

- **KIE.ai Music Generation API (SUNO)**: The core service for AI music generation, supporting various models, vocal gender selection, instrumental/vocal modes, custom mode, and Upload & Cover Audio features. It also provides a WAV conversion feature for paid users.
- **Replit OIDC Provider**: Used for enterprise authentication via OpenID Connect, managing user logins and sessions.
- **Stripe**: Integrated for secure one-time credit purchases, handling payment intents and webhooks for adding credits to user accounts.

### Development Tools

- **Replit Vite Plugins**: Provides development-time enhancements like runtime error overlays and development mapping.
- **Google Fonts**: Utilized for various fonts including Inter, Architects Daughter, DM Sans, Fira Code, and Geist Mono.
## Environment Variables

**Required**:
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Session encryption key  
- `SUNO_API_KEY`: KIE.ai music generation API key
- `STRIPE_SECRET_KEY`: Stripe server-side API key (for payments)
- `VITE_STRIPE_PUBLIC_KEY`: Stripe publishable key (for frontend payments)

**Optional**:
- `REPLIT_DOMAINS`: Allowed domains for OIDC (required in production)
- `ISSUER_URL`: OIDC provider URL (defaults to https://replit.com/oidc)

## Recent Updates (Oct 23, 2025)

- **Stripe Payment Integration**: Added one-time credit bundle purchases powered by Stripe
  - 5 credit bundle tiers ranging from $4.99 (50 credits) to $99.99 (2000 credits + 500 bonus)
  - `/checkout` page with Stripe Elements for secure payment processing
  - `CreditBundlesModal` component for browsing and selecting bundles
  - Webhook endpoint `/api/stripe-webhook` for automatic credit addition
  - Fallback endpoint `/api/confirm-payment` for manual payment confirmation
- **Payment Flow**: User selects bundle → Redirected to checkout → Stripe payment → Credits added automatically
- **Critical Bug Fix**: Credits now deduct AFTER validation (prevents credit loss on invalid requests)
