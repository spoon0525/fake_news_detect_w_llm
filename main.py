from langchain_ollama import ChatOllama
from newspaper import Article
from langchain.prompts import ChatPromptTemplate
import requests
from bs4 import BeautifulSoup
import argparse

llm = ChatOllama(model="llama3",temperature=0)

def fetch_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title, article.text[:2000]

def classify_article_with_llm(content):
  prompt_template = ChatPromptTemplate.from_template(f"""
You are a fact-checking assistant. Please analyze the following news article and determine whether it is Real or Fake.

Content:
{content}

Follow this reasoning process:
1. Identify any unusual or exaggerated claims.
2. Evaluate based on known facts.
3. Conclude with: Conclusion: Real or Fake. Confidence level: 0%~100%.
""")
  prompt = prompt_template.format_messages(content=content)
  response = llm(prompt)
  return response.content

def extract_news_content(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"無法取得網頁內容：{e}"

    soup = BeautifulSoup(response.text, 'html.parser')

    possible_selectors = [
        {'tag': 'div', 'class_': 'story'},
        {'tag': 'div', 'class_': 'article-content'},
        {'tag': 'div', 'class_': 'articulum'},
        {'tag': 'div', 'id': 'main-content'},
        {'tag': 'div', 'class_': 'post-content'},
        {'tag': 'article'},
    ]

    for selector in possible_selectors:
        if 'id' in selector:
            content_div = soup.find(selector['tag'], id=selector['id'])
        else:
            content_div = soup.find(selector['tag'], class_=selector['class_']) if 'class_' in selector else soup.find(selector['tag'])

        if content_div:
            paragraphs = content_div.find_all(['p', 'div'])
            text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if len(text) > 100:
                return text

    return "未能擷取到文章內容，請確認網址或手動指定選擇器。"

parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str, help='URL of news to be tested')
parser.add_argument('--text', type=str, help='Raw text of news to be tested')
args = parser.parse_args()

if args.url:
    input_text = extract_news_content(args.url)
    if not input_text:
        print("can't get text from this url")
        exit()
elif args.text:
    input_text = args.text
else:
    print("please provide url or text")
    exit()

result = classify_article_with_llm(input_text)

print("\nLLM Output:\n")
print(result)
