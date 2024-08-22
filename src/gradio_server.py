import gradio as gr  # 导入gradio库用于创建GUI

from datetime import datetime 
from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
from logger import LOG  # 导入日志记录器

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
llm = LLM()
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)

def export_progress_by_date_range(repo, days, since, until):
    print(repo, days, since, until)

    # chnage since (milliseconds) to datetime object
    since = datetime.fromtimestamp(float(since)) 
    until = datetime.fromtimestamp(float(until)) 

    # 定义一个函数，用于导出和生成指定时间范围内项目的进展报告
    #raw_file_path = github_client.export_progress_by_date_range(repo, days)  # 导出原始数据文件路径
    raw_file_path = github_client.export_progress_by_date_range(repo, since, until)
    report, report_file_path = report_generator.generate_report_by_date_range(raw_file_path, days)  # 生成并获取报告内容及文件路径

    return report, report_file_path  # 返回报告内容和报告文件路径


# Save new subscription to file
def add_subscription(pending_url):
    subscription_manager.add_subscription(pending_url)
    subscription_manager.load_subscriptions()
    gr.Info("添加成功")
    return reload_dropdown(), gr.update(value='')
# Reload Dropdown 


# Reload Dropdown 
def reload_dropdown():
    #return gr.Dropdown(subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目")
    return gr.update(choices=subscription_manager.list_subscriptions(), value=None)

# 创建Gradio界面

with gr.Blocks() as report_tab:
    with gr.Row():
        with gr.Column(): 
            with gr.Row():
                repo = gr.Dropdown(
                    subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
                )
                days = gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：天")
                
            with gr.Row():
                since = gr.DateTime(value="now - 24h", label="Since:")
                until = gr.DateTime(value="now", label="Until:")
            runreport = gr.Button("生成报告")

        with gr.Column():
            markdown = gr.Markdown()
            fileDowload=gr.File(label="下载报告")

    runreport.click(lambda repo, days, since, until: export_progress_by_date_range(repo, days, since, until), [repo, days, since, until], (markdown, fileDowload) )

with gr.Blocks() as edit_tab:
    with gr.Row():
        github_url=gr.Textbox(label="GitHub项目地址", placeholder="https://github.com/xxx/yyy")
        save_url=gr.Button("添加项目")
    save_url.click(lambda url: add_subscription(url) ,[github_url], [repo, github_url])

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("生成报告"):
            report_tab.render()
        with gr.TabItem("编辑订阅列表"):
            edit_tab.render()


if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))