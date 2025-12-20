# AGENT-X Pizza - Frontend

Modern, animated Next.js frontend for the agentic pizza ordering system.

## 🎨 Features

- **Beautiful UI**: Glassmorphism, gradients, and smooth animations
- **Real-time Chat**: Interactive chat with AGENT-X
- **Smart Menu**: Search, filter by category, view details
- **Order Tracking**: Visual timeline with status updates
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- **Premium Animations**: Framer Motion for smooth transitions

## 🚀 Getting Started

### Install Dependencies
```bash
npm install
```

### Configure Environment
Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production
```bash
npm run build
npm start
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── chat/            # Chat with AGENT-X
│   ├── menu/            # Browse pizzas
│   ├── cart/            # Shopping cart
│   ├── order/           # Order tracking
│   ├── layout.tsx       # Root layout with navigation
│   ├── page.tsx         # Landing page
│   └── globals.css      # Global styles
│
├── lib/
│   └── api-client.ts    # Backend API client
│
├── components/          # Reusable components
├── public/              # Static assets
├── tailwind.config.js   # Tailwind configuration
└── next.config.js       # Next.js configuration
```

## 🎨 Design System

### Colors
- `pizza-red`: #E63946
- `pizza-orange`: #F77F00
- `pizza-yellow`: #FCBF49
- `pizza-dark`: #1A1A2E
- `pizza-darker`: #16213E

### Typography
- Headings: **Poppins** (Google Fonts)
- Body: **Inter** (Google Fonts)

### Key Components

#### Glassmorphism
```tsx
<div className="glass-dark">
  {/* Content */}
</div>
```

#### Buttons
```tsx
<button className="btn-primary">Primary Action</button>
<button className="btn-secondary">Secondary Action</button>
```

#### Card Hover Effect
```tsx
<div className="card-hover">
  {/* Card content */}
</div>
```

## 🔗 API Integration

All API calls go through `lib/api-client.ts`.

Example usage:
```typescript
import { sendChatMessage, getMenu, createOrder } from '@/lib/api-client';

// Send chat message
const response = await sendChatMessage({
  message: "Show me pizzas",
  user_id: "user_123"
});

// Get menu
const items = await getMenu();

// Create order
const order = await createOrder({
  user_id: "user_123",
  items: [...]
});
```

## 🎭 Animations

Using Framer Motion for all animations:

```typescript
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>
```

## 📱 Pages

### `/` - Landing Page
Hero section with feature cards and stats

### `/chat` - AI Chat
Real-time messaging with AGENT-X

### `/menu` - Menu Browser  
Search and filter pizza catalog

### `/cart` - Shopping Cart
Review and checkout

### `/order` - Order Tracking
Track order with visual timeline

## 🚀 Deployment

### Vercel (Recommended)
1. Connect GitHub repository
2. Set environment variable: `NEXT_PUBLIC_API_URL`
3. Deploy

### Manual Deployment
```bash
npm run build
npm start
```

## 🎨 Customization

### Change Theme Colors
Edit `tailwind.config.js`:
```javascript
colors: {
  'pizza-red': '#YOUR_COLOR',
  // ...
}
```

### Add New Page
1. Create `app/yourpage/page.tsx`
2. Add route to navigation in `app/layout.tsx`

### Custom Components
Create in `components/` directory and import as needed.

## 📝 License

MIT

---

**Built with Next.js 14, TypeScript, Tailwind CSS, and Framer Motion**
