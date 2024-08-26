import time
import datetime
import schedule
from hackernews_scraper import HackerNewsScraper
from hackernews_summary import HackerNewsSummary
from report_generator import ReportGenerator
from logger import LOG  # 导入日志记录器


class HackerNewsDaemon:
    def __init__(self):
        self.llm = HackerNewsSummary()
        self.scraper = HackerNewsScraper(self.llm)
        self.report_generator = ReportGenerator(self.llm)

        # 设置定时任务
        #schedule.every().day.at("12:00").do(self.run_hackernews)  # 每天中午12点运行
        schedule.every().minute.do(self.run_hackernews)  # 每分钟运行

    def run_hackernews(self):
        """运行 Hacker News 抓取和报告生成."""
        LOG.info("Running Hacker News scraping and report generation.")
        
        # 执行爬虫任务
        self.scraper.summarize_hackernews()
        current_file = self.scraper.current_file
        
        # 生成报告
        self.report_generator.generate_daily_report(current_file)

    def run(self):
        """运行调度循环."""
        LOG.info("Hacker News Daemon started. Initial scraping will be performed now.")
        
        # 立即执行一次爬取任务
        self.run_hackernews()

        while True:
            schedule.run_pending()  # 运行所有待定的任务
            time.sleep(1)  # 等待一秒


def main():
    daemon = HackerNewsDaemon()  # 创建HackerNewsDaemon实例
    daemon.run()  # 启动调度循环


if __name__ == "__main__":
    main()

