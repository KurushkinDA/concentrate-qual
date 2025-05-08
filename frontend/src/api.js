export async function apiFetch(path, data = null, method = 'POST') {
  const response = await fetch(`http://localhost:8000${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: data ? JSON.stringify(data) : null,
  });

  const text = await response.text();
  let json = {};
  try {
    json = JSON.parse(text);
  } catch (_) {}

  if (!response.ok) {
    const error = new Error(json.detail || 'Ошибка запроса');
    error.status = response.status;
    throw error;
  }

  return json;
}