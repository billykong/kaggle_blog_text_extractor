from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
import time
import sys
import re

"""
This scraper is built for generating pure text file for typing execrises

Usage:
python scraper https://blog.kaggle.com/2017/01/31/scraping-for-craft-beers-a-dataset-creation-tutorial/

"""


def main(sourceURL):
    driver = webdriver.Chrome(
        executable_path='/Users/billykong/workspace/github/scraper/webdriver/chromedriver')
    # add checking for http preffix
    driver.get(sourceURL)
    # time.sleep(2)
    pageSoup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()

    # html = open('blog.html')
    # pageSoup = BeautifulSoup(html, 'lxml')

    title = ""
    content = ""

    try:
        title = pageSoup.title.string
    except BaseException:
        pass

    content = pageSoup.find("div", {"role": "main"})

    [tag.unwrap() for tag in content.findAll(["ul", "li", "a", "em"])]
    [c.unwrap() for c in content.findAll(
        "code", {"class": "highlighter-rouge"})]
    [c.decompose() for c in content.findAll(["code", "table"])]
    [c.decompose() for c in content.findAll(
        "div", {"class": "syntaxhighlighter"})]
    [t.decompose() for t in content.findAll(
        "a", {"class": "meta-comments"})]  # why not working???

    # wrap h* and p tags with <div>\n</div>
    [tag.insert(0, NavigableString("\n"))
     for tag in content.findAll(["p", "h1", "h2", "h3", "h4", "h5"])]

    contentText = content.get_text()
    while re.compile(r'\n*\s\n*\s\n').search(contentText):
        contentText = re.sub('\n*\s\n*\s\n', '\n\n', contentText)

    filename = 'result.txt'
    with open(filename, 'w') as out:
        out.write('Title:' + '\n')
        out.write(title + '\n\n')
        out.write(contentText)

    result = {"title": title,
              "content": contentText}
    return result


if __name__ == "__main__":
    main(sys.argv[1])
