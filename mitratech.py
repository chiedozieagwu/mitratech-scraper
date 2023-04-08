import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from playwright.sync_api import Playwright, sync_playwright

urls = [
    'https://mitratech.com/resource-hub/webinars/',
    'https://mitratech.com/resource-hub/ebooks/',
    'https://mitratech.com/resource-hub/on-demand-webinars/',
    'https://mitratech.com/resource-hub/whitepapers/',
    'https://mitratech.com/resource-hub/analyst-reports/',
    'https://mitratech.com/resource-hub/case-studies/',
    'https://mitratech.com/resource-hub/expert-interviews/',
    'https://mitratech.com/resource-hub/infographics/',
    'https://mitratech.com/resource-hub/videos/'
    ]

# products = ['TeamConnect', 'TAP Workflow Automation', 'PolicyHub', 'eCounsel', 'DataStore', 'Cluster Seven', 'VendorInsight', 'Tracker I-9 Compliance', 'Acuity ELM', 'ImmigrationTracker', 'INSZoom', 'EraCLM', 'Alyne', 'LegalHold', 'Collaborati', 'Continuity', 'Quovant', 'Integrum', 'AdvanceLaw', 'AssureHire', 'TalentReef']

blog_content = []

for url in urls:
    product_urls = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(timeout=120000)
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US, en,q=0.5'
            }
        page.set_extra_http_headers(headers)
        page.goto(url)
        page.locator("a#filterby-product").click()
        dropdown_html = page.inner_html('section#page-content')
        dropdown_soup = bs(dropdown_html, 'html.parser')
        page.wait_for_load_state('domcontentloaded')
        dropdown_tags = dropdown_soup.select('div.res-filter.dropdown.show ul a')
        for hrefs in dropdown_tags:
            dropdown_href = hrefs['href']
            product_urls.append(dropdown_href)
            print(dropdown_href)
    for product_url in product_urls:
        r = requests.get(product_url, headers=headers)
        soup = bs(r.text, 'html.parser')

        products = soup.select('div.card-article-item.col-lg-4.col-md-6.d-flex.mb-2.mb-sm-3')
        if products:
            for product in products:
                title = product.select_one('a[title]')['title']
                try:
                    asset_type = product.select_one('div.card-subtitle.text-uppercase.font-size-sm a').text
                except:
                    asset_type = ' '
                asset_link = product.select_one('h4.card-title a.link-black')['href']
                try:
                    asset_text = product.select_one('p.card-text').text
                except:
                    asset_text = ' '
                if "teamconnect" in product_url:
                    product_name = 'TeamConnect'
                if "tap-workflow-automation" in product_url:
                    product_name = 'TAP Workflow Automation'
                if "policyhub" in product_url:
                    product_name = 'PolicyHub'
                if "ecounsel" in product_url:
                    product_name = 'eCounsel'
                if "datastore" in product_url:
                    product_name = 'DataStore'
                if "clusterseven" in product_url:
                    product_name = 'Cluster Seven'
                if "vendorinsight" in product_url:
                    product_name = 'VendorInsight'
                if "tracker-i-9" in product_url:
                    product_name = 'Tracker I-9 Compliance'
                if "acuity-elm" in product_url:
                    product_name = 'Acuity ELM'
                if "immigrationtracker" in product_url:
                    product_name = 'ImmigrationTracker'
                if "inszoom" in product_url:
                    product_name = 'INSZoom'
                if "cat" in product_url:
                    product_name = 'EraCLM'
                if "alyne" in product_url:
                    product_name = 'Alyne'
                if "legalhold" in product_url:
                    product_name = 'LegalHold'
                if "collaborati" in product_url:
                    product_name = 'Collaborati'
                if "continuity" in product_url:
                    product_name = 'Continuity'
                if "quovant" in product_url:
                    product_name = 'Quovant'
                if "integrum" in product_url:
                    product_name = 'Integrum'
                if "advancelaw" in product_url:
                    product_name = 'AdvanceLaw'
                if "assurehire" in product_url:
                    product_name = 'AssureHire'
                if "talentreef" in product_url:
                    product_name = 'TalentReef'

                details = {
                    'Product': product_name,
                    'Title': title,
                    'Asset Type': asset_type,
                    'Asset Link': asset_link,
                    'Asset Text': asset_text
                }
                blog_content.append(details)

                print(details)

df = pd.DataFrame(blog_content)
df.to_csv('mitratech.csv', index=False)