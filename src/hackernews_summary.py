import os
import json
from datetime import datetime
from openai import OpenAI  # 导入OpenAI库用于访问GPT模型
from logger import LOG  # 导入日志模块

class HackerNewsSummary:
    def __init__(self):
        # 创建一个OpenAI客户端实例
        self.client = OpenAI()
        
        # 从TXT文件加载提示信息
        self.system_prompt = self.load_system_prompt("prompts/hackernews_system_prompt.txt")
        
        # 配置日志文件，当文件大小达到1MB时自动轮转，日志级别为DEBUG
        self.configure_logging("logs/llm_logs.log")

    def load_system_prompt(self, file_path):
        """从指定路径加载系统提示信息."""
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            LOG.error(f"Prompt file not found: {file_path}")
            raise

    def configure_logging(self, log_file_path):
        """配置日志文件."""
        LOG.add(log_file_path, rotation="1 MB", level="DEBUG")

    def generate_daily_report(self, markdown_content, dry_run=False):
        """生成每日报告，支持干运行模式."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Today is {datetime.now().date()}, and here's the daily progress: "},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            return self.handle_dry_run(messages)

        LOG.info("Starting report generation using GPT model.")
        LOG.info(messages)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # 指定使用的模型版本
                messages=messages
            )
            LOG.debug("GPT response: {}", response)
            return response.choices[0].message.content
        except Exception as e:
            LOG.error("An error occurred while generating the report: {}", e)
            raise

    def handle_dry_run(self, messages):
        """处理干运行模式，将提示信息保存到文件."""
        LOG.info("Dry run mode enabled. Saving prompt to file.")
        output_file = "daily_progress/prompt.txt"
        with open(output_file, "w+", encoding='utf-8') as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)
        LOG.debug("Prompt saved to daily_progress/prompt.txt")
        return "DRY RUN"

# 示例用法
if __name__ == "__main__":
    summary_generator = HackerNewsSummary()
    # 这里可以调用generate_daily_report方法
