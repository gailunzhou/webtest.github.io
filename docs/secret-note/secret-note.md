---lab
author: teriyakisushi
category:
tags: secret-note git-crypt
---

# 敏感信息处理说明

先按照基础指南第一篇文章[环境配置](../basic/2025-11-8-firstDeploy.md) 完成 **git + git-crypt** 的环境配置。

## git-crypt 初始化

在文档项目的根目录执行

```bash
git-crypt init
```

## 获取加密密钥
将 `.labsecret` 文件添加到根目录中（这个文件找cgy或者老师获取）
 
添加完后的目录结构应该是这样的：

 ![](images/local.png)

随后执行

```bash
git-crypt unlock .labsecret
``` 

以上操作完成后，你应该就能看到 `docs/secret-files/` 目录下的明文内容了，打开 `docs/secret-files/secret-test.txt` 文件确认一下🤭

## 添加敏感信息文件

!!! warning
    在上传敏感信息或文件前，一定要将其放置在 `docs/secret-files` 目录下, git-crypt 会自动对该目录下的文件进行加密处理

!!! danger "严重警告"
    不要将 `.labsecret` 文件上传到远程仓库！一定要确保 `.labsecret` 文件已被添加到 `.gitignore` 文件中!

如果你想自定义其他目录或文件的加密规则，可以编辑项目根目录下的 `.gitattributes` 文件，添加相应的路径和加密规则。例如：

=== ".gitattributes"
    ```text
    # 将所有 .secret 结尾的文件进行加密
    *.secret filter=git-crypt diff=git-crypt

    # 将所有 panz 开头的文件进行加密（如 panz001.txt）
    panz* filter=git-crypt diff=git-crypt

    # 将 docs/confidential 目录下的所有文件进行加密
    docs/confidential/** filter=git-crypt diff=git-crypt
    ```
> 匹配规则和 `.gitignore` 文件类似，不懂就去问 AI 💀

## 说明

以上流程只需执行一次，后续在该项目中 Push 或 Pull 时，git-crypt 会自动处理加密和解密操作。上传敏感文件后，请在仓库中二次确认该文件已被加密（查看 GitHub 上的 RAW 文件内容，应该是乱码），若有疏忽请及时处理！



