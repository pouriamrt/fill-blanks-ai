# Fill Blanks App - Frontend

React-based frontend for the Fill Blanks Quiz Application. This interactive web interface allows users to select topics, answer AI-generated fill-in-the-blank questions, receive instant feedback, and track their scores in real-time.

## 🚀 Features

- **Topic Selection**: Choose from various quiz topics (Science, Technology, History, etc.)
- **Interactive Quiz Interface**: Clean, intuitive UI for answering questions
- **Real-time Feedback**: Instant feedback on correct/incorrect answers
- **Score Tracking**: Live score updates (correct answers / total attempts)
- **Hint System**: Get helpful hints when stuck on a question
- **Question Navigation**: Seamless flow between questions within a topic
- **Fast Refresh**: Hot Module Replacement (HMR) for instant development updates

## 🛠️ Tech Stack

- **React 19**: Modern UI library for building user interfaces
- **Vite 7**: Next-generation frontend build tool with lightning-fast HMR
- **Axios**: Promise-based HTTP client for API requests
- **ESLint**: Code linting and quality enforcement
- **Modern CSS**: Inline styles for component-specific styling

## 📋 Prerequisites

- **Node.js 16+** (LTS version recommended)
- **npm** (comes with Node.js) or **yarn**
- **Backend API**: The FastAPI backend should be running on `http://localhost:8000`

## 🏃 Getting Started

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Development

Start the development server with hot reload:

```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or another port if 5173 is in use).

**Note**: Make sure the backend server is running on `http://localhost:8000` before starting the frontend.

### Build for Production

Create an optimized production build:

```bash
npm run build
```

The built files will be in the `dist` directory, ready to be deployed to any static hosting service.

### Preview Production Build

Preview the production build locally:

```bash
npm run preview
```

### Linting

Run ESLint to check code quality:

```bash
npm run lint
```

## 📁 Project Structure

```
frontend/
├── public/              # Static assets
│   └── vite.svg
├── src/
│   ├── assets/         # Images and other assets
│   │   └── react.svg
│   ├── App.jsx         # Main application component
│   ├── App.css         # Application-specific styles
│   ├── main.jsx        # React entry point
│   └── index.css       # Global styles
├── index.html          # HTML template
├── vite.config.js      # Vite configuration
├── eslint.config.js    # ESLint configuration
└── package.json        # Dependencies and scripts
```

## 🔌 API Integration

The frontend communicates with the FastAPI backend running on `http://localhost:8000`. The API endpoints used are:

- `GET /topics` - Fetch all available topics
- `POST /get_question` - Generate a new question for a topic
- `POST /submit_answer` - Submit an answer for evaluation
- `GET /score/{topic_id}` - Get score statistics for a topic (not currently used in UI)

To change the API URL, update the `API_URL` constant in `src/App.jsx`:

```javascript
const API_URL = "http://localhost:8000"; // Change this for different environments
```

## 🎮 How It Works

1. **Topic Selection**: On app load, available topics are fetched from the backend
2. **Game Start**: User selects a topic to begin the quiz
3. **Question Generation**: A new fill-in-the-blank question is generated via the AI backend
4. **Answer Submission**: User types their answer and submits
5. **Feedback**: Instant feedback is provided (correct/incorrect with the right answer)
6. **Auto-Next**: After 1.5 seconds, the next question is automatically loaded
7. **Score Tracking**: Score and attempts are tracked and displayed in real-time

## 🎨 Customization

### Styling

The app currently uses inline styles. To customize the appearance:

- Modify styles in `src/App.jsx` directly
- Add global styles in `src/index.css`
- Consider migrating to CSS modules or a styling library for larger projects

### Configuration

Vite configuration can be modified in `vite.config.js`. Common customizations:

- Proxy API requests during development
- Configure build options
- Add plugins for additional functionality

Example: Adding a proxy for API requests:

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

## 🐛 Troubleshooting

### Backend Connection Issues

If you see connection errors:
1. Ensure the backend is running on `http://localhost:8000`
2. Check that CORS is enabled in the FastAPI backend
3. Verify the `API_URL` in `src/App.jsx` matches your backend URL

### Port Already in Use

If port 5173 is already in use, Vite will automatically try the next available port. The terminal will show the actual port being used.

### Build Issues

If you encounter build errors:
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Clear Vite cache: `rm -rf node_modules/.vite` (Linux/Mac) or `rmdir /s node_modules\.vite` (Windows)

## 📝 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server with HMR |
| `npm run build` | Create production build |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Run ESLint to check code quality |

## 🔮 Future Enhancements

Potential improvements for the frontend:

- [ ] Add loading states and skeletons
- [ ] Implement error boundaries
- [ ] Add routing for multiple pages
- [ ] Create a history/stats page
- [ ] Add animations and transitions
- [ ] Implement dark mode
- [ ] Add unit and integration tests
- [ ] Migrate to TypeScript for type safety
- [ ] Add state management (Redux/Zustand) for complex state
- [ ] Implement responsive design improvements

## 📚 Learn More

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vite.dev/)
- [Axios Documentation](https://axios-http.com/)
- [ESLint Documentation](https://eslint.org/)

## 🤝 Contributing

When contributing to the frontend:

1. Follow the existing code style
2. Run `npm run lint` before committing
3. Test your changes in both development and production builds
4. Ensure the app works with the backend API

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
