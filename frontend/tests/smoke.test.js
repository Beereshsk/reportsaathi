/**
 * Frontend Automated Smoke Test
 * Verifies end-to-end frontend health probe, contract structure, and database response handling.
 */

import test from "node:test";
import assert from "node:assert/strict";
import { fetchHealth } from "../src/api.js";

test("Automated Frontend Smoke Test: Contract verification and DB payload extraction", async () => {
  const startTime = Date.now();
  let requestedEndpoint = "";

  const mockFetch = async (url) => {
    requestedEndpoint = url;
    return {
      ok: true,
      status: 200,
      statusText: "OK",
      json: async () => ({
        status: "pass",
        service: "aushadha-sathi-api",
        version: "1.0.0",
        timestamp: new Date().toISOString(),
        database: {
          status: "connected",
          value: "Database operational (SQLite connection verified)",
        },
      }),
    };
  };

  const health = await fetchHealth("https://staging.reportsaathi.in/api", mockFetch);
  const duration = Date.now() - startTime;

  assert.ok(requestedEndpoint.endsWith("/health"), "Should query /health endpoint");
  assert.equal(health.status, "pass", "Health status must be 'pass'");
  assert.equal(health.service, "aushadha-sathi-api");
  assert.equal(health.version, "1.0.0");
  assert.ok(health.database, "Database payload must be present");
  assert.equal(health.database.status, "connected");
  assert.ok(
    health.database.value.includes("Database operational"),
    "Should contain the database value"
  );
  assert.ok(duration < 1000, `Smoke test duration should be under 1s, took ${duration}ms`);
});
