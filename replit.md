# AI Music and Media Maker

## Overview

This is an AI-powered music and media creation application built with a modern full-stack architecture. The application provides a creative tool interface for generating and managing AI-created music and media content, inspired by professional creative tools like Runway ML, Midjourney, and ElevenLabs.

The project uses a monorepo structure with a React frontend and Express backend, connected via a REST API architecture. It's designed to support creative workflows with minimal friction while maintaining professional polish.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: React 18 with TypeScript
- **Routing**: Wouter (lightweight client-side routing)
- **State Management**: TanStack Query (React Query) for server state
- **UI Framework**: Shadcn UI components built on Radix UI primitives
- **Styling**: Tailwind CSS with custom design system
- **Build Tool**: Vite

**Design System**:
- Dark-optimized interface as primary theme with light mode support
- Content-first approach putting generated media at center stage
- Color palette featuring vibrant purple primary (creative energy) and cyan accents (tech sophistication)
- Custom CSS variables for consistent theming across light/dark modes
- Component system from Shadcn UI (40+ pre-built accessible components)

**Key Frontend Patterns**:
- Path aliases for clean imports (`@/`, `@shared/`, `@assets/`)
- Custom hooks for common functionality (mobile detection, toast notifications)
- Query client with configured defaults (no refetch on window focus, infinite stale time)
- Form validation with React Hook Form and Zod resolvers

### Backend Architecture

**Framework**: Express.js with TypeScript
- **Runtime**: Node.js with ESM modules
- **Database ORM**: Drizzle ORM
- **Session Storage**: PostgreSQL-based sessions (connect-pg-simple)
- **Development**: tsx for TypeScript execution

**API Design**:
- RESTful API with `/api` prefix for all endpoints
- JSON request/response format
- Request logging with duration tracking
- Raw body capture for webhook support

**Storage Pattern**:
- Interface-based storage abstraction (`IStorage`)
- In-memory implementation (`MemStorage`) for development
- Designed to swap to database-backed implementation
- CRUD methods: `getUser`, `getUserByUsername`, `createUser`

### Data Storage

**Database**: PostgreSQL via Neon serverless
- **ORM**: Drizzle ORM with PostgreSQL dialect
- **Schema Definition**: Type-safe schema in `shared/schema.ts`
- **Migrations**: Drizzle Kit for schema migrations (output to `./migrations`)
- **Connection**: WebSocket-based serverless connection via `@neondatabase/serverless`

**Current Schema**:
- `users` table with UUID primary key, username (unique), and password fields
- Zod validation schemas for insert operations
- Type inference for compile-time safety

**Design Rationale**:
- Serverless PostgreSQL chosen for scalability and zero-config deployment
- Drizzle ORM provides type-safe queries without code generation overhead
- Schema-first approach with validation ensures data integrity

### Authentication & Authorization

**Current State**: Basic user model implemented, authentication not yet fully configured
- User schema includes username and hashed password fields
- Session store configured for PostgreSQL via `connect-pg-simple`
- Ready for session-based authentication implementation

**Planned Approach**:
- Session-based authentication (configured but not implemented)
- Password hashing (schema ready, implementation needed)
- Express session middleware (dependencies installed)

### External Dependencies

**Third-Party Services**:
- Neon Database: Serverless PostgreSQL hosting
- Google Fonts: Typography (DM Sans, Geist Mono, Fira Code, Architects Daughter)

**Key Libraries**:
- **UI Components**: Radix UI primitives (40+ component packages)
- **Form Handling**: React Hook Form with Zod validation
- **Styling**: Tailwind CSS with autoprefixer
- **Date Utilities**: date-fns
- **State Management**: TanStack Query
- **Icons**: Lucide React
- **Development**: Replit plugins (vite-plugin-runtime-error-modal, cartographer, dev-banner)

**Build & Development Tools**:
- Vite: Frontend build tool and dev server
- esbuild: Backend bundler for production
- TypeScript: Type safety across stack
- Drizzle Kit: Database schema management

**Design Philosophy**:
- Shadcn UI approach: Components are copied into codebase rather than installed as dependencies
- This allows full customization while maintaining consistency
- All UI components use consistent patterns: Radix primitives + Tailwind + CVA for variants