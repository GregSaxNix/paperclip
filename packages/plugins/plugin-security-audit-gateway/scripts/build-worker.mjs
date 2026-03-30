import esbuild from "esbuild";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const packageRoot = path.resolve(__dirname, "..");

// Bundle the worker into a single self-contained file.
// The manifest is also bundled so the host can import it without workspace deps.
// Bundle worker as ESM (tsx loader in dev mode requires ESM)
await esbuild.build({
  entryPoints: [path.join(packageRoot, "src/worker.ts")],
  outfile: path.join(packageRoot, "dist/worker.js"),
  bundle: true,
  format: "esm",
  platform: "node",
  target: ["node20"],
  sourcemap: true,
  external: ["node:*"],
  logLevel: "info",
});

// Bundle manifest as ESM
await esbuild.build({
  entryPoints: [path.join(packageRoot, "src/manifest.ts")],
  outfile: path.join(packageRoot, "dist/manifest.js"),
  bundle: true,
  format: "esm",
  platform: "node",
  target: ["node20"],
  sourcemap: true,
  external: ["node:*"],
  logLevel: "info",
});
