---

## Granular Technical Flow (with OpenAI API and React State)

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
main.py: analyze_sentiment(feedback.feedback)
   │  - Loads OPENAI_API_KEY from environment
   │  - Prepares prompt: "Classify the sentiment of the following customer feedback as Positive, Negative, or Neutral: Feedback: ... Sentiment:"
   │  - Calls openai.Completion.create(engine="text-davinci-003", prompt, ...)
   │
   ▼
OpenAI API (cloud)
   │  - Receives prompt, runs the model, returns: "Positive" / "Negative" / "Neutral"
   │    (OpenAI charges per token; you can check usage in your OpenAI dashboard)
   ▼
main.py: Receives OpenAI response
   │  - Extracts sentiment from response
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
