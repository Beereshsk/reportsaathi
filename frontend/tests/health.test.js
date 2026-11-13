/**
 * Frontend Unit Test for Health Client
 * Uses Node.js native test runner (node:test).
 */

import test from "node:test";
import assert from "node:assert/strict";
import { fetchHealth } from "../src/api.js";

test("fetchHealth should parse successful 200 OK response with database value", async () => {
  const mockResponse = {
    status: "pass",
    service: "aushadha-sathi-api",
    version: "1.0.0",
    timestamp: "2026-11-13T14:15:00Z",
    database: {
      status: "connected",
      value: "Database connection healthy (SQLite)",
    },
  };

  const mockFetch = async (url) => {
    assert.ok(url.endsWith("/health"), "Expected URL to end with /health");
    return {
      ok: true,
      status: 200,
      statusText: "OK",
      json: async () => mockResponse,
    };
  };

  const data = await fetchHealth("http://localhost:5000/api", mockFetch);
  assert.equal(data.status, "pass");
  assert.equal(data.service, "aushadha-sathi-api");
  assert.equal(data.version, "1.0.0");
  assert.ok(data.database);
  assert.equal(data.database.status, "connected");
  assert.equal(data.database.value, "Database connection healthy (SQLite)");
});

test("fetchHealth should throw error on 500 status", async () => {
  const mockFetch = async () => ({
    ok: false,
    status: 500,
    statusText: "Internal Server Error",
    json: async () => ({ error: "Internal Server Error" }),
  });

  await assert.rejects(
    async () => {
      await fetchHealth("http://localhost:5000/api", mockFetch);
    },
    {
      message: /HTTP status 500/,
    }
  );
});
