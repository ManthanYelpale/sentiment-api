import React from 'react';
import SentimentForm from './components/SentimentForm';
import BatchSentimentForm from './components/BatchSentimentForm';

function App() {
  return (
    <div className="min-h-screen bg-white text-gray-800 p-4">
      <SentimentForm />
      <BatchSentimentForm />
    </div>
  );
}

export default App;
