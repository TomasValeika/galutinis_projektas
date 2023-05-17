import scrapy
import random


class AutogidasspiderSpider(scrapy.Spider):
    handle_httpstatus_list = [301]
    name = "autogidasspider"
    allowed_domains = ["autogidas.lt"]
    start_urls = [
        "https://autogidas.lt/skelbimai/automobiliai/?f_434[0]=Naudotas&f_1[0]=&f_model_14[0]=&f_50=kaina_asc&page=1"
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
        cars = response.css(
            "article.list-item"
        )  # Automobilio gabalas kuriame yra pradine informacija

        for car in cars:
            car_url = (
                "https://autogidas.lt/" + car.css("a.item-link").attrib["href"]
            )  # Vieno automobilio url

            yield scrapy.Request(
                car_url,
                callback=self.parse_car_page,
                headers={
                    "User-Agent": self.user_agent_list[
                        random.randint(0, len(self.user_agent_list) - 1)
                    ]
                },
            )  # Uzeiti i kiekvieno automobilio vidu

        # Next page
        next_page = response.css("div.paginator a ::attr(href)")[-1].get()

        if next_page is not None:
            next_page_url = "https://autogidas.lt" + next_page

            yield response.follow(
                next_page_url,
                callback=self.parse,
                headers={
                    "User-Agent": self.user_agent_list[
                        random.randint(0, len(self.user_agent_list) - 1)
                    ]
                },
            )

    def parse_car_page(self, response):
        skelbimo_id = response.css("div.params-block-times")
        parametru_bl = response.css("div.params-block")[1]
        parametrai = parametru_bl.css("div.left ::text").getall()

        marke = None
        modelis = None
        metai = None
        kuras = None
        kebulas = None
        pavaru_deze = None
        duru_sk = None
        variklis = None
        vairo_padetis = None
        defektai = None
        rida = None
        varantys_ratai = None

        for parametras in range(len(parametrai)):
            # tikriname parametrus
            if parametru_bl.css("div.left ::text")[parametras].get() == "Markė":
                marke = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Modelis":
                modelis = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Metai":
                metai = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Kuro tipas":
                kuras = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Kėbulo tipas":
                kebulas = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Pavarų dėžė":
                pavaru_deze = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Durų skaičius":
                duru_sk = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Variklis":
                variklis = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Vairo padėtis":
                vairo_padetis = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Defektai":
                defektai = parametru_bl.css("div.right ::text")[parametras].get()

            if parametru_bl.css("div.left ::text")[parametras].get() == "Rida":
                rida = parametru_bl.css("div.right ::text")[parametras].get()

            if (
                parametru_bl.css("div.left ::text")[parametras].get()
                == "Varomieji ratai"
            ):
                varantys_ratai = parametru_bl.css("div.right ::text")[parametras].get()

        yield {
            "url": response.url,
            "skelbimo_id": skelbimo_id.css("div.times-item-right ::text")[-1].get(),
            "telefono_nr": response.css("div.seller-phones span ::text").get(),
            "kaina": response.css("div.price ::text").get(),
            "marke": marke,
            "modelis": modelis,
            "metai": metai,
            "kuras": kuras,
            "kebulas": kebulas,
            "pavaru_deze": pavaru_deze,
            "duru_sk": duru_sk,
            "variklis": variklis,
            "vairo_padetis": vairo_padetis,
            "defektai": defektai,
            "rida": rida,
            "varantys_ratai": varantys_ratai,
        }


# Parametrai
# p = response.css('div.params-block')[1]
# p.css('div.right ::text').getall() <- Auto duomenys
# p.css('div.left ::text').getall() <- Parametrai

# Naudojami parametrai
# Markė +
# Modelis +
# Metai +
# Kuro tipas +
# Kėbulo tipas +
# Pavarų dėžė +
# Durų skaičius +
# Variklis +
# Vairo padėtis +
# Defektai +
# Rida +
# Varomieji ratai
