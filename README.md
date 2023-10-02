# MetaphorStockTrendAnalyzer
A FastAPI-based API combining Metaphor's API and OpenAI's GPT-3.5 to extract and analyze headlines for predicting stock trends and recommending stocks!
### Overview:
This comprehensive API integrates Metaphor's powerful search capabilities with OpenAI's gpt-3.5-turbo language model to offer a suite of invaluable features for stock market enthusiasts and investors.  
It leverages Metaphor's search and content retrieval endpoints to extract and process relevant financial news articles about user-specified companies. These articles, along with expertly engineered prompts, are then presented to OpenAI's gpt-3.5-turbo, which generates insightful stock trend analyses and stock recommendations. 
Users can access these analyses, along with article summaries and URLs, to make informed investment decisions.  
With its array of endpoints and powerful AI integration, this API empowers users with valuable insights for their investment strategies!
### Key Features:

#### Block Diagram of the Project:
![Alt text](https://github.com/osabnis/MetaphorStockTrendAnalyzer/blob/main/diagrams/block_diagram.png?raw=true "Block Diagram")

#### User Prompt Modification: 
The API modifies the user's query into a specific prompt, which helps extract the best results from Metaphor's API!

#### Metaphor's Search API: 
The API utilizes Metaphor's search endpoint to find the most relevant financial news about the company the user is interested in. The API returns the most relevant news articles about the company!

#### Analyzing the links: 
The API utilized Metaphor's content retrieval endpoint to extract the content from the retrieved links. This content is then processed to make it suitable for further analysis!

#### Prompt Engineering for OpenAI: 
The API uses an engineered prompt along with the processed news articles for analysis by GPT-3. The prompt was engineered to extract the best possible analysis and recommendations from GPT-3! 

#### OpenAI's gpt-3.5-turbo:
The API uses OpenAI's gpt-3.5-turbo as the LLM to generate stock trend analysis and recommendations!  

#### Processing GPT-3 responses:
The API then processes the outputs from GPT-3, to extract the most relevant analysis and recommendations for the user!

#### Analyses and Recommendations:
The API returns the analysis and recommendations to the user - from which they can get a holistic understanding of the current news and public sentiment about the company and their stock!

### Main Endpoints:
This is how the Swagger page of the API looks like:  
![Alt text](https://github.com/osabnis/MetaphorStockTrendAnalyzer/blob/main/diagrams/fastapi_swagger.png?raw=true "Swagger Diagram")

These are the main endpoints available:
#### 1. /trend_analysis/analysis:
This endpoint is used to provide the user with a stock trend analysis about a company provided by the user. They can use this analysis to make an informed decision about whether to buy, sell or hold this stock in their portfolio.

This endpoint takes three inputs:
* company_name: This input takes the name of the company that the user wants to know more about.
* start_date: This input takes the date from which they want the articles to be published.
* end_date: This input takes the date up to which they want the articles to be published.

This endpoint returns:
* A string output which has the following:
  * The URLs, the titles, and the unique IDs of the articles used by the API to come to its conclusion.
  * The summary of news about the company.
  * The approximate trends about the stock prices based on the various possible scenarios.

#### 2. /trend_analysis/read_article:
This endpoint is used to provide the user with the contents of the article that they are interested in reading.

This endpoint takes a single input:
* link_id: This input is the unique ID returned in the previous input which Metaphor uses to uniquely identify a document.

This endpoint returns:
* A string output which has the following:
  * The URL of the article.
  * The title of the article.
  * The extracted and processed content in the link.

#### 3. /trend_analysis/similar_links:
This endpoint is used to provide articles similar to the ones they provide the link for.

This endpoint takes a single input:
* link: This input is the URL of the article which they want to find similar articles for.

This endpoint returns:
* A JSON output which has the following:
  * The title of the article.
  * The URL of the article.
  * The unique ID of the article.
  * The similarity score for the articles.
  * The date the article was published.
  * The author of the article.
  * The extract if available.

#### 4. /trend_analysis/stock_comparison:
This endpoint is used to provide the user with a comparison between two different companies. The user is shown the recent news about both the companies and if a recommendation can be made, a recommendation on which is the better stock to invest in!

This endpoint takes three inputs:
* company_name_1: This input takes the name of the company that the user wants to know more about.
* company_name_2: This input takes the name of the second company that the user wants to know more about.
* start_date: This input takes the date from which they want the articles to be published.
* end_date: This input takes the date up to which they want the articles to be published.

This endpoint returns:
* A string output which has the following:
  * The summaries of the news about both companies.
  * The expected trends of the stock prices based on these summaries.
  * A recommendation on which stock to buy.


#### 5. /trend_analysis/recommendations:
This endpoint is used to provide the user, recommendations on which stock to invest in based on the financial news articles and public sentiment!

This endpoint takes a single input:
* start_date: This input takes the date from which they want the articles to be published.

This endpoint returns:
* A string output which has the following:
  * The summaries of the articles used to come up with the stock recommendations.
  * The top 10 stocks it recommends.

#### Conclusion:
In the fast-paced world of stock markets, staying informed and making well-informed investment decisions is critical. Our API, powered by the synergy of Metaphor's financial news search capabilities and OpenAI's gpt-3.5-turbo, empowers users with a comprehensive set of tools to navigate the complexities of the financial landscape!  

### How to run this?
Make the following changes to be able to run this code for yourself!
- Create an environment with the requirements file provided.
- Add your Metaphor and OpenAI tokens in the app/logic/logic.py file.
- Run the main.py file using this environment.
- You should be good to go - with the API being visible at the http://localhost:8000/docs!
