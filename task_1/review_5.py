urls = (page.url for page in browser.pages)
content_sizes = map(get_content_size, urls)
url2content_size = dict(zip(urls, content_sizes))