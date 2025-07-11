import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#22c55e', '#ef4444']; // green, red

const SentimentChart = ({ results }) => {
  const data = [
    {
      name: 'Positive',
      value: results.filter(r => r.label === 'positive').length,
    },
    {
      name: 'Negative',
      value: results.filter(r => r.label === 'negative').length,
    },
  ];

  if (data.every(d => d.value === 0)) return null;

  return (
    <div className="mt-8 bg-white p-6 rounded shadow-md">
      <h3 className="text-lg font-semibold mb-4 text-center">📊 Sentiment Breakdown</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend verticalAlign="bottom" />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SentimentChart;
