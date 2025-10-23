# AI Music and Media Maker - Design Guidelines

## Design Approach

**Selected Approach**: Modern AI Creative Tool Aesthetic  
**Reference Inspiration**: Runway ML, Midjourney, ElevenLabs, Suno's interface  
**Rationale**: Balances professional utility with creative energy. Clean, dark-focused interface that puts generated content at center stage while maintaining intuitive controls.

## Core Design Principles

1. **Content-First**: Generated music/media is the hero
2. **Efficient Workflow**: Streamlined generation process with minimal friction
3. **Professional Polish**: Credible tool for serious creators
4. **Dark-Optimized**: Reduces eye strain during extended creative sessions

---

## Color Palette

### Dark Mode (Primary)
- **Background Base**: 220 15% 8% (deep charcoal blue)
- **Surface**: 220 14% 12% (elevated panels)
- **Surface Elevated**: 220 13% 16% (cards, modals)
- **Border Subtle**: 220 10% 22%
- **Border Default**: 220 8% 28%

### Brand Colors
- **Primary**: 260 85% 65% (vibrant purple - creative energy)
- **Primary Hover**: 260 85% 70%
- **Secondary**: 200 90% 55% (cyan accent - tech sophistication)

### Functional Colors
- **Success**: 142 76% 45% (generation complete)
- **Warning**: 38 92% 50% (processing)
- **Error**: 0 84% 60%
- **Text Primary**: 220 8% 95%
- **Text Secondary**: 220 6% 70%
- **Text Muted**: 220 5% 50%

### Light Mode (Secondary)
- **Background**: 220 15% 98%
- **Surface**: 0 0% 100%
- **Primary**: 260 75% 50% (slightly darker for contrast)
- **Text Primary**: 220 15% 10%

---

## Typography

**Font Stack**: 
- **Primary**: 'Inter', system-ui, sans-serif (Google Fonts)
- **Monospace**: 'JetBrains Mono', monospace (for technical data)

**Scale & Hierarchy**:
- **Display/Hero**: text-5xl font-bold (48px) - App title
- **H1**: text-3xl font-bold (30px) - Section headers
- **H2**: text-2xl font-semibold (24px) - Card titles
- **H3**: text-lg font-semibold (18px) - Form labels
- **Body**: text-base (16px) font-normal - Primary content
- **Small**: text-sm (14px) - Metadata, timestamps
- **Tiny**: text-xs (12px) - Helper text, tags

**Font Weights**: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

---

## Layout System

**Spacing Units**: Use Tailwind's 4, 6, 8, 12, 16, 24 for consistent rhythm
- **Component Padding**: p-6 to p-8 for cards
- **Section Spacing**: space-y-8 between major sections
- **Form Fields**: space-y-4 for vertical stacking
- **Grid Gaps**: gap-6 for media galleries, gap-4 for forms

**Container Widths**:
- **Max Width**: max-w-7xl (1280px) for main app container
- **Forms**: max-w-2xl centered for generation forms
- **Modals**: max-w-lg for login, max-w-4xl for media preview

**Grid Systems**:
- **Gallery**: grid-cols-1 md:grid-cols-2 lg:grid-cols-3
- **Controls**: Two-column forms on desktop (grid-cols-2 gap-4)

---

## Component Library

### Navigation
**Top App Bar**:
- Fixed header with backdrop-blur-md
- Logo left, user account avatar right
- Height: h-16
- Border bottom: border-b border-border-subtle

### Forms & Inputs

**Vocal Gender Picker**:
- Custom select dropdown with icon indicators
- Male: Blue microphone icon
- Female: Pink microphone icon  
- Neutral/Any: Purple microphone icon
- Rounded-lg border with focus:ring-2 ring-primary

**Standard Input Fields**:
- Rounded-lg borders
- h-11 (44px) for touch-friendly targets
- bg-surface with focus:bg-surface-elevated
- Placeholder text-muted
- Clear error states with text-error below

**Generation Button**:
- Primary CTA: Large rounded-full button
- bg-primary with hover:bg-primary-hover
- px-8 py-4 text-lg font-semibold
- Include animated generating state (pulsing gradient)

### Cards & Content Display

**Media Cards**:
- Rounded-xl with overflow-hidden
- bg-surface-elevated
- Hover: transform scale-105 transition
- Aspect ratio 16:9 or 1:1 for thumbnails
- Metadata overlay on hover (dark gradient from bottom)

**Modal - Login/Auth**:
- Centered overlay with backdrop-blur
- bg-surface-elevated rounded-2xl
- Shadow-2xl for depth
- Max-w-md
- Social login buttons (Google, GitHub) as outlined buttons
- Email/password form stacked vertically

### Media Player

**Audio Player Component**:
- Full-width waveform visualization (use library like wavesurfer.js)
- Custom controls: Play/Pause, scrubber, volume, download
- bg-surface with rounded-lg
- Accent color follows primary brand

**Generation Preview**:
- Large preview area with loading skeleton
- Success: Animated fade-in reveal
- Progress indicator: Linear progress bar in primary color

### Icons
**Library**: Heroicons (via CDN)
- Use outline variants for default states
- Solid variants for active/selected states
- Size: w-5 h-5 (20px) for UI icons, w-6 h-6 for feature icons

---

## Interactive States

**Buttons**:
- Default: Solid fills or outline variants
- Hover: Subtle brightness increase (5-10%)
- Active: Scale down to 98%
- Disabled: opacity-50 cursor-not-allowed

**Cards/Media**:
- Hover: Lift effect (shadow-lg, translate-y-[-2px])
- Focus: ring-2 ring-primary ring-offset-2
- Selected: border-2 border-primary

**Forms**:
- Focus: ring-2 ring-primary ring-offset-0
- Error: border-error with shake animation
- Success: border-success with checkmark icon

---

## Animations

**Use Sparingly**:
- Page transitions: Fade in only (duration-300)
- Generation button: Pulsing gradient when processing
- Media reveals: Fade + slide up (duration-500)
- Loading states: Skeleton pulse or spinner
- NO scroll-triggered animations
- NO parallax effects

---

## Page Structure

### Main Dashboard
1. **Header**: App bar with logo, user menu
2. **Generation Form**: Centered card (max-w-2xl)
   - Prompt textarea
   - Vocal gender picker (male/female dropdown)
   - Genre/style tags
   - Duration slider
   - Generate button
3. **Generated Content Gallery**: Grid of media cards below form
4. **Quick Stats**: Small metrics (credits remaining, generations today)

### User Account Modal
- Overlay with backdrop
- Login/signup tabs
- Social auth buttons
- Email/password form
- "Remember me" checkbox
- Smooth transitions between tabs

---

## Images

**Hero Section**: NO large hero image - this is a functional app, not a landing page

**Generated Content**: Display user-generated audio waveforms, album art thumbnails if applicable

**Empty States**: Illustrative graphics for "No generations yet" - use simple line art in primary color

**Profile/Avatar**: User profile pictures in circular frames (rounded-full)

---

## Accessibility

- Maintain WCAG AA contrast ratios (4.5:1 for text)
- All interactive elements min 44x44px touch target
- Keyboard navigation with visible focus indicators
- Screen reader labels for all form inputs
- Dark mode optimized for form inputs and text fields (consistent throughout)
- Loading/processing states announced to screen readers