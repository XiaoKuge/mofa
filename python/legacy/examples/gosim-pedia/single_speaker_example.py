from openai import OpenAI
if __name__ == "__main__":
    client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="sk-jsha-1234567890")
    user_input = """
    Sray Agarwal
Head of Responsible AI (EMEA & APAC) at Infosys
linkedin
Sray Agarwal has applied AI and analytics from Financial Services to Hospitality and has led the development of Responsible AI framework for multiple banks in the UK and the US.
Based out of London, his is conversant in Predictive Modelling, Forecasting and advanced Machine Learning with profound knowledge of algorithms and advanced statistic, Sray is Head of Responsible AI (EMEA & APAC) at Infosys.
He is an active blogger and has given his talks on Ethical AI at major AI conferences across the globe (more than 20) and has podcasts, video interviews and lectures on reputed websites and social media at United Nations, Microsoft, ODSC to name a few.
His contribution to the development of the technology was recognised by Microsoft when he won the Most Valued Professional in AI award in 2020 to 2025. He is also an expert for United Nations (UNCEFACT) and have recently authored a book on Responsible AI published by Springer.
He has been a trainer with leading consulting firms and have delivered training on business transformation using AI. He is guest lecturer at Jio institute. He holds patents on RAI system and methods.
    """
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":user_input},
    ],
    )
    result = response.choices[0].message

    print(response)