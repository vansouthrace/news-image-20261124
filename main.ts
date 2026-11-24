// main.ts — entrypoint for the news-image-20261124 bounty (Node 22,
// standard library only). The entry image lives beside this file as
// entry.png (drawn by render.py); this program copies it to the output
// directory the grader provides, after a light sanity check that it is
// a whole PNG inside the competition's size limits.
//
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576; // 1 MiB, the competition's gate
const MAX_DIM = 1024;

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

const bytes = readFileSync(src);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG file');
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate`);
}
// PNG dimensions live in the IHDR chunk: width at bytes 16-19, height at 20-23.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_DIM || height > MAX_DIM) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 gate`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
const written = statSync(dest).size;
console.log(`wrote ${dest} (${width}x${height}, ${written} bytes)`);
