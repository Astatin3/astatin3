import os
import json

import src.utils as utils

def load_pages():
  module_folders = os.listdir(utils.get_root('pages'))

  return_pages = {}
  return_tabs = []

  for folder in module_folders:
    # try:
      page_json = json.loads(open(utils.get_root(f'pages/{folder}/page.json')).read())

      new_page = {}

      new_page['title'] = page_json['title']
      new_page['module'] = utils.load_script(f"pages/{folder}/{page_json['entrypoint']}", folder)
      new_page['get_html'] = new_page['module'].get_html


      if page_json['tab']:
        new_tab = {}
        new_tab['title'] = page_json['title']
        new_tab['href'] = page_json['path']
        return_tabs.insert(page_json['tab_index'], new_tab)


      return_pages[page_json['path']] = new_page

      print(f"Loaded {utils.get_root(f'pages/{folder}')}")
    # except Exception as e:
    #   print(f"Failed to load \"{utils.get_root(f'pages/{folder}')}\" Error: \"{e}\"")


  return return_pages, return_tabs