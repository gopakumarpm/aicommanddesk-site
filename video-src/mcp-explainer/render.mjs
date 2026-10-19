// Renders index.html frame-by-frame with Playwright and encodes to MP4 with ffmpeg.
// usage: node render.mjs <out.mp4> [fps=24] [frameDir]   |   node render.mjs --stills <dir> t1 t2 ...
import { createRequire } from 'module';
import { execFileSync } from 'child_process';
import { mkdirSync, rmSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const here = path.dirname(fileURLToPath(import.meta.url));

const args = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto('file://' + path.join(here, 'index.html'));

if (args[0] === '--stills') {
  const dir = args[1];
  mkdirSync(dir, { recursive: true });
  for (const t of args.slice(2)) {
    await page.evaluate(t => window.render(t), +t);
    await page.screenshot({ path: path.join(dir, `t${t}.png`) });
  }
  await browser.close();
  process.exit(0);
}

const [out, fpsArg = '24', frames = path.join(here, '.frames')] = args;
const fps = +fpsArg;
const duration = await page.evaluate(() => window.DURATION);
rmSync(frames, { recursive: true, force: true });
mkdirSync(frames, { recursive: true });
const n = Math.round(duration * fps);
for (let i = 0; i < n; i++) {
  await page.evaluate(t => window.render(t), i / fps);
  await page.screenshot({ path: path.join(frames, `f${String(i).padStart(5, '0')}.png`) });
}
await browser.close();
execFileSync('ffmpeg', ['-y', '-framerate', String(fps), '-i', path.join(frames, 'f%05d.png'),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', out], { stdio: 'inherit' });
rmSync(frames, { recursive: true, force: true });
console.log('wrote', out);
