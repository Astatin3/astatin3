import src.web as web

from src.pages import load_pages

# pages = {
#   "index": {
#     "title": "Home",
#     "get_html": html_home
#   },
#   "blocks": {
#     "title": "Blocks",
#     "get_html": blocks_home
#   }
# }

if __name__ == '__main__':
  web_pages, web_tabs = load_pages()
  web.run_flask(web_pages, web_tabs)
