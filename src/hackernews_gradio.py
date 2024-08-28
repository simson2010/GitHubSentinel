import gradio as gr
from hackernews_scraper import HackerNewsScraper
from hackernews_summary import HackerNewsSummary


llm = HackerNewsSummary()
hn = HackerNewsScraper(llm)

class HackerNewsPageData:
    def __init__(self, new_fetcher):
        self.hn = new_fetcher 
        self.markdown_height=500
    
# 获取 Hacker News 数据
    def fetch_hackernews_data(self, limit=30):

        top_stories = hn.top_stories()[:limit]  # 获取前 limit 条新闻
        articles = []

        for story in top_stories:
            if story and "title" in story and "link" in story:
                articles.append({
                    "title": story["title"],
                    "link": story["link"]
                })

        return articles

# 显示文章总结
    def display_article(self, index, articles):
        selected_article = articles[index]
        return selected_article["summary"]

pageData = HackerNewsPageData(hn)
# 抓取数据并准备 Gradio 界面
def getNews():
    md = "\n".join(f"- [{story['title']}]({story['link']})" for story in pageData.fetch_hackernews_data())
    return md 

def updatePageData(news, summary):
    news = gr.Markdown(value=getNews(), height=pageData.markdown_height)
    summary = gr.Markdown(value=hn.top_stories_summarize(), height=pageData.markdown_height)

    
# 创建 Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>Hacker News</h1>")
    
    reload_button=gr.Button(value="Refresh")
    
    with gr.Row():
        with gr.Column():
            # 左侧显示标题和链接
            
            newsList = gr.Markdown(value=getNews(), height=pageData.markdown_height )

        with gr.Column():
            # 右侧显示总结
            summary_display = gr.Markdown(value=hn.top_stories_summarize(), height=pageData.markdown_height)
    
    reload_button.click(lambda: updatePageData(newsList, summary_display))

# 启动 Gradio 应用
demo.launch()
