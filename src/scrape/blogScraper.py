from bs4 import BeautifulSoup
import requests
import dotenv
import openai
import datetime

class Scraper:
    """Class for scraping websites"""

    def __init__(self, url):
        self.soup = None
        self.valid = None
        self.date = None
        self.url = url
        return
    
    def __str__(self):
        return f"URL - {self.url}\nVALID - {self.valid}\nDATE - {self.date}"
    
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
        self.date = parsed.find("div", "thedate")
        parsed_p = parsed.find_all("p")
        parsed_text = (" ").join([tag.string for tag in parsed_p if tag.string])

        # response = self.analyzePost(parsed_text)
        # self.valid = response == 'yes'
        return self
    

    # OpenAI analyzes text to see if it contains Winds of Winter details
    def analyzePost(self, blog_post):
        # OpenAI request to see if content contains WoW discussion
        client = openai.OpenAI()

        system = """You analyze text and answer either 'yes' or 'no', only one word as to whether or not this text contains 
                    information regarding the Winds of Winter book by George R.R. Martin"""
        
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": blog_post}
        ]
        )

        # Yes or No response
        response = completion.choices[0].message.content.lower()
        return response


    # Formats GRRM date into datetime
    def getDate(self):
        # Date formatted like "September 3, 2024 at 11:54 am"
        date = self.date.split()[:3]
        date[1] = date[1][:-1]
        day, month, year = date[1], str(datetime.datetime.strptime(date[0], '%B').month), date[2]
        month =  "0" + month if len(month) < 2 else month
        day = "0" + day if len(day) < 2 else day

        # Create datetime object
        blog_date = datetime.date.fromisoformat(f"{year}-{month}-{day}")
        date_delta = datetime.timedelta(days=2)
        current_date = datetime.date.today()
        
        new = current_date - blog_date < date_delta
        return new
    
url = "https://georgerrmartin.com/notablog/"
test = Scraper(url)
# print(test.scrape().blogParse())

# test.date = "September 4, 2024 at 11:54 am"
# print(test.getDate())