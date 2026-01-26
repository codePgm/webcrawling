from newspaper import Article, Config
import requests.exceptions

def crawl_local(url):
    try:
        # fetch_images 제거하고 다른 옵션만 사용
        config = Config()
        config.request_timeout = 10
        
        article = Article(url, config=config)
        article.download()
        article.parse()
        title = article.title or "No Title"
        text = article.text.strip()
        if not text:
            raise Exception("로컬 크롤링 실패")
        return title, text
    except requests.exceptions.Timeout:
        raise Exception("요청 시간이 초과되었습니다.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP 오류: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"네트워크 오류: {e}")
    except Exception as e:
        raise Exception(f"로컬 크롤링 오류: {e}")