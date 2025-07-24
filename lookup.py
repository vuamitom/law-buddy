import requests
from bs4 import BeautifulSoup

def search_article(query):
    """
    Searches articles on thuvienphapluat.vn and returns the href attribute
    of <a> tags found directly under <p> tags with class 'nqTitle' and
    a 'lawid' attribute.

    Args:
        query (str): The search keyword.

    Returns:
        list: A list of strings, where each string is the href of the
              matching <a> tag. Returns an empty list if no content is found
              or an error occurs.
    """
    url = f"https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword={query}&match=True&area=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error requesting the URL: {e}")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # Find all <p> tags with class 'nqTitle' and a 'lawid' attribute
    # The `attrs` argument allows checking for specific attributes
    nq_title_paragraphs = soup.find_all('p', class_='nqTitle', attrs={'lawid': True})

    for p_tag in nq_title_paragraphs:
        # Find the <a> tag directly under the current <p> tag
        a_tag = p_tag.find('a')
        if a_tag and 'href' in a_tag.attrs:
            results.append(a_tag['href'])

    return results

# curl 'https://thuvienphapluat.vn/van-ban/Bo-may-hanh-chinh/Luat-sua-doi-Luat-Dat-dai-Luat-Nha-o-Luat-Kinh-doanh-bat-dong-san-Luat-Cac-to-chuc-tin-dung-2024-612195.aspx' \
#   -H 'referer: https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=lu%E1%BA%ADt%20%C4%91%E1%BA%A5t%20%C4%91ai%20&area=0&type=0&status=0&lan=1&org=0&signer=0&match=True&sort=1&bdate=17/07/1945&edate=17/07/2025' \
#   -H 'upgrade-insecure-requests: 1' \
#   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' \
#   -b 'vqc=1; _ga=GA1.1.232254569.1752674590; G_ENABLED_IDPS=google; Culture=vi; __qca=P1-e95a8109-244e-44a9-b84f-6a402ca56e85; jiyakeji_uuid=cb1e9bb0-624d-11f0-833a-411d0f22b435; Cookie_VB=close; ruirophaply-covi19=17; ASP.NET_SessionId=p3qt3naj50acuy3a2qv2e0wj; __utma=173276988.232254569.1752674590.1752760844.1752760844.1; __utmc=173276988; __utmz=173276988.1752760844.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __uidac=016879020d31272fd6076fa8d12f4602; cto_bundle=kTzV6F9wVklER3JYSWc4UDNkQ2JzNXg2bnJJZEF2dWhaYyUyRlh4c3NEeXlCd2lLVUx5VGpBeG1nY0RPZllCbFhCelBWVFl3TVFHbiUyRnUlMkJLMUhldDNFTGxLOEJYUU13MjhkQjRnZXFtbCUyRjhtbmI2WFF3c2ZHTURkQnNkTWdRQVJrQnJTcEFDZ1JwcU44RzhzSXF3Y1h6d2R6eWFVbEhSeXFkNTdKRjhVNEhHM3hLS3NwdWs4RXNia2M5NnR6RW1kWXhkak9kU1EzV0VWa29YeEFuTUpEc3hTUGNEenclM0QlM0Q; __RC=4; __R=1; _uidcms=505192801946755517; __tb=0; __IP=0; memberga=Anonymous[2001:4860:7:812::dd]; __utmt=1; __utmb=173276988.16.9.1752762605800; _ga_PGVTRDMJGD=GS2.1.s1752760833$o3$g1$t1752762606$j59$l0$h0; _ga_BJ8R96BC8C=GS2.1.s1752760833$o3$g1$t1752762606$j59$l0$h0; _ga_E8YMVYW6Y9=GS2.1.s1752760834$o2$g1$t1752762606$j59$l0$h1402611222; __gads=ID=5b18f03691efe882:T=1752674596:RT=1752762608:S=ALNI_MaDtCRF7zwG30KGnuuOPl-cKFND3g; __gpi=UID=00001163df988b67:T=1752674596:RT=1752762608:S=ALNI_MZ5nozHCyRpDe41F2cC9EgtEgAdjQ; __eoi=ID=9b355a5bdf82d70a:T=1752674596:RT=1752762608:S=AA-AfjbSMthL_DhX_MpmVZ8Dssba; _dd_s=logs=1&id=289ba145-c53c-48d4-8f1c-259c0c20ffc4&created=1752760834126&expire=1752763508329; FCNEC=%5B%5B%22AKsRol_Ub6aFcpgWecoG6EauZciv0jjdKvr53-ZpTL3iQOQJgTIixjJems1GCvdd_mE5ixTAGLJFhbtgudMDDPE5LFD7IUynx2dFnGA3Z-XNuf6s62uVYnYKgF81Bf-AtqeWHmOJ1nun_39NG0G5rYpHYg-hfKCUNQ%3D%3D%22%5D%5D; __uif=__uid%3A505192801946755517%7C__ui%3A-1%7C__create%3A1750519281' \
#   -I
def read_article(url):
    """
    Fetches the content of a given URL, simulating the provided curl request,
    and extracts the text content of the div with id="tab1".

    Args:
        url (str): The URL of the article to read.

    Returns:
        str: The text content of the div with id="tab1", or an empty string
             if the div is not found or an error occurs.
    """
    headers = {
        # Only include the headers specified in the latest curl command
        'Referer': 'https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=lu%E1%BA%ADt%20%C4%91%E1%BA%A5t%20%C4%91ai%20&area=0&type=0&status=0&lan=1&org=0&signer=0&match=True&sort=1&bdate=17/07/1945&edate=17/07/2025',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        # The Cookie header from your curl command
        'Cookie': 'vqc=1; _ga=GA1.1.232254569.1752674590; G_ENABLED_IDPS=google; Culture=vi; __qca=P1-e95a8109-244e-44a9-b84f-6a402ca56e85; jiyakeji_uuid=cb1e9bb0-624d-11f0-833a-411d0f22b435; Cookie_VB=close; ruirophaply-covi19=17; ASP.NET_SessionId=p3qt3naj50acuy3a2qv2e0wj; __utma=173276988.232254569.1752674590.1752760844.1752760844.1; __utmc=173276988; __utmz=173276988.1752760844.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __uidac=016879020d31272fd6076fa8d12f4602; cto_bundle=kTzV6F9wVklER3JYSWc4UDNkQ2JzNXg2bnJJZEF2dWhaYyUyRlh4c3NEeXlCd2lLVUx5VGpBeG1nY0RPZllCbFhCelBWVFl3TVFHbiUyRnUlMkJLMUhldDNFTGxLOEJYUU13MjhkQjRnZXFtbCUyRjhtbmI2WFF3c2ZHTURkQnNkTWdRQVJrQnJTcEFDZ1JwcU44RzhzSXF3Y1h6d2R6eWFVbEhSeXFkNTdKRjhVNEhHM3hLS3NwdWs4RXNia2M5NnR6RW1kWXhkak9kU1EzV0VWa29YeEFuTUpEc3hTUGNEenclM0QlM0Q; __RC=4; __R=1; _uidcms=505192801946755517; __tb=0; __IP=0; memberga=Anonymous[2001:4860:7:812::dd]; __utmt=1; __utmb=173276988.16.9.1752762605800; _ga_PGVTRDMJGD=GS2.1.s1752760833$o3$g1$t1752762606$j59$l0$h0; _ga_BJ8R96BC8C=GS2.1.s1752760833$o3$g1$t1752762606$j59$l0$h0; _ga_E8YMVYW6Y9=GS2.1.s1752760834$o2$g1$t1752762606$j59$l0$h1402611222; __gads=ID=5b18f03691efe882:T=1752674596:RT=1752762608:S=ALNI_MaDtCRF7zwG30KGnuuOPl-cKFND3g; __gpi=UID=00001163df988b67:T=1752674596:RT=1752762608:S=ALNI_MZ5nozHCyRpDe41F2cC9EgtEgAdjQ; __eoi=ID=9b355a5bdf82d70a:T=1752674596:RT=1752762608:S=AA-AfjbSMthL_DhX_MpmVZ8Dssba; _dd_s=logs=1&id=289ba145-c53c-48d4-8f1c-259c0c20ffc4&created=1752760834126&expire=1752763508329; FCNEC=%5B%5B%22AKsRol_Ub6aFcpgWecoG6EauZciv0jjdKvr53-ZpTL3iQOQJgTIixjJems1GCvdd_mE5ixTAGLJFhbtgudMDDPE5LFD7IUynx2dFnGA3Z-XNuf6s62uVYnYKgF81Bf-AtqeWHmOJ1nun_39NG0G5rYpHYg-hfKCUNQ%3D%3D%22%5D%5D; __uif=__uid%3A505192801946755517%7C__ui%3A-1%7C__create%3A1750519281'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error requesting the URL: {e}")
        return ""

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the div with id="tab1"
    tab1_div = soup.find('div', id='tab1')

    if tab1_div:
        return tab1_div.get_text(strip=True)
    else:
        print(f"Div with id='tab1' not found on {url}")
        return ""

def search_law(query):
    articles = search_article(query)
    results = []
    for article_url in articles[:5]:
        content = read_article(article_url)
        results.append(content)
    return results