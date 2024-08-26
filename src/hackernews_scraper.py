import os
import requests
from bs4 import BeautifulSoup  # 确保导入BeautifulSoup用于HTML解析
from datetime import datetime  # 导入datetime模块以获取当前日期
from hackernews_summary import HackerNewsSummary  # 导入HackerNewsSummary类
from logger import LOG  # 导入日志模块

class HackerNewsScraper:
    def __init__(self, summary_generator):
        self.url = 'https://news.ycombinator.com/'
        # 设置浏览器的 header 和 referer
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Referer': 'https://news.ycombinator.com/',
        }
        self.summary_generator = summary_generator  # 注入HackerNewsSummary实例

    def fetch_top_stories(self):
        """获取 Hacker News 的热门帖子."""
        response = requests.get(self.url, headers=self.headers)
        
        if response.status_code == 200:
            return self.parse_stories(response.text)
        else:
            LOG.info(f"Error fetching page: {response.status_code}")
            return []

    def parse_stories(self, html):
        """解析 HTML 内容并提取故事标题和链接."""
        stories = []
        soup = BeautifulSoup(html, 'html.parser')

        # 使用新的选择器 .titleline > a
        for item in soup.select('.titleline > a'):
            title = item.get_text()
            link = item['href']
            stories.append({'title': title, 'link': link})
        
        return stories

    def write_to_file(self, content):
        """将获取到的内容写入指定的文件."""
        # 创建目标文件夹（如果不存在）
        directory = "daily_progress/hacker_news"
        os.makedirs(directory, exist_ok=True)  # 创建文件夹，若已存在则不报错
        
        # 获取当前日期并格式化为isodate
        current_date = datetime.now().isoformat().replace(":","_")
        output_filename = f"hackernews_content_{current_date}.md"  # 文件名包含日期
        
        # 写入文件
        full_file_path = os.path.join(directory, output_filename)
        self.current_file = full_file_path
        with open(full_file_path, "w", encoding='utf-8') as file:
            file.write(content)
        LOG.info(f"Content written to {full_file_path}")

    def summarize_hackernews(self):
        """获取网站数据并生成总结."""
        titles = self.fetch_top_stories()
        # 将标题格式化为Markdown风格
        markdown_content = "\n".join(f"- [{story['title']}]({story['link']})" for story in titles)

        # 调用HackerNewsSummary生成总结
        # summary = self.summary_generator.generate_daily_report(markdown_content)
        
        # 写入获取到的内容到文件
        self.write_to_file(markdown_content)
        
        # print("Hacker News Summary:\n")
        # print(summary)

# 使用示例
if __name__ == "__main__":
    #API_KEY = "YOUR_API_KEY_HERE"  # 替换为您自己的 GPT-4o API 密钥
    summary_generator = HackerNewsSummary()  # 创建HackerNewsSummary实例
    scraper = HackerNewsScraper(summary_generator)  # 注入实例
    scraper.summarize_hackernews()  # 生成总结并输出
