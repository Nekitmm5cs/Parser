import requests
from bs4 import BeautifulSoup

class BMW:
    def __init__(self, url):
        self.url = url
        self.info_elements = []
        self.car_data = []
        self.get_data()

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        car_name_elements = soup.find_all("h3", class_="listing__title")
        car_names = []
        for car_name_element in car_name_elements:
            car_names.append(car_name_element.text)
        return car_names

    def get_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            html = response.text
            self.main_parse_html(html)
        else:
            raise ValueError(f"Invalid response with status: {response.status_code}")

    def main_parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        car_name_elements = soup.find_all("h3", class_="listing__title")
        car_names = []
        for car_name_element in car_name_elements:
            car_names.append(car_name_element.text)
            print(car_names)
        car_elements = soup.find_all("div", class_='listing-item')

        for car_element in car_elements:
            car_info = {}
            photo_element = car_element.find("img", class_="ls-is-cached lazyloaded")
            link_element = car_element.find("a", class_="listing-item__link")
            name_element = car_element.find("span", class_="link-text")
            params_element = car_element.find("div", class_="listing-item__params")
            location_element = car_element.find("div", class_="listing-item__location")

            if name_element:
                car_info["name"] = name_element.text.strip()
            if photo_element:
                car_info["photo"] = photo_element.text.strip()
            if link_element:
                car_info["link"] = link_element["href"]
            if params_element:
                car_info["params"] = params_element.text.strip()
            if location_element:
                car_info["location"] = location_element.text.strip()

            self.car_data.append(car_info)

    def print_car_info(self):
        for car_info in self.car_data:
            print("Name: {}".format(car_info.get("name")))
            print("Link: {}".format(car_info.get("link")))
            print("Photo: {}".format(car_info.get("photo")))
            print("Params: {}".format(car_info.get("params")))
            print("Location: {}".format(car_info.get("location")))
            print("\n")

if __name__ == "__main__":
    URL = "https://cars.av.by/filter?brands[0][brand]=8&brands[0][model]=81&brands[0][generation]=11815&sort=2"
    bmw = BMW(URL)
    bmw.print_car_info()

