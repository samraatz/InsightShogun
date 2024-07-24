
#  Insight Shogun

![Insight Shogun Banner](https://github.com/samraatz/InsightShogun/blob/main/banner.png)

### Unleashing the Power of NLP and Knowledge Graphs

**Insight Shogun** is a comprehensive tool that combines the prowess of web scraping, natural language processing (NLP), and knowledge graph creation. Inspired by the strategic mastery of a Shogun, this project aims to provide deep insights from news articles, establishing meaningful connections between entities and topics.

### Features

- **Web Scraping**: Efficiently extract article titles, publication dates, content, and URLs from various news websites using `requests` and `BeautifulSoup`.
  ![Web Scraping](https://github.com/samraatz/InsightShogun/blob/main/ws.png)
- **Named Entity Recognition (NER)**: Identify key entities such as people, organizations, and locations within the content using `spaCy`.
  ![Named Entity Recognition](https://github.com/samraatz/InsightShogun/blob/main/ner.png)
- **Keywords Extraction**: Utilize the OpenAI API to extract significant keywords from the articles, adding another layer of analysis.
  ![Keywords Extraction](https://github.com/samraatz/InsightShogun/blob/main/key.png)
- **Knowledge Graph Creation**: Build and visualize a knowledge graph using `Neo4j`, representing relationships between entities and articles.
  ![Knowledge Graph Creation](https://github.com/samraatz/InsightShogun/blob/main/kg.png)
- **LLM Integration**: Leverage the OpenAI API to uncover additional relationships between entities, identifying deeper insights and connections within the content.
  ![LLM Integration](https://github.com/samraatz/InsightShogun/blob/main/api.png)

### How It Works

1. **Scrape Articles**: Extract detailed information from news websites.
   ![Scrape Articles](https://github.com/samraatz/InsightShogun/blob/main/scrape.png)
2. **Process Content**: Use NLP techniques to identify entities and keywords within the articles.
   ![Process Content](https://github.com/samraatz/InsightShogun/blob/main/spacy.png)
3. **Build Knowledge Graph**: Create nodes for entities and articles, and establish relationships based on their co-occurrence and shared keywords.
   ![Build Knowledge Graph](https://github.com/samraatz/InsightShogun/blob/main/kg1.png)
4. **Enhance with LLM**: Utilize the power of language models to reveal hidden relationships and deeper insights.
   ![Enhance with LLM](https://github.com/samraatz/InsightShogun/blob/main/er.png)

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

