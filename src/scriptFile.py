from scrape.blogScraper import Scraper
from email.emailer import Emailer

# Check for new Winds of Winter updates
url = "https://georgerrmartin.com/notablog/"
blog = Scraper(url)

# Whether or not there is an update
update = blog.scrape().valid

if update:
    email = Emailer()
    email.email()