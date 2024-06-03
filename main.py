import os
import utils
import web

def html_home():
  return utils.openFile("home.html")

def blocks_home():
  return utils.openFile("home.html")

pages = {
  "home": {
    "title": "Home",
    "get_html": html_home
  },
  "blocks": {
    "title": "Blocks",
    "get_html": blocks_home
  }
}
if __name__ == '__main__':
   web.run_flask(pages)
