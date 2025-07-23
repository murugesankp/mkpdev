# Sentiment Analyzer Frontend (React + Vite)

This frontend provides a user interface for collecting customer feedback and displaying sentiment analysis results. Built with React and Vite for fast development and modern tooling.

## Features
- Interactive product card with review modal
- Real-time feedback submission to FastAPI backend
- Sentiment analysis results display (Positive/Negative/Neutral)
- Modern, responsive UI with loading states and error handling

## Tech Stack
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **CSS3** - Styling and animations
- **Fetch API** - HTTP requests to backend

---

## Granular Technical Flow (with BERT/OpenAI and React State)

```
User (Browser)
   │
   ▼
index.html
   │  (loads)
   ▼
src/main.jsx
   │  (calls ReactDOM.createRoot, renders <App />)
   ▼
src/App.jsx
   │  (renders product card, "Leave a Review" button)
   ▼
User clicks "Leave a Review"
   │
   ▼
App.jsx: setShowModal(true)   // React state: showModal = true
   │
   ▼
Modal opens (App.jsx)
   │
   ▼
User enters name (customer) and feedback (feedback)
   │
   ▼
App.jsx: setCustomer(value), setFeedback(value)   // React state: customer, feedback update on each keystroke
   │
   ▼
User clicks "Submit" (form onSubmit)
   │
   ▼
App.jsx: handleSubmit(e)
   │  - Prevents default form action
   │  - setLoading(true)   // React state: loading = true
   │  - setError(null), setSentiment(null)
   │  - Calls fetch('http://localhost:8000/feedback', { method: 'POST', headers, body: JSON.stringify({ customer, product, feedback }) })
   ▼
HTTP POST /feedback
   │
   ▼
backend/main.py
   │
   ▼
@app.post("/feedback", response_model=FeedbackOut)
   │  - Receives JSON: { customer, product, feedback }
   │  - Validates with Pydantic model: Feedback
   │
   ▼
main.py: analyze_sentiment_bert(feedback.feedback)  // DEFAULT: BERT
   │  - Uses Hugging Face Transformers library
   │  - Loads pre-trained BERT model (cardiffnlp/twitter-roberta-base-sentiment-latest)
   │  - Processes text locally (no external API calls)
   │  - Returns: "POSITIVE", "NEGATIVE", or "NEUTRAL"
   │
   ▼ (Alternative: OpenAI if specified)
main.py: analyze_sentiment_openai(feedback.feedback)  // OPTIONAL
   │  - Loads OPENAI_API_KEY from environment
   │  - Prepares prompt for sentiment classification
   │  - Calls OpenAI API (requires API key and internet)
   │  - Returns: "Positive", "Negative", or "Neutral"
   ▼
Backend processes sentiment result
   │  - Creates entry: { customer, product, feedback, sentiment }
   │  - Stores entry in MongoDB: sentiment_db.feedback.insert_one(entry)
   │  - Returns JSON: { customer, product, feedback, sentiment }
   ▼
HTTP Response to frontend
   │
   ▼
App.jsx: Receives response
   │  - setSentiment(data.sentiment)   // React state: sentiment = result
   │  - setShowModal(false)            // React state: showModal = false
   │  - setCustomer(''), setFeedback('') // React state: clear form fields
   │  - setLoading(false)              // React state: loading = false
   │  - Shows thank you message and sentiment result
   ▼
User sees result in browser
```

**Key Features:**
- **BERT by Default:** Fast, local sentiment analysis using Hugging Face Transformers
- **OpenAI Optional:** Can use OpenAI API for alternative analysis (requires API key)
- **Error Handling:** If backend or sentiment analysis fails, frontend shows error message
- **CORS:** FastAPI backend configured to allow frontend requests
- **State Management:** React's useState manages modal, form fields, loading, error, and sentiment
- **Data Validation:** Pydantic models ensure only valid data is processed
- **Security:** No API keys exposed to frontend; all analysis happens server-side

---

## End-to-End Flow
1. **User opens the app** (`frontend`): Sees a product card and clicks "Leave a Review"
2. **Review modal opens**: User enters their name and feedback
3. **On submit**: React sends feedback to FastAPI backend (`backend/main.py`) via HTTP POST
4. **Backend receives feedback**: Uses BERT (default) or OpenAI to analyze sentiment, stores result in MongoDB
5. **Backend responds**: Returns sentiment result to frontend
6. **Frontend displays result**: User sees a thank you and the sentiment (positive/negative/neutral)

---

## File-by-File Explanation

### Frontend (`frontend/`)
- **src/App.jsx**: Main React component. Shows product, handles modal, form, and API calls to backend
- **src/App.css**: Styles for product card, modal, buttons, and responsive layout
- **src/index.css**: Global styles and CSS variables for the app
- **src/main.jsx**: Entry point that renders the React app
- **src/assets/**: Images for the product card and UI elements
- **index.html**: HTML template loaded by Vite/React
- **package.json**: Lists dependencies (react, vite) and scripts (`npm run dev`, `npm run build`)
- **vite.config.js**: Vite build tool configuration for React development

### Backend Integration
The frontend communicates with these backend endpoints:
- **POST /feedback**: Submit customer feedback, get sentiment analysis (BERT default)
- **GET /feedback**: Retrieve all feedback entries (for admin/analytics)
- **POST /analyze-sentiment**: Direct sentiment analysis with method choice (bert/openai)
- **POST /analyze-sentiment-detailed**: Get detailed sentiment scores (BERT only)

### Sentiment Analysis Methods
- **BERT (Default)**: Uses Hugging Face Transformers for fast, offline sentiment analysis
- **OpenAI (Optional)**: Uses OpenAI API for cloud-based analysis (requires OPENAI_API_KEY)

---

## Setup Instructions
1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## Backend Requirements
Ensure the backend is running on `http://localhost:8000` with the following setup:
- FastAPI server running (`uvicorn main:app --reload`)
- MongoDB database accessible
- BERT model loaded (automatic on first run)
- (Optional) OpenAI API key for alternative sentiment analysis

---

## How it Works (Summary)
| Step | Component      | Action                                                                 |
|------|---------------|------------------------------------------------------------------------|
| 1    | React (UI)    | User sees product, clicks "Leave a Review"                             |
| 2    | React (UI)    | Modal form opens, user enters feedback                                 |
| 3    | React (JS)    | Form submits via fetch to FastAPI backend                              |
| 4    | FastAPI       | Receives POST, validates, analyzes sentiment (BERT default/OpenAI optional) |
| 5    | FastAPI+Mongo | Stores feedback+sentiment in MongoDB                                   |
| 6    | FastAPI       | Responds with sentiment result                                         |
| 7    | React (UI)    | Shows thank you + sentiment to user                                    |
| 8    | MongoDB       | Data is saved for future analytics                                     |

---

## Development Notes
- **BERT Analysis**: Fast and free, runs locally without external dependencies
- **OpenAI Analysis**: Requires API key and internet, may incur costs
- **Hot Reload**: Vite provides instant updates during development
- **Modern Tooling**: ES6+, JSX, CSS3, and modern React patterns
- **Error Boundaries**: Graceful error handling for better user experience

---

For backend setup and API details, see `../backend/README.md`.

**Extra Details:**
- **Error Handling:** If OpenAI or MongoDB fails, backend returns error, frontend shows error message (setError).
- **CORS:** FastAPI uses CORSMiddleware so browser fetch() is allowed.
- **State Management:** React’s useState manages modal, form fields, loading, error, and sentiment.
- **Data Validation:** Pydantic models ensure only valid data is processed.
- **API Security:** OpenAI API key is never exposed to frontend; only used server-side.

# Sentiment Analyzer: End-to-End Flow & File Guide

This project is a full-stack web app for product sentiment analysis using React (frontend), FastAPI (backend), MongoDB (database), and OpenAI GPT (AI model).

---

## End-to-End Flow
1. **User opens the app** (`frontend`): Sees a product card and clicks "Leave a Review".
2. **Review modal opens**: User enters their name and feedback.
3. **On submit**: React sends feedback to FastAPI backend (`backend/main.py`) via HTTP POST.
4. **Backend receives feedback**: Calls OpenAI GPT to analyze sentiment, stores result in MongoDB.
5. **Backend responds**: Returns sentiment result to frontend.
6. **Frontend displays result**: User sees a thank you and the sentiment (positive/negative/neutral).

---

## File-by-File Explanation

### Frontend (`frontend/`)
- **src/App.jsx**: Main React component. Shows product, handles modal, form, and API calls.
- **src/App.css**: Styles for product card, modal, and layout.
- **src/index.css**: Global styles for the app.
- **src/assets/**: (Optional) Images for the product or UI.
- **index.html**: HTML template loaded by Vite/React.
- **package.json**: Lists dependencies and scripts (e.g., `npm run dev`).
- **vite.config.js**: Vite build tool config for React.

### Backend (`backend/`)
- **main.py**: FastAPI app. Handles API endpoints, connects to MongoDB, and uses OpenAI for sentiment analysis.
  - `analyze_sentiment`: Calls OpenAI API to classify feedback.
  - `@app.post("/feedback")`: Receives feedback, analyzes, stores, and returns result.
  - `@app.get("/feedback")`: Returns all feedback (for future use).
- **requirements.txt**: Python dependencies (fastapi, uvicorn, pymongo, openai).

### Database
- **MongoDB**: Stores all feedback and sentiment results. No code file—just ensure MongoDB is running locally.

---

## How to Run
1. **Start MongoDB** (if not already running)
2. **Backend:**
   - Set your OpenAI API key: `$env:OPENAI_API_KEY="sk-..."`
   - `cd backend`
   - `python -m uvicorn main:app --reload`
3. **Frontend:**
   - `cd frontend`
   - `npm install` (first time only)
   - `npm run dev`
   - Open the URL shown in your terminal (e.g., http://localhost:5173)

---

## How it Works (Summary)
| Step | Component      | Action                                                                 |
|------|---------------|------------------------------------------------------------------------|
| 1    | React (UI)    | User sees product, clicks “Leave a Review”                             |
| 2    | React (UI)    | Modal form opens, user enters feedback                                 |
| 3    | React (JS)    | Form submits via fetch to FastAPI                                      |
| 4    | FastAPI       | Receives POST, validates, analyzes sentiment (OpenAI)                  |
| 5    | FastAPI+Mongo | Stores feedback+sentiment in MongoDB                                   |
| 6    | FastAPI       | Responds with sentiment result                                         |
| 7    | React (UI)    | Shows thank you + sentiment to user                                    |
| 8    | MongoDB       | Data is saved for future use                                           |

---

## Notes
- **OpenAI API usage may incur costs.** See https://openai.com/pricing and your OpenAI dashboard for details.
- You can improve the UI, sentiment logic, or add features as you learn!
