# AI News Fact-Checker (Llama 3 Powered)

This project is an automated news analysis tool that leverages **Large Language Models (LLM)** to identify potential misinformation. It uses **LangChain** to orchestrate the workflow, **Ollama** to run Llama 3 locally, and various web scraping libraries to extract content from news URLs.

## 🌟 Key Features

* **Dual Extraction**: Combined logic using `BeautifulSoup` and `newspaper3k` for robust content scraping.
* **Local LLM Integration**: Uses `ChatOllama` to run **Llama 3**, ensuring data privacy and zero API costs.
* **Logical Reasoning**: The AI is prompted to follow a specific fact-checking reasoning process before reaching a verdict.
* **Flexible Input**: Supports both direct URL crawling and raw text input.

## 🛠️ Prerequisites

1.  **Install Ollama**: Download and install from [ollama.com](https://ollama.com/).
2.  **Download Llama 3**: Run the following command in your terminal:
    ```bash
    ollama run llama3
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

You can run the script via the command line using either a URL or raw text.

### Option A: Analyze via URL
```bash
python main.py --url "[https://www.example-news.com/article-123](https://www.example-news.com/article-123)"
```
### Option B: Analyze via Raw Tex
```bash
python main.py --text "Paste the news content here to verify its authenticity."
```
