#!/usr/bin/env node
/**
 * render.cjs — 把任务目录里的 index.html 确定性渲染成 PNG
 *
 * 用法：
 *   node scripts/render.cjs <任务目录> [--scale=2] [--out=output] [--only=01-cover]
 *
 * 约定：
 *   - <任务目录>/index.html 必须存在，且是单文件（不引用外部 css/js）
 *   - 每个 <section class="poster"> 出一张 PNG
 *   - 文件名取 data-name，缺省按出现顺序 01.png / 02.png …
 *   - 输出到 <任务目录>/<out>/，默认 output/
 *   - 日志报的是**输出像素**（画板 CSS px × --scale），不是画板尺寸
 *   - 长图（.poster.long，可达 8000px）不受视口高度限制，不会被截断
 *     （实测 6412px @1x / 12824px @2x 完整出图）
 *
 * 浏览器解析顺序：系统 Chrome → 系统 Edge → Playwright 自带 chromium
 * 全部带 --no-sandbox（受管沙箱必需）。详见 references/render-pipeline.md。
 */
'use strict';

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

/* ---------------- 参数 ---------------- */
const argv = process.argv.slice(2);
const flags = {};
const positional = [];
for (const a of argv) {
  const m = /^--([^=]+)(?:=(.*))?$/.exec(a);
  if (m) flags[m[1]] = m[2] === undefined ? true : m[2];
  else positional.push(a);
}
const taskDir = positional[0] ? path.resolve(positional[0]) : null;
if (!taskDir) {
  console.error('用法：node scripts/render.cjs <任务目录> [--scale=2] [--out=output] [--only=01-cover]');
  process.exit(2);
}
const scale = Number(flags.scale || 1);
const outDirName = flags.out || 'output';
const only = typeof flags.only === 'string' ? flags.only : null;

/* ---------------- 解析 playwright ---------------- */
function resolvePlaywright() {
  const names = ['playwright-core', 'playwright'];
  const roots = [];
  if (process.env.PLAYWRIGHT_PATH) roots.push(process.env.PLAYWRIGHT_PATH);
  roots.push(path.resolve(__dirname, '../../../node_modules'));
  roots.push(path.resolve(__dirname, '../../node_modules'));
  roots.push(path.resolve(__dirname, '../node_modules'));
  if (process.env.NODE_PATH) {
    for (const p of process.env.NODE_PATH.split(path.delimiter)) if (p) roots.push(p);
  }
  roots.push(path.join(os.homedir(), '.workbuddy-ai', 'binaries', 'node', 'workspace', 'node_modules'));
  roots.push(path.join(os.homedir(), '.workbuddy', 'binaries', 'node', 'workspace', 'node_modules'));
  roots.push('/usr/local/lib/node_modules');
  roots.push('/opt/homebrew/lib/node_modules');

  for (const r of roots) {
    for (const n of names) {
      const p = path.join(r, n);
      try {
        return { mod: require(p), from: p };
      } catch (_) { /* 继续 */ }
    }
  }
  return null;
}

/* ---------------- 启动浏览器（带兜底链） ---------------- */
async function launch(chromium) {
  const attempts = [
    ['系统 Chrome', { channel: 'chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] }],
    ['系统 Edge', { channel: 'msedge', args: ['--no-sandbox', '--disable-dev-shm-usage'] }],
    ['自带 chromium', { args: ['--no-sandbox', '--disable-dev-shm-usage'] }],
  ];
  const errors = [];
  for (const [label, opts] of attempts) {
    try {
      const browser = await chromium.launch({ headless: true, ...opts });
      return { browser, label };
    } catch (e) {
      errors.push(`${label}: ${String(e).split('\n')[0]}`);
    }
  }
  throw new Error('所有浏览器都启动失败：\n  ' + errors.join('\n  '));
}

/* ---------------- 主流程 ---------------- */
(async () => {
  const indexHtml = path.join(taskDir, 'index.html');
  if (!fs.existsSync(indexHtml)) {
    console.error(`✗ 找不到 ${indexHtml}`);
    process.exit(1);
  }

  const found = resolvePlaywright();
  if (!found) {
    console.error('✗ 找不到 playwright / playwright-core。');
    console.error('  可设置 PLAYWRIGHT_PATH 指向包含 playwright-core 的 node_modules 目录。');
    process.exit(1);
  }

  const outDir = path.join(taskDir, outDirName);
  fs.mkdirSync(outDir, { recursive: true });

  const { browser, label } = await launch(found.mod.chromium);
  console.log(`浏览器：${label}`);

  const page = await browser.newPage({
    deviceScaleFactor: scale,
    viewport: { width: 2200, height: 1600 },
  });
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(String(e)));

  await page.goto('file://' + indexHtml, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(120);

  const posters = await page.$$('.poster');
  if (!posters.length) {
    console.error('✗ 页面里没有任何 <section class="poster">');
    await browser.close();
    process.exit(1);
  }

  let n = 0;
  const written = [];
  for (let i = 0; i < posters.length; i++) {
    const el = posters[i];
    const meta = await el.evaluate((node, idx) => {
      const name = node.getAttribute('data-name');
      const cls = node.className;
      const size = cls.includes('wide') ? 'wide' : cls.includes('square') ? 'square' : cls.includes('long') ? 'long' : '3:4';
      const r = node.getBoundingClientRect();
      return { name, size, w: Math.round(r.width), h: Math.round(r.height) };
    }, i);

    const base = meta.name || String(i + 1).padStart(2, '0');
    if (only && base !== only) continue;

    const file = path.join(outDir, `${base}.png`);
    await el.scrollIntoViewIfNeeded();
    await el.screenshot({ path: file, type: 'png' });
    const kb = (fs.statSync(file).size / 1024).toFixed(1);
    written.push(base);
    /* 报「输出像素」，不是画板 CSS 尺寸——--scale=2 时两者差一倍，
       报错口径会让人以为文件只有画板那么大。非 1x 时补注画板尺寸。 */
    const ow = Math.round(meta.w * scale);
    const oh = Math.round(meta.h * scale);
    const note = scale === 1 ? '' : `（画板 ${meta.w}×${meta.h}）`;
    console.log(`  ✓ ${base}.png   ${ow}×${oh} @${scale}x${note}   ${kb} KB   [${meta.size}]`);
    n++;
  }

  await browser.close();

  if (pageErrors.length) {
    console.log(`\n⚠ 页面报错 ${pageErrors.length} 条：`);
    for (const e of pageErrors.slice(0, 5)) console.log('   ' + e);
  }
  console.log(`\n完成：${n} 张 → ${path.relative(process.cwd(), outDir)}/`);
  if (!n) process.exit(1);
})().catch((e) => {
  console.error('✗ 渲染失败：' + e.message);
  console.error('  兜底：把 index.html 交给用户在浏览器里打开导出，或至少交付 HTML 源文件。');
  process.exit(1);
});
