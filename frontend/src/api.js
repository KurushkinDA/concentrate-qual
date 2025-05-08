const API_URL = 'http://localhost:8000';

export async function apiFetch(path, data = null, method = 'POST') {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  };

  if (data && method !== 'GET') {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(`${API_URL}${path}`, options);

  const text = await response.text();
  console.log('RAW RESPONSE:', text);

  let json = {};
  try {
    json = JSON.parse(text);
  } catch (_) {}

  if (!response.ok) {
    console.error('Ошибка запроса:', json);
    throw new Error(json.detail || 'Ошибка запроса');
  }

  return json;
}