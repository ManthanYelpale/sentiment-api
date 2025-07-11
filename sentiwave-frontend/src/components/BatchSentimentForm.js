import SentimentChart from './SentimentChart';
import React, { useState } from 'react';
import axios from 'axios';

const BatchSentimentForm = () => {
  const [textBlock, setTextBlock] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzeBatch = async (e) => {
    e.preventDefault();
    const lines = textBlock.split('\n').map(line => line.trim()).filter(Boolean);
    if (lines.length === 0) return alert("Please enter at least one sentence.");
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/analyze_batch', { texts: lines });
      setResults(response.data);
    } catch (err) {
      alert("Batch API Error: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold text-blue-700 mb-4 flex items-center gap-2">
        <span role="img" aria-label="repeat">🔁</span> Batch Sentiment Analysis
      </h2>
      <form onSubmit={analyzeBatch} className="space-y-4">
        <textarea
          className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={6}
          placeholder="Enter one sentence per line..."
          value={textBlock}
          onChange={(e) => setTextBlock(e.target.value)}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Batch"}
        </button>
      </form>

      {results.length > 0 && (
        <div className="mt-6 space-y-3">
          {results.map((res, i) => (
            <div key={i} className="p-3 bg-gray-50 border rounded">
              <p><strong>Line {i + 1}:</strong> <span className="capitalize">{res.label}</span></p>
              <p className="text-sm text-gray-600">Pos: {res.pos.toFixed(3)} | Neg: {res.neg.toFixed(3)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BatchSentimentForm;
{results.length > 0 && <SentimentChart results={results} />}

