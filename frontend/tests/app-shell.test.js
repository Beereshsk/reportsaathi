import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const app = fs.readFileSync(path.join(root, "app.js"), "utf8");

test("frontend serves the prescription assistant workflow", () => {
  assert.match(html, /id="cameraButton"/);
  assert.match(html, /id="uploadButton"/);
  assert.match(html, /id="typeButton"/);
  assert.match(html, /id="prescriptionText"/);
  assert.match(html, /id="reviewButton"/);
  assert.match(html, /id="speakButton"/);
  assert.match(html, /id="shareButton"/);
  assert.match(html, /Please confirm all medicine details with your doctor or pharmacist before taking any medicine\./);
  assert.doesNotMatch(html, /System Health & Verification/);
  assert.match(html, /src="app\.js"/);
  assert.ok(fs.existsSync(path.join(root, "app.js")));
  assert.ok(fs.existsSync(path.join(root, "styles.css")));
  assert.match(app, /\$\{apiBaseUrl\}\/notes/);
});
