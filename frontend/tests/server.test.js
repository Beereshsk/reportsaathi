import test from "node:test";
import assert from "node:assert/strict";
import { createStaticServer } from "../server.js";

test("static server serves the app and assets with browser-safe MIME types", async (context) => {
  const server = createStaticServer();
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  context.after(() => new Promise((resolve, reject) => {
    server.close((error) => error ? reject(error) : resolve());
  }));

  const address = server.address();
  assert.ok(address && typeof address !== "string");
  const baseUrl = `http://127.0.0.1:${address.port}`;

  for (const [asset, contentType] of [
    ["/", "text/html"],
    ["/app.js", "text/javascript"],
    ["/styles.css", "text/css"],
  ]) {
    const response = await fetch(`${baseUrl}${asset}`);
    assert.equal(response.status, 200, `${asset} should load`);
    assert.match(response.headers.get("content-type") ?? "", new RegExp(contentType));
  }
});
