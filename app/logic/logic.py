# IMPORTING PACKAGES
from metaphor_python import Metaphor
from app.utils.openai_chat_agent import OpenAIAgent
import bs4
import requests

class TrendAnalyzer:
    # INITIALIZATION OF THE TREND ANALYZER OBJECT
    def __init__(self):
        self.openai_token = "YOUR-OPENAI-TOKEN"
        self.metaphor_token = "YOUR-METAPHOR-TOKEN"
        self.num_results = 20
        self.metaphor = Metaphor(self.metaphor_token)
        self.openai_args = {
            "token": self.openai_token,
            "temperature": 0.2,  # make the output as deterministic as possible
            "presence_penalty": -1.0,  # make the model reward talking about the same topics
        }
        self.openai_agent = OpenAIAgent(self.openai_args)

    # FUNCTION TO GENERATE LINKS USING METAPHOR'S API
    def generate_links(self, user_prompt, start_date):
        """
        @param user_prompt: User's query that has been made been consumable for Metaphor's API.
        @param start_date: The start date the user wants to search for.
        @return: A list of response ids, response links and response titles for the links generated from the user's prompt
        """
        response = self.metaphor.search(user_prompt,
                                        num_results=self.num_results,
                                        start_published_date=start_date,
                                        use_autoprompt=False
                                        )
        response_ids = []
        response_titles = []
        response_urls = []

        # EXTRACTING THE TITLES, IDs AND URLS FROM THE RESULTS
        for result in response.results:
            response_titles.append(result.title)
            response_ids.append(result.id)
            response_urls.append(result.url)

        # TAKING THE BEST 8 RESULTS DUE TO TOKEN LIMITATIONS
        response_ids = response_ids[0:8]
        response_titles = response_titles[0:8]
        response_urls = response_urls[0:8]

        # RETURNING THE IDs, TITLES AND URLS
        return response_ids, response_titles, response_urls

    # FUNCTION TO GENERATE THE LINKS FOR A SPECIFIC COMPANY USING METAPHOR'S API
    def generate_links_for_company(self, user_prompt, user_company, start_date, end_date):
        """
        @param user_company: The company the user is searching for.
        @param user_prompt: User's query that has been made been consumable for Metaphor's API.
        @param start_date: The start date the user wants to search for.
        @param end_date: The end date the user wants to search for.
        @return: A list of response ids, response links and response titles for the links generated from the user's prompt
        """
        # HITTING THE METAPHOR API TO GET THE LINKS TO SUMMARIZE
        response = self.metaphor.search(user_prompt,
                                        num_results=self.num_results,
                                        start_published_date=start_date,
                                        end_published_date=end_date,
                                        use_autoprompt=False
                                        )
        response_ids = []
        response_titles = []
        response_urls = []
        # EXTRACTING THE RESULTS THAT HAVE THE COMPANY NAME IN THE HEADLINE
        for result in response.results:
            if user_company in result.title:
                print(result.title)
                response_titles.append(result.title)
                response_ids.append(result.id)
                response_urls.append(result.url)

        # TAKING THE BEST 8 RESULTS DUE TO TOKEN LIMITATIONS
        response_ids = response_ids[0:8]
        response_titles = response_titles[0:8]
        response_urls = response_urls[0:8]

        # RETURNING THE IDs, TITLES AND URLS
        return response_ids, response_titles, response_urls

    # FUNCTION TO CLEAN HTML TAGS FROM TEXT
    def clean_text(self, response_ids):
        """
        @param response_ids: A list of response ids for the links generated from the user's prompt
        @return: A list of cleaned text extracted from the links
        """
        # HITTING THE METAPHOR API TO GET THE LINK CONTENT
        responses = self.metaphor.get_contents(response_ids)

        # CLEANING THE TEXT
        cleaned_text_list = []
        for response in responses.contents:
            soup = bs4.BeautifulSoup(response.extract, features="lxml")
            cleaned_text = soup.get_text().strip("\n")
            cleaned_text_list.append(cleaned_text)

        # RETURNING THE LIST OF CLEANED TEXT EXTRACTED
        return cleaned_text_list

    # FUNCTION TO GET COMPANY TICKER FROM COMPANY NAME
    @staticmethod
    def get_ticker(company_name):
        """
        @param company_name: The name of the company
        @return: The ticker name of the company
        """
        # HITTING THE YAHOO FINANCE API TO GET THE COMPANY TICKER NAME
        yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        params = {"q": company_name, "quotes_count": 1, "country": "United States"}
        result = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
        data = result.json()
        company_code = data['quotes'][0]['symbol']

        # RETURNING THE COMPANY TICKER
        return company_code

    # FUNCTION TO GET THE ARTICLE CONTENT USING THE DOCUMENT ID
    def read_article(self, link_id):
        """
        @param link_id: The document id provided by the user for the link he wants to read!
        @return: The content of the document provided by the Metaphor API
        """
        # HITTING THE METAPHOR API TO GET THE LINK CONTENT
        response = self.metaphor.get_contents(link_id)

        # RETURNING THE API RESPONSE
        return response

    # FUNCTION TO GET SEMANTICALLY SIMILAR LINKS
    def get_similar_links(self, link_url):
        """
        @param link_url: The url provided by the user for the article he wants to find similar URL for!
        @return: The semantically similar urls provided by the Metaphor API
        """
        # HITTING THE METAPHOR API
        response = self.metaphor.find_similar(url=link_url)

        # RETURNING THE API RESPONSES
        return response


# MAIN FUNCTION
if __name__ == "__main__":
    pass
