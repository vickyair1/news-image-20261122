// The World Today — Sunday 22 November 2026 (Node 22, stdlib only).
//
// The entry is the dense one-page newspaper next to this file (entry.png,
// 1024x1024): 28 verified stories from Sunday 22 November 2026 across 7
// regions — three leads (COP31 closing in on a deal at dawn in Antalya,
// Iran's overnight strikes on US bases in Bahrain, the Sparta II still
// ablaze in the Gulf of Finland), ten feature cards, 15 one-line briefs,
// a stat strip, a region tally, a dotted world map with numbered pins, a
// DATE CHECK box of earlier stories deliberately left out, and a source
// footer. Round 2 of this entry: the lead hierarchy was rebuilt around the
// burning freighter, COP31 was de-padded from 8 stories to 4, all briefs
// are verified Sunday stories with no stale date tags, and the lead art was
// redrawn richer with no label chips on the art. The page was drawn with
// Python/PIL (see the build script in the working directory, not part of
// this repo); every picture on it is a drawn illustration, every word
// rendered as text, nothing copied from any other entry.
//
// This program only hands the finished image over: it reads entry.png,
// checks it really is a PNG of at most 1 MiB, and writes those exact
// bytes to the output directory. No clock, no randomness, no network —
// so two runs write identical bytes.

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1048576;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

const folder = dirname(fileURLToPath(import.meta.url));
const source = join(folder, 'entry.png');
const destinationDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const destination = join(destinationDir, 'entry.png');

const image = readFileSync(source);
if (image.length === 0 || image.length > MAX_BYTES) {
  throw new Error(`entry.png is ${image.length} bytes, expected 1..${MAX_BYTES}`);
}
if (!image.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png does not start with the PNG signature');
}
if (image.length < 33 || image.subarray(12, 16).toString('ascii') !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk where one is expected');
}
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  throw new Error(
    `entry.png is ${width}x${height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`,
  );
}

mkdirSync(destinationDir, { recursive: true });
writeFileSync(destination, image);

const sourceHash = createHash('sha256').update(image).digest('hex');
const copied = readFileSync(destination);
if (!copied.equals(image)) {
  throw new Error('the copied entry.png differs from the source');
}
const copiedHash = createHash('sha256').update(copied).digest('hex');
if (copiedHash !== sourceHash) {
  throw new Error('the copied entry.png hash differs from the source');
}

console.log(`Front page written to ${destination} (${copied.length} bytes)`);
console.log(`sha256 ${copiedHash}`);
