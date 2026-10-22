# CJK 回归用例来源

Markdown 输入来自 tats-u/markdown-cjk-friendly commit 71d6b25d406a31d0303b102d582bd675067ed73f；保留同目录 MIT LICENSE。
HTML 预期由 markdown-it 15.0.3 + markdown-it-cjk-friendly 3.0.0 默认 html:true 生成，并与本实现逐项对照。它们是辅助差分用例，Unicode 分类仍以固定提案和 Unicode 18 数据为准，不以宿主 JS 的 Unicode 版本覆盖规范。
gfm-non-cjk 的删除线语法与标签输出因引擎不同而不同，该文件只比较本引擎选项开/关是否一致，不强行对齐 markdown-it。
