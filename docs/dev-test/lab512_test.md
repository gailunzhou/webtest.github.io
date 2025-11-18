---lab
date: 1999-12-31
author: teriyakisushi
category: dev-test
tags: dev-test
---

# Lab512 Plugin Testing Area

头部meta信息应该渲染出来了，在原始markdown文件中是这样写的:

=== "lab512_test.md"
    ```text
    ---lab
    date: 1999-12-31
    author: teriyakisushi
    category: dev-test
    tags: dev-test
    ---
    ```

其中 `date` 为空的话会显示 $current_time，其他字段为空则默认不显示，