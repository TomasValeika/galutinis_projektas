import scrapy
import random


class AutobonusspiderSpider(scrapy.Spider):
    handle_httpstatus_list = [301]
    name = "autobonusspider"
    allowed_domains = ["www.autobonus.lt"]
    start_urls = [
        "https://www.autobonus.lt/auto/paieska/?cat=1&search=1&doSearch=1&collapsrch=1&cnt=561&ord=date&asc=desc"
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
        cars = response.css("a.item-link")
        for car in cars:
            car_url = car.attrib["href"]

            yield scrapy.Request(
                car_url,
                callback=self.parse_car_page,
                headers={
                    "User-Agent": self.user_agent_list[
                        random.randint(0, len(self.user_agent_list) - 1)
                    ]
                },
            )

        # Next page
        next_page = response.css("div.paginator a ::attr(href)")[-1].get()

        if next_page is not None:
            yield response.follow(
                next_page,
                callback=self.parse,
                headers={
                    "User-Agent": self.user_agent_list[
                        random.randint(0, len(self.user_agent_list) - 1)
                    ]
                },
            )

    def parse_car_page(self, response):
        parametru_bl = response.css("div.item-features-container")[3]
        parametrai = parametru_bl.css("div.left ::text").getall()

        marke = None
        modelis = None
        variklis = None
        pagaminimo_data = None
        rida = None
        kebulo_tipas = None
        kuras = None
        pavaru_deze = None
        duru_sk = None
        varantys_ratai = None
        vairo_padetis = None
        vin = None
        bukle = None

        for parametras in range(len(parametrai)):
            if parametru_bl.css("div.left ::text")[parametras].get() == "Markė":
                marke = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Modelis":
                modelis = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Variklis":
                variklis = parametru_bl.css("div.right ::text")[parametras].get()

            if (
                parametru_bl.css("div.left ::text")[parametras].get()
                == "Pagaminimo data"
            ):
                pagaminimo_data = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Rida":
                rida = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Kėbulo tipas":
                kebulo_tipas = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Kuro tipas":
                kuras = parametru_bl.css("div.right ::text")[parametras].get()

            if (
                parametru_bl.css("div.left ::text")[parametras].get()
                == "Pavarų\xa0dėžė"
            ):
                pavaru_deze = parametru_bl.css("div.right ::text")[parametras].get()

            if (
                parametru_bl.css("div.left ::text")[parametras].get()
                == "Durų\xa0skaičius"
            ):
                duru_sk = parametru_bl.css("div.right ::text")[parametras].get()

            if (
                parametru_bl.css("div.left ::text")[parametras].get()
                == "Varantieji ratai"
            ):
                varantys_ratai = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Vairo padėtis":
                vairo_padetis = parametru_bl.css("div.right ::text")[parametras].get()

            if (
                parametru_bl.css("div.left ::text")[parametras].get()
                == "Kėbulo numeris (VIN)"
            ):
                vin = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Būklė":
                bukle = parametru_bl.css("div.right ::text")[parametras].get()

        yield {
            "url": response.url,
            "kaina": response.css("div.price ::text").get(),
            "kliento_tipas": response.css("div.profile-data-info b ::text").get(),
            "telefonas": response.css("div.primary ::text").get(),
            "marke": marke,
            "modelis": modelis,
            "variklis": variklis,
            "pagaminimo_data": pagaminimo_data,
            "rida": rida,
            "kebulo_tipas": kebulo_tipas,
            "kuras": kuras,
            "pavaru_deze": pavaru_deze,
            "duru_sk": duru_sk,
            "varantys_ratai": varantys_ratai,
            "vairo_padetis": vairo_padetis,
            "vin": vin,
            "bukle": bukle,
        }


# response.css('div.item-features-container')[3].getall()
