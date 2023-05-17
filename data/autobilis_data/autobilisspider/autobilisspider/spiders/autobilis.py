import scrapy
import random


class AutobilisSpider(scrapy.Spider):
    handle_httpstatus_list = [301]
    name = "autobilis"
    allowed_domains = ["www.autobilis.lt"]
    start_urls = [
        "https://www.autobilis.lt/skelbimai/naudoti-automobiliai?order_by=created_at-desc&category_id=1&page=2"
    ]

    user_agent_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    ]

    def parse(self, response):
        cars = response.css("div.search-rezult-content a")
        for car in cars:
            car = car.attrib["href"]

            yield scrapy.Request(
                car,
                callback=self.parse_autobilis_page,
                headers={
                    "User-Agent": self.user_agent_list[
                        random.randint(0, len(self.user_agent_list) - 1)
                    ]
                },
            )

        next_page = response.css("ul.pagination a")[-2].attrib["href"]
        if next_page is not None:
            next_page_url = "https://www.autobilis.lt/" + next_page
            yield response.follow(
                next_page_url,
                callback=self.parse,
                headers={
                    "User-Agent": self.user_agent_list[
                        random.randint(0, len(self.user_agent_list) - 1)
                    ]
                },
            )

    def parse_autobilis_page(self, response):
        info = response.css("div.advert-price-MainInfo-title")

        headers = info.css("div.car-info-h p ::text").getall()

        Marke = None
        Modelis = None
        Pagaminimo_data = None
        darbinis_turis = None
        galia = None
        pavaru_deze = None
        kuras = None
        kebulas = None
        varantieji_ratai = None
        rida = None
        duru_skaicius = None
        vairo_padetis = None
        bukle = None
        vin = None

        for header in range(len(headers)):
            if info.css("div.car-info-h p ::text")[header].get() == "Markė":
                Marke = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Modelis":
                Modelis = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Pagaminimo data":
                Pagaminimo_data = info.css("div.car-info-c b ::text")[header].get()

            if (
                info.css("div.car-info-h p ::text")[header].get()
                == "Darbinis tūris, l."
            ):
                darbinis_turis = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Galia, kW":
                galia = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Pavarų dėžė":
                pavaru_deze = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Kuro tipas":
                kuras = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Kėbulo tipas":
                kebulas = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Varantieji ratai":
                varantieji_ratai = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Rida":
                rida = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Durų skaičius":
                duru_skaicius = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Vairo padėtis":
                vairo_padetis = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "Būklė":
                bukle = info.css("div.car-info-c b ::text")[header].get()

            if info.css("div.car-info-h p ::text")[header].get() == "VIN numeris":
                vin = info.css("div.car-info-c b ::text")[header].get()

        yield {
            "url": response.url,
            "id": response.css("span.advert-id ::text").get(),
            "pardavejas": response.css("div.connect-container-title ::text").get(),
            "telefonas": response.css("div.clearfix ::text")[3].get(),
            "vardas": response.css("div.clearfix ::text")[8].get(),
            "miestas": response.css("div.clearfix ::text")[13].get(),
            "kaina": response.css("span.price-value ::text").get(),
            "title": response.css("h1 ::text")[0].get(),
            "marke": Marke,
            "modelis": Modelis,
            "pagaminimo_data": Pagaminimo_data,
            "darbinis_turis": darbinis_turis,
            "galia": galia,
            "pavaru_deze": pavaru_deze,
            "kuras": kuras,
            "kebulas": kebulas,
            "varantieji_ratai": varantieji_ratai,
            "rida": rida,
            "duru_skaicius": duru_skaicius,
            "vairo_padetis": vairo_padetis,
            "bukle": bukle,
            "vin": vin,
        }
