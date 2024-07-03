import requests
import json
import time
from bs4 import BeautifulSoup
import re
import concurrent.futures
import pandas as pd


def fetch_url(func, url):
    if not url:
        return ""
    return func(url)


# 失败重试装饰器
def retry(func):
    def wrapper(*args, **kwargs):
        for i in range(4):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"get error {args[1]} 第{i+1}次重试：{e}")
                time.sleep(1)
        return func(*args, **kwargs)

    return wrapper


class PoemScraper:
    """
    爬取《古诗文选》网的古诗文
    """

    COOKIES = {
        "_ga": "GA1.2.1708416337.1719827428",
        "_gid": "GA1.2.871281696.1719827428",
        "_ga_69YE6Q6PR6": "GS1.2.1719827429.1.0.1719827429.0.0.0",
        "Hm_lvt_e20a3613f02b877462a888180936f6ee": "1719827436",
        "_gushici_session": "c09KY1k4ZjduT0xzbVRUN3M2czVLcTNnUWNsaXQ4VXdvWEF6VVpGc0gzZGlBRVdsMUxvNGF2Q1dBVnBONWp5a2ZQbHFVcFV5VHJ4RGRuY3RyMXFQOEdCQ2lFVnJyN3J4L280b2ZsV1N2UTVrUGpVUGNGVU5sMGhFdW5FU3hRUEpSQjFhNHJxVDhLZ3VyQitSOVNGQnlBPT0tLWVjZlpqR2sralFCaHBJZTA5Q1VzR1E9PQ%3D%3D--29d6ed8ba3fb84a7ab849d9faa82ef0eea672343",
        "Hm_lpvt_e20a3613f02b877462a888180936f6ee": "1719894375",
    }

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh,en;q=0.9,zh-CN;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    def __init__(self):
        self.base_url = "https://dugushici.com"
        self.results = []

    @retry
    def get_soup(self, url, params=None):
        """
        获取网页的soup对象
        :param url: 网页地址
        """
        self.HEADERS["referer"] = url
        if params:
            response = requests.get(
                url,
                headers=self.HEADERS,
                params=params,
                timeout=10,
                cookies=self.COOKIES,
            )
        else:
            response = requests.get(
                url, headers=self.HEADERS, timeout=10, cookies=self.COOKIES
            )
        response.raise_for_status()  # Raises an error for bad status
        return BeautifulSoup(response.text, "html.parser")

    def get_content(self, url):
        """
        获取网页的正文、解释、背景、鉴赏
        """
        print(f"Fetching {url}")
        soup = self.get_soup(url)
        content_div = soup.find("div", class_="content")
        content = content_div.get_text(separator="\n")

        annotations, background, appreciation = "", "", ""
        links = []
        try:
            annotations_link = (
                soup.find("h3", string="译文及注释")
                .find_next_sibling()
                .find("a")["href"]
            )
        except Exception as e:
            annotations_link = ""

        try:
            background_link = (
                soup.find("h3", string="创作背景").find_next_sibling().find("a")["href"]
            )
        except Exception as e:
            background_link = ""
        try:
            appreciation_link = (
                soup.find("h3", string=re.compile("鉴赏|赏析|评析"))
                .find_next_sibling()
                .find("a")["href"]
            )

        except Exception as e:
            appreciation_link = ""
        links = [annotations_link, background_link, appreciation_link]
        print(links)
        # 加快下载速度
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            urls = []
            for hres in links:
                if hres:
                    urls.append(self.base_url + hres)
                else:
                    urls.append("")
            funcs = [self.get_annotations, self.get_background, self.get_appreciation]

            # 使用 map 方法确保结果顺序与任务提交顺序一致
            results = list(executor.map(fetch_url, funcs, urls))
            annotations, background, appreciation = results

        return content, annotations, background, appreciation

    def get_annotations(self, url):
        """
        获取解释
        """
        soup = self.get_soup(url)
        annotation_div = soup.find("div", class_="shangxicont")
        original_url_div = annotation_div.find("div", class_="original_url")
        if original_url_div:
            original_url_div.decompose()
        return annotation_div.get_text(separator="\n").strip()

    def get_background(self, url):
        """
        获取背景
        """
        soup = self.get_soup(url)
        background_div = soup.find("div", class_="shangxicont")
        original_url_div = background_div.find("div", class_="original_url")
        if original_url_div:
            original_url_div.decompose()
        return background_div.get_text(separator="\n").strip()

    def get_appreciation(self, url):
        """
        获取鉴赏
        """
        soup = self.get_soup(url)
        appreciation_div = soup.find("div", class_="shangxicont")
        original_url_div = appreciation_div.find("div", class_="original_url")
        if original_url_div:
            original_url_div.decompose()
        return appreciation_div.get_text(separator="\n").strip()

    def get_poems(self, page, category=1):
        """
        获取古诗文列表
        :param page: 页码
        :param category: 分类
        """
        params = {
            "page": f"{page}",
            "q[prose_series_id_eq]": f"{category}",
        }
        time.sleep(0.5)
        url = f"{self.base_url}/ancient_proses/query"
        soup = self.get_soup(url, params=params)

        table = soup.find("div", class_="pagination").find_previous_sibling()
        trs = table.find_all("tr")[1:]

        for tr in trs:
            tds = tr.find_all("td")
            title = tds[0].text.strip()
            dynasty = tds[1].text.strip()
            author = tds[2].text.strip()
            content_url = self.base_url + tds[0].find("a")["href"]
            content, annotations, background, appreciation = self.get_content(
                content_url
            )
            yield {
                "title": title,
                "dynasty": dynasty,
                "author": author,
                "content": content,
                "annotations": annotations,
                "background": background,
                "appreciation": appreciation,
            }

    def scrape_poems(self, categories, pages):
        for category in categories:
            for page in pages:
                print(f"Scraping category {category}, page {page}")
                try:
                    poems = self.get_poems(page, category)
                    for poem in poems:
                        self.results.append(poem)
                except Exception as e:
                    print(f"Failed to scrape category {category}, page {page}: {e}")
                    break

    def save_results(self, filename):
        # 使用pandas 去重
        df = pd.DataFrame(self.results)
        df.drop_duplicates(inplace=True)
        df = df.drop_duplicates(subset=["title", "dynasty", "author"])
        df.to_json(filename, indent=4, orient="records", force_ascii=False)

    def run(self, categories, pages, output_filename):
        self.scrape_poems(categories, pages)
        self.save_results(output_filename)
        print(
            f"Scraping completed. {len(self.results)} records saved to {output_filename}."
        )


if __name__ == "__main__":
    # 获取全部古诗文
    # scraper = PoemScraper()
    # categories = range(1, 30)  # 示例分类
    # pages = range(1, 34)  # 示例页数
    # output_filename = "all_peoms_v2.json"
    # scraper.run(categories, pages, output_filename)

    # 测试
    scraper = PoemScraper()
    categories = range(1, 2)  # 示例分类
    pages = range(1, 2)  # 示例页数
    output_filename = "peom_data.json"
    scraper.run(categories, pages, output_filename)
