from ollama_llm import Ollama_LLM
from openai_llm import OpenAI_LLM
from config import Config

class LLM:

    def __init__(self):
            #read config.json
        self.config = Config()
        if self.config.local_model_enabled == False:
            self.llm = OpenAI_LLM()
        else:
            self.llm = Ollama_LLM(model=self.config.local_model_name, url=self.config.local_model_base_url)
    
    def generate_daily_report(self, markdown_content):
        return self.llm.generate_daily_report(markdown_content)


if __name__ == "__main__":
    llm = LLM()
    print(llm.generate_daily_report("test"))

# run result for ollama hosting model
# agent-study) D:\ai-study\GitHubSentinel>python src\gradio_server.py
# Running on local URL:  http://0.0.0.0:7860

# Could not create share link. Please check your internet connection or our status page: https://status.gradio.app.
# ollama/ollama 2 1724956049.039206 1725042449.039206
# 2024-08-31T02:27:31.932872+0800 INFO Exported time-range progress to daily_progress\ollama_ollama\2024-08-30T02_27_29.039206_to_2024-08-31T02_27_29.039206.md
# 2024-08-31T02:27:31.932872+0800 INFO Starting report generation using OLLAMA hosting model.
# 2024-08-31T02:27:37.036882+0800 DEBUG OLLAMA hosting model response: ChatCompletion(id='chatcmpl-510', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='# ollama/ollama 项目进展\n\n\n## 时间周期：2024-08-30至2024-08-31\n\n\n## 新增功能\n本次更新中，没有新增任何函数或模块的声明。\n\n\n## 主要改进\n本次发布没有特定的主要改进，因为所有改进都是修复 bug 或是增加一些小细节的 调整.\n\n\n## 修复问题\n此版本修复以下几个 bug:\n\n- 删除了不必要的构建产物（build artifacts），以此来减少包大小并提高部署效率。\n- 修复了在docker环境中通过代理下载模型文件时出现的问题(#6550)。\n- 针对 ollama 的模板进行了更新，将 message 消息升级为使用最初始的配置（#6534）。\n- 确 保OLLAMA_HOST路径能够正确传递到客户端（Client）（#6482）。\n- 修复docker环境下 api-call请求与python-client-library无法成功接收响应的问题(#6398)。\n- 重磅修复ollamadocker运行时出现的错误终止问题(#845）。', refusal=None, role='assistant', function_call=None, tool_calls=None))], created=1725042457, model='llama3.1', object='chat.completion', service_tier=None, system_fingerprint='fp_ollama', usage=CompletionUsage(completion_tokens=245, prompt_tokens=389, total_tokens=634))
# 2024-08-31T02:27:37.037992+0800 INFO Generated report saved to daily_progress\ollama_ollama\2024-08-30T02_27_29.039206_to_2024-08-31T02_27_29.039206_report.md
