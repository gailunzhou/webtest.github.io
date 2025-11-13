import os
import re
from datetime import datetime
from mkdocs.plugins import BasePlugin
from mkdocs.exceptions import PluginError
from mkdocs.config import base, config_options as c


class LabConfig(base.Config):
    # wait for extending
    enabled = c.Type(bool, default=True)


class LabAuthorPlugin(BasePlugin[LabConfig]):
    def on_config(self, config, **kwargs):
        self.labauthor_path = os.path.join(config.config_file_path, '..', '.labauthor')
        self.labauthor_path = os.path.abspath(self.labauthor_path)

        if not os.path.exists(self.labauthor_path):
            # 自动生成模板
            with open(self.labauthor_path, 'w', encoding='utf-8') as f:
                f.write("contributor_name = Anonymous\n")
            print("⚠️  Warning: .lab file not found. Created a template for you.")
            print(f"    Please edit: {self.labauthor_path}")

        # 读取 contributor_name (位于根目录下的 .labauthor中)
        contributor = None
        with open(self.labauthor_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("contributor_name = "):
                    contributor = line[len("contributor_name = "):].strip().strip('"\'')
                    break

        if not contributor:
            raise PluginError(
                f"Could not find 'contributor_name = ...' in {self.labauthor_path}. "
                "Please ensure the file contains a valid contributor_name."
            )

        self.contributor_name = contributor
        return config

    def on_page_markdown(self, markdown, **kwargs):
        pattern = r'(?<!```)\{info\}(.*?)\s*\.\s*(.*?)\{/info\}(?!```)'
        current_time = datetime.now().strftime("%Y-%m-%d")

        def replacer(match):
            cate = match.group(1).strip()  # 分类
            tags = match.group(2).strip()  # 标签
            return f'''
            <div class="article-meta" style="background: #f0f8ff; padding: 15px; border-left: 4px solid #2196f3; margin-bottom: 20px; border-radius: 4px;">
            <p style="margin: 0; color: #666; font-size: 0.9em;">
            <strong>📅 发布日期:</strong> {current_time} &nbsp;|&nbsp;
            <strong>👤 作者:</strong> {self.contributor_name} &nbsp;|&nbsp;
            <strong>📁 分类:</strong> {cate} &nbsp;|&nbsp;
            <strong>🏷️ 标签:</strong> {tags}
            </p>
            </div>
            '''

        return re.sub(pattern, replacer, markdown, flags=re.DOTALL)
