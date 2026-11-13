/**
 * Aushadha Sathi Frontend - API Client (TypeScript)
 */

export interface DatabaseHealth {
  status: "connected" | "disconnected" | "unconfigured";
  value: string;
}

export interface HealthResponse {
  status: "pass" | "fail";
  service: string;
  version: string;
  timestamp: string;
  database: DatabaseHealth;
}

export function resolveBackendBaseUrl(): string {
  if (typeof window !== "undefined") {
    const win = window as unknown as { __API_URL__?: string };
    if (win.__API_URL__) {
      return win.__API_URL__;
    }
    const metaApi = document.querySelector<HTMLMetaElement>('meta[name="api-base-url"]');
    if (metaApi && metaApi.content) {
      return metaApi.content;
    }
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return "http://localhost:5000/api";
    }
  }
  return "/api";
}

export type FetchFn = (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>;

export async function fetchHealth(baseUrl?: string, customFetch?: FetchFn): Promise<HealthResponse> {
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

    const data: HealthResponse = await response.json();
    return data;
  } catch (error: unknown) {
    clearTimeout(timeoutId);
    if (error instanceof Error) {
      throw new Error(`API health check request failed: ${error.message}`);
    }
    throw new Error("API health check request failed with unknown error");
  }
}
