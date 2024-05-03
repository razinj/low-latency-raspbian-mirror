from typing import Any
from scrapy import Spider
from scrapy.http import Response


class MirrorsSpider(Spider):
    name = "mirrors"
    allowed_domains = ["www.raspbian.org"]
    start_urls = ["https://www.raspbian.org/RaspbianMirrors"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        data_list = response.xpath(
            '//div[@id="content"]/div/table/tbody/tr/td/p/text()'
        ).getall()

        def filter_fn(value: str):
            if value.startswith(("http", "(http")):
                return True

            return False

        def standardize_fn(value: str):
            return value.strip()

        standarized_data_list = map(standardize_fn, data_list)
        filtered_data_list = filter(filter_fn, standarized_data_list)

        def all_http_fn(value: str):
            first_para_index = value.index("(")
            last_para_index = value.index(")")

            return value[:first_para_index] + "http" + value[last_para_index + 1 :]

        all_http_data_list = list(map(all_http_fn, filtered_data_list))

        print(f"Found {len(all_http_data_list)} URLs")

        for _, item in enumerate(all_http_data_list):
            if "http://" not in item:
                continue

            yield {"url": item}
