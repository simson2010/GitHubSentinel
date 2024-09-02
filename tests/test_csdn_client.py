import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加 src 目录到模块搜索路径，以便可以导入 src 目录中的模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from csdn_client import CSDNClient 

class TestCSDNClient(unittest.TestCase):

    def setUp(self):
        self.client = CSDNClient()

    @patch('csdn_client.webdriver.Chrome')  # Mocking the Chrome WebDriver
    def test_fetch_article_list_success(self, mock_chrome):
        # Arrange
        client = self.client 
        mock_driver = MagicMock()  # Create a mock browser driver
        mock_chrome.return_value = mock_driver  # Return the mock driver when creating a Chrome instance
        
        # Prepare HTML response that would simulate a real CSDN page
        mock_driver.page_source = '''
        <html>
            <body>
                <a class="blog" href="https://example.com/article1">
                    <span class="blog-text">Article 1</span>
                </a>
                <a class="blog" href="https://example.com/article2">
                    <span class="blog-text">Article 2</span>
                </a>
            </body>
        </html>
        '''
        
        # Act
        articles = client.fetch_article_list()

        # Assert
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]['title'], 'Article 1')
        self.assertEqual(articles[0]['link'], 'https://example.com/article1')
        self.assertEqual(articles[1]['title'], 'Article 2')
        self.assertEqual(articles[1]['link'], 'https://example.com/article2')

    @patch('csdn_client.webdriver.Chrome')
    def test_fetch_article_list_failure(self, mock_chrome):
        # Arrange
        client = self.client 
        mock_chrome.side_effect = Exception("WebDriver failed")  # Simulate a WebDriver failure

        # Act
        articles = client.fetch_article_list()

        # Assert
        self.assertEqual(articles, [])
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open)  # Mock open function
    @patch('os.makedirs')  # Mock os.makedirs to avoid filesystem operations
    def test_export_articles(self, mock_makedirs, mock_open):
        # Arrange
        client = CSDNClient()
        client.fetch_article_list = MagicMock(return_value=[
            {'title': 'Test Article 1', 'link': 'https://example.com/test1'},
            {'title': 'Test Article 2', 'link': 'https://example.com/test2'}
        ])
        
        # Act
        file_path = client.export_articles(date='2024-09-03', hour='10')

        # Assert
        mock_makedirs.assert_called_once_with('csdn_articles\\2024-09-03', exist_ok=True)
        mock_open.assert_called_once_with('csdn_articles\\2024-09-03\\10.md', 'w', encoding='utf-8')
        self.assertTrue(file_path.endswith('\\10.md'))  # Ensure it returns a path ending with '/10.md'


if __name__ == '__main__':
    unittest.main()
