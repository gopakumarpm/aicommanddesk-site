// Renders index.html frames with Playwright (parallel workers) and encodes with ffmpeg.
// set VERTICAL=1 for the 9:16 (1080x1920) cut
// usage: node render.mjs --stills <dir> <timings.json> t1 t2 ...
//        node render.mjs <timings.json> <out_silent.mp4> [fps=20] [workers=4] [frameDir]
import { createRequire } from 'module';
import { execFileSync } from 'child_process';
import { mkdirSync, rmSync, readFileSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);

const VERT = process.env.VERTICAL === '1';
async function open(timings) {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage(VERT ? { viewport: { width: 720, height: 1280 }, deviceScaleFactor: 1.5 } : { viewport: { width: 1280, height: 720 } });
  await page.addInitScript(([t, v]) => { window.TIMINGS = t; window.VERTICAL = v; }, [timings, VERT]);
  await page.goto('file://' + path.join(here, 'index.html'));
  return { browser, page };
}

if (args[0] === '--stills') {
  const [, dir, tj, ...ts] = args;
  mkdirSync(dir, { recursive: true });
  const { browser, page } = await open(JSON.parse(readFileSync(tj)));
  for (const t of ts) {
    await page.evaluate(t => window.render(t), +t);
    await page.screenshot({ path: path.join(dir, `t${t}.png`) });
  }
  await browser.close();
  process.exit(0);
}

const [tj, out, fpsArg = '20', workersArg = '4', frames = path.join(here, '.frames')] = args;
const timings = JSON.parse(readFileSync(tj));
const fps = +fpsArg, workers = +workersArg, n = Math.round(timings.total * fps);
rmSync(frames, { recursive: true, force: true });
mkdirSync(frames, { recursive: true });
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  const { browser, page } = await open(timings);
  for (let i = w; i < n; i += workers) {
    await page.evaluate(t => window.render(t), i / fps);
    await page.screenshot({ path: path.join(frames, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  await browser.close();
}));
execFileSync('ffmpeg', ['-y', '-framerate', String(fps), '-i', path.join(frames, 'f%05d.jpg'),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out], { stdio: 'inherit' });
rmSync(frames, { recursive: true, force: true });
console.log('wrote', out);
