import scrapy
import random


class AutomobilisspiderSpider(scrapy.Spider):
    handle_httpstatus_list = [301]
    name = "automobilisspider"
    allowed_domains = ["www.automobilis.lt"]
    start_urls = [
        # "https://www.automobilis.lt/paieskos-rezultatai/p,%d" % i for i in range(1, 586)
        "https://www.automobilis.lt/paieskos-rezultatai/p,569"
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
        cars = response.css("div.skelbimas .sfuf")

        for car in cars:
            car_url = car.css("a").attrib["href"]

            yield scrapy.Request(
                car_url,
                callback=self.parse_car_page,
                headers={
                    "User-Agent": self.user_agent_list[
                        random.randint(0, len(self.user_agent_list) - 1)
                    ]
                },
            )
            # yield {"url": car.css("a").attrib["href"]}

        # # Next page
        # next_page = (
        #     "https://www.automobilis.lt/" + response.css("a.bigNext").attrib["href"]
        # )

        # if next_page is not None:
        #     yield response.follow(
        #         next_page,
        #         callback=self.parse,
        #         headers={
        #             "User-Agent": self.user_agent_list[
        #                 random.randint(0, len(self.user_agent_list) - 1)
        #             ]
        #         },
        #     )

    def parse_car_page(self, response):
        parametrai = response.css("div.iL .iP ::text").getall()

        metai = None
        kebulo_tipas = None
        kuras = None
        darbinis_turis = None
        duru_skaicius = None
        pavaru_deze = None
        vairo_padetis = None
        rida = None
        galia = None
        bukle = None
        vardas = None
        telefonas = None

        for parametras in range(len(parametrai)):
            if response.css("div.iL .iP ::text")[parametras].get() == "Pagaminta:":
                metai = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Kėbulo tipas:":
                kebulo_tipas = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Kuro tipas:":
                kuras = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Darbinis tūris:":
                darbinis_turis = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Durų skaičius:":
                duru_skaicius = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Pavarų dėžė:":
                pavaru_deze = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Vairo padėtis:":
                vairo_padetis = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Rida:":
                rida = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Galia:":
                galia = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == ":":
                bukle = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Vardas:":
                vardas = response.css("div.iL .iR ::text")[parametras].get()

            if response.css("div.iL .iP ::text")[parametras].get() == "Telefonas:":
                telefonas = response.css("div.iL .iR ::text")[parametras].get()

        yield {
            "url": response.url,
            "pavadinimas": response.css("h1 ::text").get(),
            "kaina": response.css("div.spk span ::text").get(),
            "metai": metai,
            "kebulo_tipas": kebulo_tipas,
            "kuras": kuras,
            "darbinis_turis": darbinis_turis,
            "duru_sk": duru_skaicius,
            "pavaru_deze": pavaru_deze,
            "vairo_padetis": vairo_padetis,
            "rida": rida,
            "galia": galia,
            "bukle": bukle,
            "vardas": vardas,
            "telefonas": telefonas,
        }
