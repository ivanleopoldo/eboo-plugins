from core import Base, Scraper

hostname = "http://ranobes.net/"
search_url = hostname + "index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story="

class Ranobes(Base):
    def __init__(self):
        self.scraper = Scraper(hostname)

    def search(self, keyword: str):
        if keyword == "":
            return []

        soup = self.scraper.cook_soup(search_url + keyword.lower().replace(" ", "+"))

        try:
            search_results = soup.find("div", id="dle-content").find_all("article", {"class": "block story shortstory mod-poster"})
            resultsList = []
            for i in search_results:
                parent_tag = i.find("div", {"class": "short-cont"}).find("h2", {"class": "title"})
                resultsList.append({
                    "title": parent_tag.a.text,
                    "link": parent_tag.a["href"]
                })

        except AttributeError: 
            return []