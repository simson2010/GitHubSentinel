import json
import os

class Config:
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        # 从环境变量获取GitHub Token
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            # 如果环境变量中没有GitHub Token，则从配置文件中读取
            if not self.github_token:
                self.github_token = config.get('github_token')
                
            self.notification_settings = config.get('notification_settings')
            self.subscriptions_file = config.get('subscriptions_file')
            self.update_interval = config.get('update_interval', 24 * 60 * 60)  # 默认24小时
            self.use_local_model = config.get('use_local_model', {})
            self.local_model_enabled = self.use_local_model.get('enabled', False)
            self.local_model_name = self.use_local_model.get('model', "no mode")
            self.local_model_base_url = self.use_local_model.get('base_url', "no url")


if __name__ == '__main__':
    config = Config()
    print(config.github_token)
    print(config.notification_settings)
    print(config.subscriptions_file)
    print(config.update_interval)
    print(config.use_local_model)
    print(config.local_model_enabled)
    print(config.local_model_name)
    print(config.local_model_base_url)
