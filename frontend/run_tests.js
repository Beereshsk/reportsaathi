#!/usr/bin/env node
/**
 * Frontend Test Runner
 * Uses Node.js built-in test runner to execute unit and smoke tests.
 */

import { run } from "node:test";
import { spec } from "node:test/reporters";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log("Running frontend test suite via node:test...");

const testFiles = [
  path.join(__dirname, "tests", "health.test.js"),
  path.join(__dirname, "tests", "smoke.test.js"),
  path.join(__dirname, "tests", "app-shell.test.js"),
  path.join(__dirname, "tests", "server.test.js"),
];

const stream = run({ files: testFiles });
stream.compose(new spec()).pipe(process.stdout);

stream.on("test:fail", () => {
  process.exitCode = 1;
});
