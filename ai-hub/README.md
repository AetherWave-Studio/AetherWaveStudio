# AIverse - AI Tools Directory

AIverse is a comprehensive directory of 1000+ AI tools, built with React, TypeScript, and Vite. The application provides users with an intuitive interface to discover, search, and explore various AI tools across multiple categories.

## Tech Stack

- **Frontend**: React 18 + TypeScript
- **Build Tool**: Vite 6
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI + shadcn/ui
- **Backend**: Supabase (Database + Authentication)
- **Package Manager**: pnpm
- **Routing**: React Router v6

## Features

- 🔍 Advanced search and filtering
- 📁 Category-based organization
- ⭐ Tool ratings and recommendations
- 🎨 Dark mode support
- 📱 Responsive design
- 🔐 User authentication (via Supabase)
- 💾 User favorites and submissions
- ♿ Accessibility features (high contrast mode)

## Project Structure

```
aiverse/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── hooks/          # Custom React hooks
│   ├── lib/            # Utilities and Supabase client
│   └── App.tsx         # Main application component
├── public/             # Static assets
└── supabase/           # Database migrations and functions
```

## Getting Started

### Prerequisites

- Node.js 18+ or 20+
- pnpm package manager

### Installation

1. Install dependencies:
```bash
cd aiverse
pnpm install
```

2. Start the development server:
```bash
pnpm run dev
```

The application will be available at `http://localhost:5000`

### Build for Production

```bash
pnpm run build
```

## Database

The application uses Supabase for backend services:
- PostgreSQL database
- Real-time subscriptions
- Authentication
- Row Level Security (RLS) policies

Database tables:
- `tools` - AI tool listings
- `categories` - Tool categories
- `profiles` - User profiles
- `user_favorites` - User favorite tools
- `user_submissions` - User-submitted tools

## Environment

The Supabase connection details are configured in `src/lib/supabase.ts`. For production, consider moving credentials to environment variables.

## Contributing

This is an open-source project. Contributions are welcome!

## License

See LICENSE file for details.
