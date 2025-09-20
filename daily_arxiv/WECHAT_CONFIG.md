# WeChat Search Configuration

This document describes the configuration for the WeChat search functionality using the WeChat Search V1 API.

## Overview

The system now uses the **WeChat Search V1 API** to fetch WeChat articles. This provides a more reliable and standardized way to search for WeChat content compared to the previous RSS-based approach.

## Environment Variables

### Required Variables

- `WECHAT_API_TOKEN`: Your API token for the WeChat Search API (stored as GitHub Secret)

### Optional Variables

- `WECHAT_API_BASE_URL`: Base URL for the API (default: `http://47.117.133.51:30015`)
- `WECHAT_KEYWORDS`: Comma-separated list of keywords to search (default: `AI,人工智能,机器学习,深度学习`)

## API Configuration

The system uses the WeChat Search V1 API with the following parameters:

- **Endpoint**: `/api/weixin/search/v1`
- **Method**: `GET`
- **Search Type**: `_2` (articles only)
- **Sort Type**: `_2` (latest first)
- **Keywords**: Configurable list of search terms
- **Pagination**: Uses offset-based pagination (20 items per page)
- **Deduplication**: Automatically removes duplicate articles based on docID and URL

## Configuration Steps

### 1. Add WeChat API Token (Required)

Go to your repository: `Settings -> Secrets and variables -> Actions -> Secrets`

Add:
- `WECHAT_API_TOKEN`: Your API token for the Unified Search API

### 2. Add WeChat Configuration Variables (Optional)

Go to: `Settings -> Secrets and variables -> Actions -> Variables`

Add the following variables:

- `WECHAT_KEYWORDS`: Comma-separated list of keywords to search
  - Example: `"AI,artificial intelligence,machine learning,计算机视觉,自然语言处理"`
  - Default: `"AI,人工智能,机器学习,深度学习"`

- `WECHAT_API_BASE_URL`: API server address (only if different from default)
  - Example: `"http://47.117.133.51:30015"`
  - Default: `"http://47.117.133.51:30015"`

## How It Works

1. **API Authentication**: Uses the provided token for API access
2. **Keyword Search**: Searches for each keyword separately
3. **Date Filtering**: Automatically searches the last 7 days
4. **Pagination**: Automatically handles multi-page results using `nextCursor`
5. **Format Conversion**: Converts WeChat articles to arXiv format
6. **Content Categorization**: Automatically categorizes based on content

## Data Format

WeChat articles are automatically converted to match arXiv format:

```json
{
  "id": "wechat.2509.a1b2c3d4",
  "categories": ["wechat.ai", "wechat.ml"],
  "pdf": "https://original-article-url.com",
  "abs": "https://original-article-url.com", 
  "authors": ["Author Name"],
  "title": "Article Title",
  "comment": "Source: WeChat, Published: 2025-09-19",
  "summary": "Article summary or content..."
}
```

## Content Categorization

The system automatically categorizes WeChat articles based on keywords:

- `wechat.ai`: AI/ML related content (AI, artificial intelligence, 人工智能, 机器学习, 深度学习)
- `wechat.cv`: Computer vision topics (computer vision, image, video, cv, recognition, 计算机视觉, 图像)
- `wechat.cl`: Computational linguistics/NLP (nlp, language, text, translation, bert, gpt, 自然语言, 文本)
- `wechat.article`: General category

## API Response Format

The API returns articles in the following format:

```json
{
  "code": 0,
  "message": "",
  "data": {
    "boxID": "0x2-0-1705916886373149745",
    "boxPos": 1,
    "count": 21,
    "items": [
      {
        "date": 1758384000,
        "desc": "为实现DeepSeek-R1-Zero的大规模强化学习，我们采用了一个高效的强化学习流程...",
        "docID": "1705916886373149745",
        "docType": 0,
        "doc_url": "http://mp.weixin.qq.com/s?__biz=MzkzMTE5MzEyMQ==&mid=2247529164&idx=8&sn=0098613abb09af761146a39d79af8793&chksm=c3893233cf8db25161b99df46eda3f491227447d68854b61f0f0f012c1190cd9258954a7c5c8#rd",
        "itemShowType": 0,
        "mpScene": 7,
        "reportId": "1705916886373149745:mp:349698",
        "source": {
          "dateTime": "1小时前",
          "title": "精确打击洞见"
        },
        "src_type": 49,
        "thumbUrl": "https://mmbiz.qpic.cn/sz_mmbiz_jpg/qtKfIJIib6n7fniao4YtjWpAxdvF9ictx3LqaNicibNviarYaIwmiaXfFqd6IOicWpBt2gkop2AzfJgzSApEyFASTIjbBA/0?wx_fmt=jpeg",
        "timestamp": 1758384000,
        "title": "【完整中文版】梁文锋 Nature封面论文 - DeepSeek-R1：通过强化学习激励大语言模型的推理能力"
      }
    ],
    "real_type": 2,
    "resultType": 0,
    "subType": 0,
    "totalCount": 185,
    "type": 2
  },
  "message": null,
  "recordTime": "2025-09-21T01:13:26.876504942"
}
```

### Key Fields:
- **`items`**: Array of articles (changed from `list`)
- **`date`**: Unix timestamp in seconds (changed from `createTime`)
- **`desc`**: Article description/content (changed from `content`)
- **`doc_url`**: Article URL (changed from `url`)
- **`docID`**: Unique identifier for each article (used for deduplication)
- **`source`**: Contains author name in `title` field
- **`totalCount`**: Total number of results

## Deduplication Features

The system implements intelligent deduplication to avoid duplicate articles:

1. **Primary Deduplication**: Based on `docID` field from WeChat API
2. **Secondary Deduplication**: Based on article URL hash as fallback
3. **Cross-keyword Deduplication**: Prevents duplicates across different search keywords
4. **Real-time Processing**: Deduplication happens during API response parsing

This ensures that:
- The same article won't appear multiple times from different keywords
- Articles with identical content but different URLs are handled
- The final dataset contains only unique articles

## Error Handling

The system handles various error scenarios:
- Missing API token
- API request failures
- Invalid JSON responses
- Missing required fields in responses
- API error codes (non-zero code values)

All errors are logged and the spider continues processing other keywords.

## Example Configuration

**Repository Secrets:**
```
WECHAT_API_TOKEN = "your-api-token-here"
```

**Repository Variables:**
```
WECHAT_KEYWORDS = "AI,artificial intelligence,machine learning,计算机视觉,自然语言处理"
WECHAT_API_BASE_URL = "http://47.117.133.51:30015"
```

## Migration from RSS-based System

If you were previously using the RSS-based system:

1. **Remove old variables**: `WECHAT_SOURCES`, `WECHAT_API_KEY`
2. **Add new token**: `WECHAT_API_TOKEN` (as Secret)
3. **Update keywords**: Use `WECHAT_KEYWORDS` instead of hardcoded sources
4. **Test the integration**: Run the workflow manually to verify

## Security Notes

- API tokens must be stored as GitHub Secrets, not Variables
- The API server address is configurable but should be trusted
- All external content is validated and sanitized
- Consider rate limiting for high-frequency searches

## Troubleshooting

### No Articles Found

1. Verify your API token is valid
2. Check if the API server is accessible
3. Try different keywords
4. Check GitHub Actions logs for API errors

### API Errors

1. Ensure the API token has proper permissions
2. Verify the API server URL is correct
3. Check if the server is running (status: the default server may be down)
4. Review API response codes and messages in logs