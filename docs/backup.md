---
title: 环境配置指南
status: new
---

=== "软件清单"

- **Python 3.10+**
- **git**
- **git-crypt**
- **MkDocs MkDocs-Material**
- **文本编辑器**（推荐 VSCode）

## 安装步骤

cgy或者你们的学姐学长会提供一个压缩包，里面包含了上述所有环境的安装包和配置脚本，下载解压后直接运行 `setup.bat` 即可完成环境配置（不包括 python 噢，pip依赖问题自己解决） :smile:

!!! tip "手动配置"
    如果你想自己手动配置环境，下载上述软件并安装，配置好环境变量即可（不会就去问AI）

## 配置 Git 

### 注册 Github 账号
如果你还没有 Github 账号，先去 [Github 官网](https://github.com/join) 注册一个新账号

!!! warning "网络问题"
    中国大陆网络可能有点慢或受限，建议使用 VPN 或者加速器解决

### 配置 Git 用户信息

打开命令行终端，执行以下命令配置

```bash
git config --global user.name "你的Github用户名"
git config --global user.email "你的Github注册邮箱"
```


## 配置 VSCode

安装并打开 VSCode，按下 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>X</kbd> 打开扩展市场，搜索并安装以下扩展：

- **Markdown All in One**
- **Markdown Preview Enhanced** (可选，用于增强 Markdown 预览功能)
- **Python**

安装完成后，重启 VSCode 以确保扩展生效。

## 初始化目录

!!! warning
    确保 cgy 已经把你拉入了仓库的 Collaborators 中，否则以下操作会受限！


新建一个目录，比如`D:/lab512`，在该目录下右键空白处，选择“使用终端打开”（或者在vscode中直接打开该目录），执行以下命令初始化我们的文档项目：

```bash
git clone https://github.com/gailunzhou/512Docs
```

执行完成后，`D:/lab512` 目录下会多出一个 `512Docs` 目录，进入该目录：








