from core import Base, Scraper

hostname = "https://www.foxaholic.com/"
search_url = hostname + "?s="
suffix = "&post_type=wp-manga"

class Foxaholic(Base):
    def __init__(self):
        self.scraper = Scraper(hostname)

    def search(self, keyword):
        soup = self.scraper.cookSoup(search_url + keyword.lower().replace(" ", "+") + suffix)
        
        try:
            search_results = soup.find("div", {"class": "c-tabs-item"}).find_all("div", {"class": "row c-tabs-item__content"})
            resultsList = []
            for i in search_results:
                parent_tag = i.find("h3", {"class": "h4"})
                resultsList.append({
                    "title": parent_tag.a.text,
                    "link": parent_tag.a["href"]
                })
            return resultsList
        
        except AttributeError:
            return []