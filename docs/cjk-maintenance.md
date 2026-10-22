# CJK 强调维护分支

## 来源与边界

基于 swiftlang/swift-cmark 正式 0.9.0（08ddb528923cc1a6527e02b7a1aee9e516ca749a）。计划发布本维护分支 0.9.1，目前未发布。它与官方包 identity/module/C 符号相同，是互斥替代，不能在同一个依赖图并存。

仅添加 `CMARK_OPT_CJK_FRIENDLY_EMPHASIS`（bit 22）控制的 delimiter flanking 分类；不修改匹配栈、原文或来源位置。默认关闭。CLI 对应 `--cjk-friendly-emphasis`。不改变删除线扩展。

规则依据 [markdown-cjk-friendly 固定提案](https://github.com/tats-u/markdown-cjk-friendly/blob/71d6b25d406a31d0303b102d582bd675067ed73f/specification.md)，这是社区扩展而不是 CommonMark 标准。本文为独立摘要；未复制规范正文。代码用例的 MIT 许可证保存在 test/cjk-fixtures/LICENSE；Unicode 数据许可证保存在 tools/cjk-data/18.0.0/LICENSE.txt。

Unicode 18 数据、固定 URL 与 SHA256 在 tools/cjk-data/manifest.json。生成器不读取主机 Unicode 数据、不联网，`python3 tools/generate-cjk-tables.py --check` 校验输入及输出。CommonMark 空白只含 Zs 与 TAB/LF/FF/CR，不能误用 Unicode White_Space。

## 验证

```sh
swift build --product cmark-gfm-bin
swift build --product api_test
.build/debug/api_test
python3 test/spec_tests.py --program .build/debug/cmark-gfm-bin --spec test/spec.txt
python3 test/cjk_contract_test.py .build/debug/cmark-gfm-bin
python3 tools/generate-cjk-tables.py --check
```

本地结果：严格规范 670 项；API 815 项（包括多字节中间分段、非法 UTF8 清洗、原文来源位置）；7 项明确行为、5 个社区 golden 文件、非 CJK GFM 开关一致、10 万字符 delimiter 有界验证通过。不会将这些结果称作 Swift 桥接或 App 验证。

## 上游维护

上游安全修复优先合入，并重新执行以上门禁、Swift 桥接以及下游平台测试。每次 Unicode 更新须显式更新 manifest、生成区间和分类负例。禁止覆盖已发布 tag。上游原生支持等价选项后，在明确版本迁移中切回官方 URL；不静默更换同 identity 的远程来源。

## 第一轮代码评审处置

独立 checkpoint 评审 REVISE，未发现 flanking 分类实现偏离，但指出三项验证缺口。已改为显式异常校验 manifest/输入/输出，python -O 不会移除发布门禁；PropList.White_Space 与 Zs+四项 CommonMark 空白做独立集合交叉校验；增加 FE00–FE0E、FE0F、IVS 和未分配宽字符 U+2A6E0 的明确 HTML 断言。

旧生成器在 -O 下对损坏表仍退出 0 的问题已复现（/tmp/cjk-generator-red-evidence.log）。新门禁损坏版本、SHA、输出三种场景均拒绝；25 项明确行为及既有 golden/GFM/长 delimiter 通过。生成的 C 表和运行时 C 实现未改变，先前 API/规范运行结果可复用。
