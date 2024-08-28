import argparse
from hackernews_summary import HackerNewsSummary  # 确保该模块存在
from hackernews_scraper import HackerNewsScraper  # 确保HackerNewsScraper已定义在scraper.py文件中

def print_usage():
    """打印使用说明"""
    usage_info = """
    使用说明:
    -----------------------
    1. 获取热门故事: fetch 
    2. 生成趋势分析报告: summarize
    3. 退出: exit
    -----------------------
    请根据指示输入命令。
    """
    print(usage_info)

def main():
    # 创建 HackerNewsSummary 实例
    summary_generator = HackerNewsSummary()  # 假设这个类存在并可以用于生成总结
    scraper = HackerNewsScraper(summary_generator)  # 注入实例

    while True:
        print_usage()  # 打印使用说明
        command = input("请输入命令: ").strip().lower()  # 获取用户输入并转为小写

        if command == 'fetch':
            print("Fetching top stories from Hacker News...")
            stories = scraper.top_stories()
            if stories:
                for idx, story in enumerate(stories, start=1):
                    print(f"{idx}. {story['title']} (链接: {story['link']})")
            else:
                print("没有找到热门故事。")

        elif command == 'summarize':
            print("Generating Hacker News summary...")
            scraper.summarize_hackernews()
            print("Summary generated and saved to file.")

        elif command == 'exit':
            print("退出程序。")
            break  # 退出循环

        else:
            print("无效命令，请重试。")

if __name__ == "__main__":
    main()
