/**
 * Univer 嵌入快速起步（示意）
 * 对应 dream-num/univer：面向开发者的 SDK，可在内部工具里嵌入
 * 表格 / 文档 / 幻灯片 编辑能力。
 *
 * ⚠️ Univer API 迭代较快，下方为「预设（presets）」风格的示意写法，
 *    实际包名、导入路径、初始化参数请以官方最新文档为准：
 *    https://docs.univer.ai / https://github.com/dream-num/univer
 *
 * 前置：npm i @univerjs/presets @univerjs/core ...
 */

import {
  createUniver,
  defaultTheme,
  LocaleType,
  merge,
  type FUniver,
} from '@univerjs/presets';
import { UniverSheetsCorePreset } from '@univerjs/presets/preset-sheets-core';
import { UniverUiPreset } from '@univerjs/presets/preset-ui';
import designEnUS from '@univerjs/presets/preset-sheets-core/locales/en-US';
import designZhCN from '@univerjs/presets/preset-sheets-core/locales/zh-CN';
import uiEnUS from '@univerjs/presets/preset-ui/locales/en-US';
import uiZhCN from '@univerjs/presets/preset-ui/locales/zh-CN';
import '@univerjs/presets/lib/styles/preset-sheets-core.css';

const container = document.getElementById('app')!;

// 1) 创建 Univer 实例并挂载 UI 预设到容器
const { univer, workbook }: { univer: FUniver; workbook: unknown } = createUniver({
  locale: LocaleType.ZH_CN,
  locales: {
    [LocaleType.EN_US]: merge({}, designEnUS, uiEnUS),
    [LocaleType.ZH_CN]: merge({}, designZhCN, uiZhCN),
  },
  theme: defaultTheme,
  presets: [
    UniverSheetsCorePreset(),
    UniverUiPreset({ container: 'app' }),
  ],
});

// 2) 新建一个空表格（或用 load 加载已有数据）
univer.createUnit(/* UniverInstanceType.UNIVER_SHEET */ 2, {
  id: 'sheet-demo',
  name: '内部数据表',
  sheetOrder: ['sheet-1'],
  sheets: {
    'sheet-1': {
      id: 'sheet-1',
      name: 'Sheet1',
      cellData: {
        0: { 0: { v: '姓名' }, 1: { v: '金额' } },
        1: { 0: { v: '张三' }, 1: { v: 1280 } },
      },
    },
  },
});

// 3) 与业务系统对接的常用钩子（示意）
// - 监听内容变化，自动存草稿到后端
// - 用 univer.getData() 序列化，落库；打开时 load 还原
// - 权限：按当前登录用户决定是否允许编辑某 sheet

export { univer, workbook };
