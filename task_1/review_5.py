urls = (page.url for page in browser.pages)
content_sizes = map(get_content_size, urls)
url2content_size = {}
for url, size in zip(urls, content_sizes):
    url2content_size[url] = size

# from itertools import zip_longest
#
# urls = (page.url for page in browser.pages)
# content_sizes = map(get_content_size, urls)
# url2content_size = dict(zip_longest(urls, content_sizes, fillvalue=0))