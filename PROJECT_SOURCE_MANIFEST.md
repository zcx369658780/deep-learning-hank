# 项目源导出与替换清单

路线：`DLH-WL-V1-20260918`。日期：2026-09-18。
GitHub 是仓库事实来源，项目源是文档发布提交的镜像。包内外部 `SOURCE_EXPORT_MANIFEST.json` 记录实际发布 SHA、每个导出文件的 repository path、Git blob、SHA-256 和包路径；不要求本文写自身 commit SHA。

## 当前上传集合

AGENTS、README_START_HERE、规则索引及所有必读规则、Owner dated decision、路线锁 manifest、主路线图、Task Index、Startup Snapshot、家庭合同、W^L 合同、DSH 同步协议/短入口、当前会话交接。文档按 GitHub 相同字节导出到 `UPLOAD_CURRENT/`，不编辑成第二套 authority。

## 包目录

- `UPLOAD_CURRENT/`：当前权威镜像，按仓库相对路径存放；
- `REFERENCE_ONLY/`：只读方法说明及可选 Owner 原始指南，非状态权威；
- `REPLACEMENT_INSTRUCTIONS/`：旧文件→新文件替换说明、简短接续提示和发布核验记录。

原始指南不提交公共仓库，不从另一个仓库拉代码。论文/PDF/raw data/私有笔记不打进 GitHub 文档提交。

## 旧上传处理

替换旧 master-roadmap、多个 startup-snapshot、旧 task index、旧启动 prompt、旧 CURRENT 规则/交接及早期 bootstrap 压缩包。具体文件名在压缩包替换说明逐项列出。保留论文、文献、原始数据与唯一科学资料；旧操作文档可离线归档。

历史实验与 dated handoff 在 GitHub 保留，通过新入口追溯，不删除 accepted/failed evidence。上传后由 Owner 确认，再让 DSH 同步；打包完成不等于用户上传完成或 DSH 已同步。
