/**
 * Aushadha Sathi Frontend - API Client (JavaScript ES Module)
 */

export function resolveBackendBaseUrl() {
  if (typeof window !== "undefined") {
    if (window.__API_URL__) {
      return window.__API_URL__;
    }
    const metaApi = document.querySelector('meta[name="api-base-url"]');
    if (metaApi && metaApi.content) {
      return metaApi.content;
    }
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return "http://localhost:5000/api";
    }
  }
  return "/api";
}

export async function fetchHealth(baseUrl, customFetch) {
  const root = baseUrl || resolveBackendBaseUrl();
  const endpoint = `${root.replace(/\/$/, "")}/health`;
  const fetcher = customFetch || globalThis.fetch.bind(globalThis);

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);

  try {
    const response = await fetcher(endpoint, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Health probe failed with HTTP status ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error) {
      throw new Error(`API health check request failed: ${error.message}`);
    }
    throw new Error("API health check request failed with unknown error");
  }
}
