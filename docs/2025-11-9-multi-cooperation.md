<div class="article-meta" style="background: #f0f8ff; padding: 15px; border-left: 4px solid #2196f3; margin-bottom: 20px; border-radius: 4px;">
<p style="margin: 0; color: #666; font-size: 0.9em;">
<strong>📅 发布日期:</strong> 2025-11-09 &nbsp;|&nbsp;
<strong>👤 作者:</strong> CCChiJi &nbsp;|&nbsp;
<strong>📁 分类:</strong> 技术笔记 &nbsp;|&nbsp;
<strong>🏷️ 标签:</strong> 多人协作
</p>
</div>

# 多人协作搭建文章网站操作指南

要实现多人协作添加文章到网站，可按以下步骤操作，并遵循文档格式规范：

## 一、多人协作加入仓库的具体步骤

### 1. 仓库管理者（你）的操作

#### （1）在 GitHub 仓库中添加协作者



* 进入你的 GitHub 仓库（如 `xxx.github.io`）→ 点击顶部 `Settings` → 左侧菜单 `Collaborators` → 点击 `Add people`。

![cooperation01](images/2025-11-9-multi-cooperation/cooperation01.png)

* 输入协作者的 GitHub 用户名或邮箱，点击搜索并选择对应用户（权限默认为writer）。

* 协作者会收到邮件邀请，接受后即可获得仓库操作权限。

#### （2）告知协作者仓库地址



* 仓库地址格式：`https://github.com/``你的用户名/你的仓库名.git`（可在仓库主页点击 `Code` 按钮复制）。

![cooperation02](images/2025-11-9-multi-cooperation/cooperation02.png)

### 2. 协作者（其他人）的操作

#### （1）克隆仓库到本地

选取一个位置创建一个文件夹用来存放仓库内的文件

用VScode打开文件夹并开启终端 *（确保当前路径为所创建的文件夹下）*，执行以下命令（替换仓库地址为邀请者发送的地址）：



```bash
#克隆仓库到本地

git clone https://github.com/邀请者的用户名/邀请者的仓库名.git

#进入仓库文件夹

cd 你的仓库名
```

#### （2）推送前需知

* 查看mkdocs.yml文件中的 **nav （网站导航结构）** 部分中导航栏结构

![cooperation03](images/2025-11-9-multi-cooperation/cooperation03.png)

* 根据自己所写文章类别添加到对应栏位内并保存，如果没有对应类别，可添加 *(添加前最好联系一下管理员，即邀请者)*

![cooperation04](images/2025-11-9-multi-cooperation/cooperation04.png)


#### （3）日常写文章并推送流程



```bash
#1. 每次写文章前，先拉取远程最新内容（避免冲突）
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#非常重要

git pull origin main

#2. 在本地仓库的 source/\_posts 文件夹中，新建 .md 文件写文章

（文件名建议用英文/数字+连字符，如：2025-11-09-study-notes.md）

#3. 提交修改到本地仓库

git add .  # 添加所有新文件/修改

git commit -m "新增文章：xxx标题"  # 备注清晰的提交说明

#4. 推送到远程仓库（自动更新网站）

git push origin main
```

#### （4）冲突处理（若多人同时修改同一文件）



* 推送时若提示冲突，先执行 `git pull origin main`，会自动合并或提示冲突位置。

* 打开冲突文件，找到 `<<<<<<< HEAD`（你的修改）和 `>>>>>>> 远程分支`（他人修改），手动编辑保留正确内容，删除冲突标记。

* 再执行 `git add .` → `git commit -m "解决冲突"` → `git push origin main`。


### 3. 预览检查



* 本地写完后，可在仓库文件夹执行 `hexo serve`或`hexo s`，本地预览效果，确认格式无误后再推送。


