/**
 * Aushadha Sathi Frontend - Walking Skeleton Health Page (JavaScript ES Module)
 */

import { fetchHealth, resolveBackendBaseUrl } from "./api.js";

function getEl(id) {
  const el = document.getElementById(id);
  if (!el) {
    throw new Error(`Element #${id} not found in DOM`);
  }
  return el;
}

export async function checkSystemHealth() {
  const statusBadge = getEl("statusBadge");
  const serviceEl = getEl("serviceVal");
  const versionEl = getEl("versionVal");
  const dbStatusEl = getEl("dbStatusVal");
  const dbValueEl = getEl("dbValueText");
  const timestampEl = getEl("timestampVal");
  const latencyEl = getEl("latencyVal");
  const errorBanner = getEl("errorBanner");
  const errorMessage = getEl("errorMessage");
  const backendUrlEl = getEl("backendUrlVal");
  const refreshBtn = getEl("refreshBtn");

  const baseUrl = resolveBackendBaseUrl();
  backendUrlEl.textContent = baseUrl;

  // Set loading state
  statusBadge.className = "badge badge-loading";
  statusBadge.textContent = "PROBING...";
  refreshBtn.disabled = true;
  errorBanner.hidden = true;

  const startTime = performance.now();

  try {
    const data = await fetchHealth(baseUrl);
    const elapsed = Math.round(performance.now() - startTime);

    latencyEl.textContent = `${elapsed} ms`;
    serviceEl.textContent = data.service || "aushadha-sathi-api";
    versionEl.textContent = data.version || "1.0.0";
    timestampEl.textContent = data.timestamp || new Date().toISOString();

    if (data.status === "pass") {
      statusBadge.className = "badge badge-pass";
      statusBadge.textContent = "PASS (200 OK)";
    } else {
      statusBadge.className = "badge badge-fail";
      statusBadge.textContent = "FAIL";
    }

    // Render database value read by the backend
    if (data.database) {
      dbStatusEl.textContent = data.database.status.toUpperCase();
      dbStatusEl.className =
        data.database.status === "connected" ? "status-connected" : "status-disconnected";
      dbValueEl.textContent = data.database.value || "(No value returned from database)";
    } else {
      dbStatusEl.textContent = "UNSPECIFIED";
      dbStatusEl.className = "status-disconnected";
      dbValueEl.textContent = "Backend did not include database health payload.";
    }
  } catch (err) {
    const elapsed = Math.round(performance.now() - startTime);
    latencyEl.textContent = `${elapsed} ms`;
    statusBadge.className = "badge badge-fail";
    statusBadge.textContent = "UNREACHABLE";
    dbStatusEl.textContent = "DISCONNECTED";
    dbStatusEl.className = "status-disconnected";
    dbValueEl.textContent = "Could not fetch database status from backend.";

    errorBanner.hidden = false;
    errorMessage.textContent = err instanceof Error ? err.message : String(err);
  } finally {
    refreshBtn.disabled = false;
  }
}

// Initialize on page load
if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", () => {
    checkSystemHealth();
    const refreshBtn = document.getElementById("refreshBtn");
    if (refreshBtn) {
      refreshBtn.addEventListener("click", () => checkSystemHealth());
    }
  });
}
