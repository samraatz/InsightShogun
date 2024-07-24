
# Insight Shogun

![Insight Shogun Banner](https://github.com/samraatz/InsightShogun/main/banner.png)

### Unleashing the Power of NLP and Knowledge Graphs

**Insight Shogun** is a comprehensive tool that combines the prowess of web scraping, natural language processing (NLP), and knowledge graph creation. Inspired by the strategic mastery of a Shogun, this project aims to provide deep insights from news articles, establishing meaningful connections between entities and topics.

### Features

- **Web Scraping**: Efficiently extract article titles, publication dates, content, and URLs from various news websites using `requests` and `BeautifulSoup`.
  ![Web Scraping](path_to_your_image/web_scraping.png)
- **Named Entity Recognition (NER)**: Identify key entities such as people, organizations, and locations within the content using `spaCy`.
  ![Named Entity Recognition](path_to_your_image/ner.png)
- **Keywords Extraction**: Utilize the OpenAI API to extract significant keywords from the articles, adding another layer of analysis.
  ![Keywords Extraction](path_to_your_image/keywords_extraction.png)
- **Knowledge Graph Creation**: Build and visualize a knowledge graph using `Neo4j`, representing relationships between entities and articles.
  ![Knowledge Graph Creation](path_to_your_image/knowledge_graph.png)
- **LLM Integration**: Leverage the OpenAI API to uncover additional relationships between entities, identifying deeper insights and connections within the content.
  ![LLM Integration](path_to_your_image/llm_integration.png)

### How It Works

1. **Scrape Articles**: Extract detailed information from news websites.
   ![Scrape Articles](path_to_your_image/scrape_articles.png)
2. **Process Content**: Use NLP techniques to identify entities and keywords within the articles.
   ![Process Content](path_to_your_image/process_content.png)
3. **Build Knowledge Graph**: Create nodes for entities and articles, and establish relationships based on their co-occurrence and shared keywords.
   ![Build Knowledge Graph](path_to_your_image/build_knowledge_graph.png)
4. **Enhance with LLM**: Utilize the power of language models to reveal hidden relationships and deeper insights.
   ![Enhance with LLM](path_to_your_image/enhance_with_llm.png)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/insight-shogun.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

### Usage

1. Update the configuration with your Neo4j and OpenAI API credentials.
2. Run the main script:
   ```bash
   python main.py
   ```

### Requirements

- Python 3.6+
- BeautifulSoup4
- Requests
- spaCy
- Neo4j
- OpenAI API

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

### License

This project is licensed under the MIT License.
```

