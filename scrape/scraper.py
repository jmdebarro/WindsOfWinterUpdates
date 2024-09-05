from bs4 import BeautifulSoup
import requests
import dotenv
import openai

class Scraper:
    """Class for scraping websites"""

    def __init__(self, url):
        self.soup = None
        self.valid = None
        self.url = url
        return
    
    def __str__(self):
        return f"URL - {self.url}\nVALID - {self.valid}"
    
    # Gets HTML from websites
    def scrape(self):

        # Get url content
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, 'html.parser')
        self.soup = soup
        return self
    

    # Parses GRRM Blog
    def blogParse(self):

        dotenv.load_dotenv()

        # post-main is class of divs containing post info
        parsed = self.soup.find("div", "post-main")
        parsed_p = parsed.find_all("p")
        parsed_text = (" ").join([tag.string for tag in parsed_p if tag.string])

        # OpenAI request to see if content contains WoW discussion
        client = openai.OpenAI()

        system = """You analyze text and answer either 'yes' or 'no', only one word as to whether or not this text contains 
                    information regarding the Winds of Winter book by George R.R. Martin"""
        
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": parsed_text}
        ]
        )

        # Yes or No response
        response = completion.choices[0].message.content.lower()
        self.valid = response == 'yes'
        return self


url = "https://georgerrmartin.com/notablog/"
test = Scraper(url)
print(test.scrape().blogParse())