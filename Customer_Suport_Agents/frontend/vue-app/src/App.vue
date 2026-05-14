<template>
  <div class="app-container">
    <h1>Customer Support Agent (Vue)</h1>
    <textarea v-model="query" placeholder="Ask your question" rows="3" />
    <button @click="sendQuery" :disabled="loading || !query.trim()">Send</button>

    <div v-if="loading" class="status">Thinking...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="response" class="response">
      <h2>Response</h2>
      <p><strong>Agent:</strong> {{ response.agent }}</p>
      <p><strong>Answer:</strong> {{ response.answer }}</p>
      <p><strong>Confidence:</strong> {{ response.confidence }}</p>
      <pre>{{ response.metadata }}</pre>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const query = ref('');
    const response = ref(null);
    const error = ref('');
    const loading = ref(false);

    async function sendQuery() {
      error.value = '';
      response.value = null;
      loading.value = true;

      try {
        const resp = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: query.value })
        });

        if (!resp.ok) {
          const json = await resp.json();
          throw new Error(json.detail || 'API error');
        }

        response.value = await resp.json();
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    return { query, response, error, loading, sendQuery };
  }
};
</script>

<style scoped>
.app-container {
  max-width: 720px;
  margin: 3rem auto;
  padding: 1rem;
  font-family: Arial, sans-serif;
}
textarea {
  width: 100%;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}
button {
  padding: 0.5rem 1rem;
}
.status { color: #444; }
.error { color: #b00020; }
.response { background: #f8f8f8; padding: 1rem; margin-top: 1rem; border-left: 4px solid #007acc; }
</style>