# 光照公平性参数示例

> 本文内容逐字抽取自 [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)（MIT 协议）。
> 已做：剥 frontmatter、章节 emoji 前缀归一、AI 平台品牌名中性化。未做：任何内容改写。

```typescript
// 根据肤色范围定义光照策略
const LIGHTING_PROFILES = {
  // Fitzpatrick 皮肤分型 I-II（浅色皮肤）
  light: {
    keyLight: "柔和漫射光，避免高光过曝导致面部细节丢失",
    fillRatio: "1:2（key:fill）",
    colorTemp: "5500K 自然日光",
    notes: "避免直射硬光造成的皮肤泛红"
  },
  // Fitzpatrick 分型 III-IV（中等肤色）
  medium: {
    keyLight: "45度侧光，适度对比展现面部轮廓",
    fillRatio: "1:3",
    colorTemp: "5000-5500K",
    notes: "确保颧骨和鼻梁的高光自然过渡"
  },
  // Fitzpatrick 分型 V-VI（深色皮肤）
  deep: {
    keyLight: "大面积柔光源，距离主体更近以增加光效",
    fillRatio: "1:2（减少对比度以保留暗部细节）",
    colorTemp: "4500-5000K 偏暖",
    notes: "增加反射填充光，确保面部五官清晰可见。绝不使用全局提亮——会让皮肤看起来灰蒙蒙的"
  }
};
```
