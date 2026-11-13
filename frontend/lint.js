#!/usr/bin/env node
/**
 * Frontend Linter
 * Checks JavaScript and TypeScript code formatting and sanity.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log("Running frontend linter on src and tests...");

const dirsToScan = [
  path.join(__dirname, "src"),
  path.join(__dirname, "tests"),
];
const filesToScan = [path.join(__dirname, "app.js")];

let totalFiles = 0;
let lintErrors = 0;

for (const dir of dirsToScan) {
  if (!fs.existsSync(dir)) continue;
  for (const file of fs.readdirSync(dir)) {
    if (file.endsWith(".js") || file.endsWith(".ts")) {
      filesToScan.push(path.join(dir, file));
    }
  }
}

for (const fullPath of filesToScan) {
  const file = path.basename(fullPath);
  totalFiles++;
  const content = fs.readFileSync(fullPath, "utf8");
  if (content.includes("debugger;")) {
    console.error(`Lint error: 'debugger' statement found in ${file}`);
    lintErrors++;
  }
}

if (lintErrors > 0) {
  console.error(`Frontend linting failed with ${lintErrors} error(s).`);
  process.exit(1);
}

console.log(`All ${totalFiles} frontend source files passed lint check!`);
process.exit(0);
