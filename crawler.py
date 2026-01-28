from newspaper import Article, Config
import requests
import fitz
import io

def crawl_local(url):
    try:
        config = Config()
        config.request_timeout = 10

        article = Article(url, config=config)
        article.download()
        article.parse()

        title = article.title or "No Title"
        text = article.text.strip()

        if not text:
            raise Exception("본문 추출 실패")

        return title, text

    except requests.exceptions.Timeout:
        raise Exception("요청 시간이 초과되었습니다.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"네트워크 오류: {e}")
    except Exception as e:
        raise Exception(f"로컬 크롤링 오류: {e}")
    
def crawl_pdf(url):
    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()

        content_type = res.headers.get("Content-Type", "").lower()

        if (
            "application/pdf" not in content_type
            and ".pdf" not in url.lower()
        ):
            raise Exception(f"PDF 아님 (Content-Type: {content_type})")

        pdf_data = io.BytesIO(res.content)
        doc = fitz.open(stream=pdf_data, filetype="pdf")

        text = ""
        for page in doc:
            page_text = page.get_text("text")
            if not page_text.strip():
                page_text = page.get_text("blocks")
            text += page_text

        if not text.strip():
            raise Exception("PDF는 열렸으나 텍스트가 포함되어 있지 않습니다.")

        title = doc.metadata.get("title") or "PDF_Document"
        return title, text.strip()

    except requests.exceptions.Timeout:
        raise Exception("PDF 요청 시간 초과")
    except Exception as e:
        raise Exception(f"PDF 크롤링 오류: {e}")