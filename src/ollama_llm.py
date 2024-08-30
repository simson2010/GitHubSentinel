import json
from openai import OpenAI
from logger import LOG  # 导入日志模块

class Ollama_LLM:
    def __init__(self, model, url):
        # openai.api_key = api_key
        self.model = model
        self.url_base = url
        self.client = OpenAI()
        self.client.api_key = "temp_key"
        self.client.base_url = self.url_base
        self.messages = []
        with open("prompts/report_prompt.txt", "r", encoding='utf-8') as file:
            self.system_prompt = file.read()
         # 配置日志文件，当文件大小达到1MB时自动轮转，日志级别为DEBUG
        LOG.add("logs/llm_ollama_logs.log", rotation="1 MB", level="DEBUG")
  
    def generate_daily_report(self, markdown_content, dry_run=False):
        # 使用从TXT文件加载的提示信息
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            # 如果启用了dry_run模式，将不会调用模型，而是将提示信息保存到文件中
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                # 格式化JSON字符串的保存
                json.dump(messages, f, indent=4, ensure_ascii=False)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"

        # 日志记录开始生成报告
        LOG.info("Starting report generation using OLLAMA hosting model.")

        
        try:
            # 调用OpenAI GPT模型生成报告
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            LOG.debug("OLLAMA hosting model response: {}", response)
            # 返回模型生成的内容
            return response.choices[0].message.content
        except Exception as e:
            # 如果在请求过程中出现异常，记录错误并抛出
            LOG.error("An error occurred while generating the report: {}", e)
            raise

if __name__ == "__main__":
    # 创建 ChatAPI 实例（这里的 URL 是本地代理的地址）
    model='llama3.1'
    chat_api = Ollama_LLM(model, "http://localhost:11434/v1/")
    
    try:
        # 发送请求并获取响应
        response_data = chat_api.generate_daily_report("# 开源模型测试")
        print("响应数据:")
        print( response_data)
    except Exception as e:
        print(f"发生错误: {str(e)}")
