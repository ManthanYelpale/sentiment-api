import React, { useState } from 'react';
import axios from 'axios';

const SentimentForm = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeSentiment = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/analyze_single', { text });
      setResult(response.data);
    } catch (error) {
      alert('API Error: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-8">
      <h1 className="text-3xl font-bold text-purple-700 mb-4 flex items-center gap-2">
        <span role="img" aria-label="brain">🧠</span> Sentiwave - Real-Time Sentiment Analyzer
      </h1>
      <form onSubmit={analyzeSentiment} className="space-y-4">
        <textarea
          className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
          rows={4}
          placeholder="Type your sentence here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          type="submit"
          className="bg-purple-600 text-white px-5 py-2 rounded hover:bg-purple-700 transition"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Sentiment"}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 bg-gray-50 border rounded">
          <p className="text-lg font-semibold">Sentiment: <span className="capitalize text-purple-700">{result.label}</span></p>
          <p className="text-sm text-gray-600">Positive: {result.pos.toFixed(3)}</p>
          <p className="text-sm text-gray-600">Negative: {result.neg.toFixed(3)}</p>
        </div>
      )}
    </div>
  );
};

export default SentimentForm;
