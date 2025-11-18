<h2 align="center">
Lab512 Docs
</h2>



<div align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/MKDOCS-Latest-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.10-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="python version"/>
<img alt="GitHub contributors" src="https://img.shields.io/github/contributors-anon/gailunzhou/512Docs?style=for-the-badge&color=%238352de">

  <img src="https://img.shields.io/github/deployments/gailunzhou/512Docs/github-pages?style=for-the-badge" alt="Deployment Status">

</div>

## 简介
神秘的 **Lab512** 的文档仓库，包含实验室的项目介绍、使用说明、技术文档等内容。使用 **MkDocs** 构建，Github Pages 托管，旨在为实验室成员阅读和参考。

访问链接: [https://gailunzhou.github.io/512Docs/](https://gailunzhou.github.io/512Docs/)

## 贡献指南

欢迎实验室成员贡献内容！请遵循以下步骤：
1. 动手前必须先阅读 [贡献指南](https://gailunzhou.github.io/512Docs/)。
2. 确保你已经掌握了 **Git** 和 **Markdown** 的基本使用方法。
3. 确保你的网络能流畅的访问 GitHub 和相关服务。

**注意: 禁止直接在 Github 上编写文档！！！ 请在本地使用编辑器（如 VSCode）编写和预览文档，然后通过 Git 提交和推送。否则 commits 记录会非常混乱😅**

## 敏感信息说明

实验室相关敏感信息，特别是涉及个人隐私的内容，请务必进行脱敏处理。
如需加密内容或文件，请统一存放至 `docs/secret-files/` 目录。正确配置后，在 Push 到远程仓库前系统将执行自动加密，拉取至本地时则会自动解密。

注意： 只有拥有 **.labsecret** 密钥文件的用户才能查看加密文件内容（详见[敏感信息处理说明](https://gailunzhou.github.io/512Docs/secret-note/secret-note)），否则你只能看到加密后的 RAW 文件。

> 如需获取该密钥文件，请联系学姐、学长或老师获取，并将其正确配置于本地环境中。