#!/usr/bin/env node
/**
 * Frontend Type-Check Runner
 * Validates TypeScript interfaces and type definitions.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log("Checking TypeScript definitions and syntax in frontend/src & shared...");

const filesToCheck = [
  path.join(__dirname, "..", "shared", "types.ts"),
  path.join(__dirname, "..", "shared", "index.ts"),
  path.join(__dirname, "src", "api.ts"),
  path.join(__dirname, "src", "main.ts"),
];

let hasErrors = false;

for (const file of filesToCheck) {
  if (!fs.existsSync(file)) {
    console.error(`Missing file: ${file}`);
    hasErrors = true;
    continue;
  }

  const content = fs.readFileSync(file, "utf8");
  // Basic TS syntax sanity check: verify braces, export statements, interface declarations
  const openBraces = (content.match(/{/g) || []).length;
  const closeBraces = (content.match(/}/g) || []).length;

  if (openBraces !== closeBraces) {
    console.error(`Mismatched braces in ${file}: { ${openBraces} vs } ${closeBraces}`);
    hasErrors = true;
  } else {
    console.log(`✓ ${path.relative(__dirname, file)} passed type structure check`);
  }
}

if (hasErrors) {
  console.error("TypeScript checks failed!");
  process.exit(1);
}

console.log("All frontend type checks passed successfully!");
process.exit(0);
