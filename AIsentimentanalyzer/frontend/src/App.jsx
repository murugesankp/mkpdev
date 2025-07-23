

import { useState } from 'react';
import './App.css';

function App() {
  const [showModal, setShowModal] = useState(false);
  const [customer, setCustomer] = useState('');
  const [feedback, setFeedback] = useState('');
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const product = {
    name: 'SuperWidget 3000',
    image: 'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80',
    description: 'The SuperWidget 3000 is the latest in widget technology. Experience performance and style like never before!'
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSentiment(null);
    try {
      const res = await fetch('http://localhost:8000/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer, product: product.name, feedback })
      });
      if (!res.ok) throw new Error('Failed to analyze feedback');
      const data = await res.json();
      setSentiment(data.sentiment);
      setShowModal(false);
      setCustomer('');
      setFeedback('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="product-card">
        <img src={product.image} alt={product.name} className="product-image" />
        <h1>{product.name}</h1>
        <p className="product-desc">{product.description}</p>
        <button className="review-btn" onClick={() => setShowModal(true)}>
          Leave a Review
        </button>
      </div>

      {showModal && (
        <div className="modal-backdrop" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h2>Leave a Review</h2>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Your Name"
                value={customer}
                onChange={e => setCustomer(e.target.value)}
                required
              />
              <textarea
                placeholder="Your feedback..."
                value={feedback}
                onChange={e => setFeedback(e.target.value)}
                required
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Submitting...' : 'Submit'}
              </button>
              <button type="button" className="close-btn" onClick={() => setShowModal(false)}>
                Cancel
              </button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
          </div>
        </div>
      )}

      {sentiment && (
        <div className="result">
          <h2>Thank you for your review!</h2>
          <p>Sentiment: <span>{sentiment}</span></p>
        </div>
      )}
    </div>
  );
}

export default App;
