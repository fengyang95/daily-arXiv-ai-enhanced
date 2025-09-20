import scrapy
import os
from ..fetchers.wechat_fetcher import WeChatFetcher


class WechatSpider(scrapy.Spider):
    name = "wechat"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Unified Search API configuration
        self.api_base_url = os.environ.get("WECHAT_API_BASE_URL", "http://47.117.133.51:30015")
        self.api_token = os.environ.get("WECHAT_API_TOKEN", "")
        self.keywords = os.environ.get("WECHAT_KEYWORDS", "AI,人工智能,机器学习,深度学习").split(",")
        self.source = 'WEIXIN'  # WeChat source as specified in API
        
    def start_requests(self):
        """Generate requests for WeChat data using Unified Search API"""
        if not self.api_token:
            self.logger.warning("No API token provided for WeChat search")
            return
        
        # Create fetcher instance
        config = {
            'api_token': self.api_token,
            'api_base_url': self.api_base_url,
            'keywords': self.keywords,
            'source': self.source
        }
        fetcher = WeChatFetcher(config)
        
        # Fetch articles directly using the fetcher
        articles = fetcher.fetch_articles()
        
        # Yield each article
        for article in articles:
            yield article