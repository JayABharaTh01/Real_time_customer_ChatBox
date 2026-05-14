"use client";

import { useState } from "react";

export default function HomePage() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!query.trim()) return;

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail || 'API error');
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: '3rem auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Customer Support Agent (Next.js)</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask your question"
          rows={3}
          style={{ width: '100%', marginBottom: '0.6rem', fontSize: '1rem' }}
        />
        <button type="submit" disabled={loading || !query.trim()}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #ddd', background: '#f8f8f8' }}>
          <h2>Result</h2>
          <p><strong>Agent:</strong> {result.agent}</p>
          <p><strong>Answer:</strong> {result.answer}</p>
          <p><strong>Confidence:</strong> {result.confidence}</p>
          <pre>{JSON.stringify(result.metadata, null, 2)}</pre>
        </div>
      )}
    </main>
  );
}