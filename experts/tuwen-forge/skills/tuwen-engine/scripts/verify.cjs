#!/usr/bin/env node
/**
 * verify.cjs — 排版质检闸门（真实 DOM 测量，不是静态扫描）
 *
 * 用法：
 *   node scripts/verify.cjs <任务目录>
 *
 * 规则：
 *   R1 overflow        元素超出画板              error
 *   R2 footer-collision 内容压到页脚              error
 *   R3 min-font        正文小于 24px              error
 *   R4 band-density    画板高≥900 时纵向切 4 横带，有空带   warn
 *   R5 line-cap        标题行数超预算             error
 *   R6 title-gap       标题与下一块贴太近          warn
 *   R7 bottom-void     底部留白 > 22% 且未被 .allow-void 覆盖   warn
 *   R8 orphan-line     末行只剩一个字（孤字）        warn
 *
 * 有 error → 不得交付。只有 warn → 可交付，但交付说明里要逐条讲。
 * 脚本跑不起来 → 如实说「本次只做了人工核对」，走 references/qa-checklist.md 的人工清单。
 */
'use strict';

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const taskDir = process.argv[2] ? path.resolve(process.argv[2]) : null;
if (!taskDir) {
  console.error('用法：node scripts/verify.cjs <任务目录>');
  process.exit(2);
}

function resolvePlaywright() {
  const names = ['playwright-core', 'playwright'];
  const roots = [];
  if (process.env.PLAYWRIGHT_PATH) roots.push(process.env.PLAYWRIGHT_PATH);
  roots.push(path.resolve(__dirname, '../../../node_modules'));
  roots.push(path.resolve(__dirname, '../../node_modules'));
  roots.push(path.resolve(__dirname, '../node_modules'));
  if (process.env.NODE_PATH) for (const p of process.env.NODE_PATH.split(path.delimiter)) if (p) roots.push(p);
  roots.push(path.join(os.homedir(), '.workbuddy-ai', 'binaries', 'node', 'workspace', 'node_modules'));
  roots.push(path.join(os.homedir(), '.workbuddy', 'binaries', 'node', 'workspace', 'node_modules'));
  roots.push('/usr/local/lib/node_modules');
  roots.push('/opt/homebrew/lib/node_modules');
  for (const r of roots) for (const n of names) {
    try { return { mod: require(path.join(r, n)), from: path.join(r, n) }; } catch (_) {}
  }
  return null;
}

async function launch(chromium) {
  const attempts = [
    ['系统 Chrome', { channel: 'chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] }],
    ['系统 Edge', { channel: 'msedge', args: ['--no-sandbox', '--disable-dev-shm-usage'] }],
    ['自带 chromium', { args: ['--no-sandbox', '--disable-dev-shm-usage'] }],
  ];
  const errors = [];
  for (const [label, opts] of attempts) {
    try { return { browser: await chromium.launch({ headless: true, ...opts }), label }; }
    catch (e) { errors.push(`${label}: ${String(e).split('\n')[0]}`); }
  }
  throw new Error('所有浏览器都启动失败：\n  ' + errors.join('\n  '));
}

const MEASURE = () => {
  // 正文最小 24px。豁免：页脚（页码/署名）与 .caption（来源、注脚）
  const R3_EXEMPT = new Set(['caption']);
  const HEAD_SEL = '.h-display, .h-xl, .h-lg, .h-md, .h-statement, .block-title';
  const HEAD_CAP = [
    ['.h-display', 88, 3], ['.h-statement', 72, 4], ['.h-xl', 56, 4], ['.h-lg', 40, 5], ['.h-md', 0, 6], ['.block-title', 0, 4],
  ];

  const tagOf = (el) => {
    const cls = (el.className && typeof el.className === 'string') ? el.className.split(/\s+/).filter(Boolean)[0] : '';
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 18);
    return `<${el.tagName.toLowerCase()}${cls ? '.' + cls : ''}>「${t}」`;
  };

  const posters = [...document.querySelectorAll('.poster')];
  return posters.map((poster, idx) => {
    const pr = poster.getBoundingClientRect();
    const H = pr.height, W = pr.width;
    const name = poster.getAttribute('data-name') || String(idx + 1).padStart(2, '0');
    const issues = [];
    const all = [...poster.querySelectorAll('*')];

    const textEls = all.filter((el) =>
      [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length)
    );
    // 页脚（页码/署名）是固定装饰，不算「内容」——否则底部空洞永远测不出来
    const bodyTextEls = textEls.filter((el) => !el.closest('.poster-footer'));
    const voids = all.filter((el) => el.classList.contains('allow-void'));
    const voidRects = voids.map((v) => v.getBoundingClientRect());

    /* ---- R1 overflow ---- */
    for (const el of all) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) continue;
      const over = Math.max(r.right - pr.right, r.bottom - pr.bottom, pr.left - r.left, pr.top - r.top);
      if (over > 2) {
        issues.push({ rule: 'R1', level: 'error', msg: `${tagOf(el)} 超出画板 ${Math.round(over)}px` });
      }
    }

    /* ---- R2 footer-collision ---- */
    const body = poster.querySelector('.poster-body');
    const footer = poster.querySelector('.poster-footer');
    if (body && footer) {
      const bb = body.getBoundingClientRect(), fb = footer.getBoundingClientRect();
      if (bb.bottom > fb.top + 1) {
        issues.push({ rule: 'R2', level: 'error', msg: `内容区压到页脚 ${Math.round(bb.bottom - fb.top)}px` });
      }
    }

    /* ---- R3 min-font ---- */
    for (const el of textEls) {
      if (el.closest('.poster-footer')) continue;
      if ([...el.classList].some((c) => R3_EXEMPT.has(c))) continue;
      const fs2 = parseFloat(getComputedStyle(el).fontSize);
      if (fs2 && fs2 < 24) {
        issues.push({ rule: 'R3', level: 'error', msg: `${tagOf(el)} 字号 ${fs2}px < 24px（正文下限 24px；来源/注脚请加 .caption）` });
      }
    }

    /* ---- R4 band-density ---- */
    if (H >= 900) {
      const BANDS = 4, bh = H / BANDS;
      for (let b = 0; b < BANDS; b++) {
        const top = pr.top + b * bh, bot = top + bh;
        const hasText = bodyTextEls.some((el) => {
          const r = el.getBoundingClientRect();
          return r.height > 0 && r.bottom > top + 2 && r.top < bot - 2;
        });
        if (hasText) continue;
        const hasVoid = voidRects.some((r) => r.height > 0 && r.bottom > top + 2 && r.top < bot - 2);
        if (!hasVoid) {
          issues.push({ rule: 'R4', level: 'warn', msg: `第 ${b + 1}/${BANDS} 横带（${Math.round(b * bh)}–${Math.round(bot - pr.top)}px）既无内容也无 .allow-void` });
        }
      }
    }

    /* ---- R5 line-cap ---- */
    for (const el of poster.querySelectorAll(HEAD_SEL)) {
      const cs = getComputedStyle(el);
      const fs2 = parseFloat(cs.fontSize);
      const lh = cs.lineHeight === 'normal' ? fs2 * 1.2 : parseFloat(cs.lineHeight);
      const lines = Math.max(1, Math.round(el.getBoundingClientRect().height / lh));
      const cls = [...el.classList].find((c) => c.startsWith('h-') || c === 'block-title') || '';
      const capEntry = HEAD_CAP.find(([c]) => el.classList.contains(c.slice(1)));
      const cap = capEntry ? capEntry[2] : 6;
      if (lines > cap) {
        issues.push({ rule: 'R5', level: 'error', msg: `${tagOf(el)} 占 ${lines} 行，上限 ${cap} 行（.${cls} ${fs2}px）` });
      }
    }

    /* ---- R6 title-gap ---- */
    for (const el of poster.querySelectorAll(HEAD_SEL)) {
      const next = el.nextElementSibling;
      if (!next || !next.getBoundingClientRect().height) continue;
      const gap = next.getBoundingClientRect().top - el.getBoundingClientRect().bottom;
      if (gap >= 0 && gap < 24) {
        issues.push({ rule: 'R6', level: 'warn', msg: `${tagOf(el)} 与下一块间距仅 ${Math.round(gap)}px（建议 ≥ 24px）` });
      }
    }

    /* ---- R7 bottom-void（区域级判据） ---- */
    // 早期版本用 `!voids.length` 做抑制条件，即「页面上任意位置有一个 .allow-void
    // 就整页跳过 R7」——粒度太粗：顶部有个小呼吸区标记、底部却有意外的空洞时，
    // 底部空洞会被一并放过。现在改成只在该空洞**确实被标记覆盖**时才沉默。
    // voidPx 的算法保持不变（仍是 pr.bottom - lastBottom），所以阈值语义与旧版一致。
    if (bodyTextEls.length) {
      const lastBottom = Math.max(...bodyTextEls.map((el) => el.getBoundingClientRect().bottom));
      const voidPx = pr.bottom - lastBottom;
      if (voidPx > H * 0.22) {
        const span = pr.bottom - lastBottom;
        const covered = voidRects.some((r) => {
          if (r.height <= 0) return false;
          const overlap = Math.min(r.bottom, pr.bottom) - Math.max(r.top, lastBottom);
          return overlap > 0 && overlap >= span * 0.5;
        });
        if (!covered) {
          const why = voids.length
            ? '页面上虽有 .allow-void，但没有覆盖到这片空洞'
            : '且未标记 .allow-void';
          issues.push({
            rule: 'R7',
            level: 'warn',
            msg: `底部留白 ${Math.round(voidPx)}px（画板高 ${Math.round(H)}px 的 ${Math.round((voidPx / H) * 100)}%），${why}`,
          });
        }
      }
    }

    /* ---- R8 orphan-line（孤字/寡行） ---- */
    // 中文排版里「末行只剩一个字」最扎眼，靠肉眼才看得出——这里用 Range 逐行测量把它自动化。
    // 手段：range.getClientRects() 拿到每个行盒；再二分查找「最后一行从第几个字符开始」。
    for (const el of bodyTextEls) {
      const node = [...el.childNodes].find((n) => n.nodeType === 3 && n.textContent.trim().length >= 4);
      if (!node) continue;
      const txt = node.textContent;
      if (txt.trim().length < 8) continue;
      try {
        const whole = document.createRange();
        whole.selectNodeContents(node);
        const lineRects = [...whole.getClientRects()].filter((x) => x.width > 0.5 && x.height > 0.5);
        if (lineRects.length < 2) continue;
        const lastTop = lineRects[lineRects.length - 1].top;
        let lo = 0, hi = txt.length;
        while (lo < hi) {
          const mid = (lo + hi) >> 1;
          const rr = document.createRange();
          rr.setStart(node, mid);
          rr.setEnd(node, mid + 1);
          if (rr.getBoundingClientRect().top >= lastTop - 1) hi = mid;
          else lo = mid + 1;
        }
        const onLast = txt.length - lo;
        if (onLast <= 1) {
          issues.push({
            rule: 'R8',
            level: 'warn',
            msg: `${tagOf(el)} 末行仅 ${onLast} 字（孤字），共 ${lineRects.length} 行；建议加 text-wrap:pretty 或改写文案`,
          });
        }
      } catch (_) { /* Range 在某些节点上不可用，跳过即可，不影响其余规则 */ }
    }

    return { name, w: Math.round(W), h: Math.round(H), theme: poster.getAttribute('data-theme') || '(未设)', issues };
  });
};

(async () => {
  const indexHtml = path.join(taskDir, 'index.html');
  if (!fs.existsSync(indexHtml)) { console.error(`✗ 找不到 ${indexHtml}`); process.exit(1); }

  const found = resolvePlaywright();
  if (!found) {
    console.error('✗ 找不到 playwright / playwright-core。设置 PLAYWRIGHT_PATH 后重试，或改走人工清单。');
    process.exit(1);
  }

  const { browser, label } = await launch(found.mod.chromium);
  const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width: 2200, height: 1600 } });
  await page.goto('file://' + indexHtml, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(80);

  // 前置检查
  const pre = await page.evaluate(() => ({
    posters: document.querySelectorAll('.poster').length,
    external: [...document.querySelectorAll('link[rel=stylesheet],script[src]')].map((e) => e.getAttribute('href') || e.getAttribute('src')),
  }));
  if (!pre.posters) { console.error('✗ 页面里没有任何 <section class="poster">'); await browser.close(); process.exit(1); }
  if (pre.external.length) console.log(`⚠ 引用了外部资源（必须单文件）：${pre.external.join(', ')}\n`);

  const report = await page.evaluate(MEASURE);
  await browser.close();

  let errors = 0, warns = 0;
  for (const p of report) {
    const errs = p.issues.filter((i) => i.level === 'error');
    const wns = p.issues.filter((i) => i.level === 'warn');
    errors += errs.length; warns += wns.length;
    const mark = errs.length ? '✗' : wns.length ? '⚠' : '✓';
    console.log(`${mark} ${p.name}   ${p.w}×${p.h}   theme=${p.theme}`);
    for (const i of [...errs, ...wns]) {
      console.log(`    [${i.level}] ${i.rule}  ${i.msg}`);
    }
  }
  console.log(`\n浏览器：${label}`);
  console.log(`共 ${report.length} 张画板：${errors} 个 error，${warns} 个 warn`);
  if (errors) console.log('→ 有 error，**不得交付**，先修再跑。');
  else if (warns) console.log('→ 只有 warn，可交付，但交付说明里要逐条讲清。');
  else console.log('→ 全部通过。');
  process.exit(errors ? 1 : 0);
})().catch((e) => {
  console.error('✗ 质检脚本运行失败：' + e.message);
  console.error('  兜底：走 references/qa-checklist.md 的人工清单，并在交付说明里写明「本次未跑自动质检」。');
  process.exit(1);
});
