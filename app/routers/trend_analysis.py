# IMPORT PACKAGES
from fastapi import APIRouter
from app.logic.logic import TrendAnalyzer
from fastapi.responses import Response
import re

# DEFINE THE FASTAPI ROUTER
router = APIRouter(tags=["Trend Analysis"])

# INITIALIZING THE TREND ANALYZER CLASS
trend_analyzer = TrendAnalyzer()


# THE GET ENDPOINT FOR RETURNING THE SUMMARY AND ANALYSIS BY GPT-3.5
@router.get("/trend_analysis/analysis", description="Analysis of the headlines for your company of choice!")
def trend_analysis(company_name: str, start_date: str, end_date: str):

    # USER QUERY
    USER_QUESTION = "Here's the latest financial headlines about {}:".format(
        company_name)  # To reduce my OpenAI credit usage, I directly used a query that is useful for Metaphor!

    # GET LINKS FROM METAPHOR
    link_ids, link_titles, link_urls = trend_analyzer.generate_links_for_company(user_prompt=USER_QUESTION,
                                                                                 user_company=company_name,
                                                                                 start_date=start_date,
                                                                                 end_date=end_date)

    # CLEAN AND EXTRACT THE TEXT FROM THE LINKS
    headlines_list = trend_analyzer.clean_text(response_ids=link_ids)
    headlines = "\n".join(headlines_list)

    # SETTING UP OPENAI AGENT FOR GENERATING THE TRENDS BASED ON THE HEADLINES
    prompt = f"There is news about the {company_name} Company, whose stock code is '{trend_analyzer.get_ticker(company_name)}'. The news are separated in '\\n'. The news are {headlines}. \
    Please give a brief summary of these news and determine the potential impact of recent headlines on the stock price of {company_name}.\
    Please give trends results based on different possible assumptions."

    # GETTING THE RESULTS
    results = trend_analyzer.openai_agent.get_response(prompt)
    summary = trend_analyzer.openai_agent.show_conversation()

    # FORMATTING THE RESPONSES
    url_titles_list = []
    for i in range(len(link_urls)):
        url_titles_list.append(f"Title: {link_titles[i]}\nURL: {link_urls[i]}\nLink ID: {link_ids[i]}")
    url_titles_list = "\n".join(url_titles_list)

    # RETURNING THE FINAL RESPONSE
    return Response(content=f"URLs Analyzed:\n{url_titles_list}\n\n{summary['content']}", media_type="String")


# THE GET ENDPOINT FOR RETURNING THE CONTENT OF THE ARTICLE USING ITS LINK ID
@router.get("/trend_analysis/read_article", description="Read the financial article you are interested in!")
def read_article(link_id: str):

    # GETTING THE CONTENT FROM METAPHOR'S ENDPOINT
    content = trend_analyzer.read_article(link_id=link_id)

    # REGEX TO CLEAN
    regex_clean = re.compile('<.*?>')
    print(content.contents)
    link_title = content.contents[0].title
    link_url = content.contents[0].url
    link_text = content.contents[0].extract
    cleaned_text = re.sub(regex_clean, '', link_text)
    cleaned_text = cleaned_text.strip("\n").strip('\t')

    # RETURNING THE FINAL RESPONSE
    return Response(content=f"Link URL:\n{link_url}\n\nLink Title:\n{link_title}\n\nLink Content:\n{cleaned_text}")

# THE GET ENDPOINT FOR RETURNING SIMILAR LINKS TO THE URL PROVIDED
@router.get("/trend_analysis/similar_links", description="Find similar articles to the ones you are interested in!")
def find_similar_links(link: str):

    # GETTING THE SIMILAR LINKS FROM METAPHOR'S ENDPOINT
    content = trend_analyzer.get_similar_links(link_url=link)

    # RETURN THE RESPONSE
    return content

# THE GET ENDPOINT FOR PROVIDING A COMPARISON BETWEEN TWO COMPANIES BASED ON THE HEADLINES
@router.get("/trend_analysis/stock_comparison", description="Provide a comparison between two companies and which would be a better investment based on current public sentiment!")
def compare_companies(company_name_1: str, company_name_2: str, start_date: str, end_date: str):
    # USER QUERY
    USER_QUESTION1 = "Here's the latest financial headlines about {}:".format(company_name_1)  # To reduce my OpenAI credit usage, I directly used a query that is useful for Metaphor!

    # GET LINKS FROM METAPHOR
    link_ids_1, link_titles_1, link_urls_1 = trend_analyzer.generate_links_for_company(user_prompt=USER_QUESTION1,
                                                                                       user_company=company_name_1,
                                                                                       start_date=start_date,
                                                                                       end_date=end_date)

    # CLEAN AND EXTRACT THE TEXT FROM THE LINKS
    headlines_list_1 = trend_analyzer.clean_text(response_ids=link_ids_1)
    headlines_1 = "\n".join(headlines_list_1)

    # USER QUERY
    USER_QUESTION2 = "Here's the latest financial headlines about {}:".format(company_name_2)  # To reduce my OpenAI credit usage, I directly used a query that is useful for Metaphor!

    # GET LINKS FROM METAPHOR
    link_ids_2, link_titles_2, link_urls_2 = trend_analyzer.generate_links_for_company(user_prompt=USER_QUESTION2,
                                                                                       user_company=company_name_2,
                                                                                       start_date=start_date,
                                                                                       end_date=end_date)

    # CLEAN AND EXTRACT THE TEXT FROM THE LINKS
    headlines_list_2 = trend_analyzer.clean_text(response_ids=link_ids_2)
    headlines_2 = "\n".join(headlines_list_2)

    # SETTING UP OPENAI AGENT FOR GENERATING THE TRENDS BASED ON THE HEADLINES
    prompt = f"There is news about the {company_name_1} Company'. The news are separated by '\\n'. The news are {headlines_1}. \
               There is news about the {company_name_2} Company'. The news are separated by '\\n'. The news are {headlines_2}. \
               Please give a brief summary of the news for both companies. \
               Determine the potential impact of recent headlines on the stock price for both {company_name_1} and {company_name_2}.\
               Predict which is the stock that could be the better investment based on the recent headlines."

    # GETTING THE RESULTS
    results = trend_analyzer.openai_agent.get_response(prompt)
    summary = trend_analyzer.openai_agent.show_conversation()

    # RETURN THE RESPONSE
    return Response(content=f"Response:\n\n{summary['content']}", media_type="String")


# THE GET ENDPOINT TO GET GENERAL STOCK RECOMMENDATIONS
@router.get("/trend_analysis/recommendations", description="Provide some recommendations on which stock to buy based on recent headlines and public sentiment!")
def stock_recommendations(start_date: str):

    # USER QUERY
    USER_QUESTION = "What are some stock recommendations?"  # To reduce my OpenAI credit usage, I directly used a query that is useful for Metaphor!

    # GET LINKS FROM METAPHOR
    link_ids, link_titles, link_urls = trend_analyzer.generate_links(user_prompt=USER_QUESTION, start_date=start_date)

    # CLEAN AND EXTRACT THE TEXT FROM THE LINKS
    headlines_list = trend_analyzer.clean_text(response_ids=link_ids)
    headlines = "\n".join(headlines_list)

    # SETTING UP OPENAI AGENT FOR GENERATING THE TRENDS BASED ON THE HEADLINES
    prompt = f"There is articles about stock recommendations. The articles are separated in '\\n'. The articles are {headlines}. \
               Please provide a detailed summary for each of these articles. \
               Determine the top 10 stocks all the articles together are recommending."

    # GETTING THE RESULTS
    results = trend_analyzer.openai_agent.get_response(prompt)
    summary = trend_analyzer.openai_agent.show_conversation()

    # RETURN THE RESPONSE
    return Response(content=f"These are the summaries of the articles I looked at:\n\n{summary['content']}", media_type="String")
