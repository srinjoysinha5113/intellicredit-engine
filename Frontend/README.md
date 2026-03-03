# Jindal Assistant - React Version

This is a React-based conversion of the original vanilla HTML/CSS/JavaScript Jindal Assistant chatbot application.

## Project Structure

The project has been converted from a monolithic structure to a component-based React architecture with the following improvements:

### Component-Based Architecture
- **Header Component** (`src/components/Header.jsx`) - Handles logo, title, and theme toggle
- **Sidebar Component** (`src/components/Sidebar.jsx`) - Manages FAQ navigation and collapsible sidebar
- **ChatArea Component** (`src/components/ChatArea.jsx`) - Handles message display and input
- **App Component** (`src/App.jsx`) - Main application with state management

### Modular CSS
The original 416-line CSS file has been broken down into:
- `src/styles/variables.css` - CSS variables and global styles
- `src/styles/Header.css` - Header-specific styles
- `src/styles/Sidebar.css` - Sidebar-specific styles
- `src/styles/ChatArea.css` - Chat area-specific styles
- `src/styles/App.css` - App layout styles

### State Management
- **Theme Context** (`src/context/ThemeContext.jsx`) - Centralized theme management with localStorage persistence
- **React State** - Component-level state for chat history, sidebar collapse, FAQ data, and input handling

### Key Features Preserved
- ✅ Dark/Light theme toggle with persistence
- ✅ Collapsible sidebar with smooth animations
- ✅ FAQ department navigation with icons
- ✅ Chat functionality with backend API integration
- ✅ Responsive design
- ✅ Auto-resizing textarea input
- ✅ Markdown parsing for bot responses

### New React Benefits
- 🔄 Component reusability
- 🎯 Better state management
- 🧩 Modular architecture
- 🚀 Improved maintainability
- 📦 Easier to extend and test

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## Dependencies
- React 18
- Vite (build tool)
- marked (Markdown parsing)
- Material Icons (via Google Fonts)

## Backend Integration
The app expects a backend API running at `http://localhost:8000/chat` that accepts POST requests with:
```json
{
  "message": "user question here"
}
```

And responds with:
```json
{
  "answer": "bot response here"
}
```
