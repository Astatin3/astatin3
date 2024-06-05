import src.utils as utils
import json

def get_blog_main_html():
  pass

def get_blog_html(page):
  try:
    blog_json = json.loads(utils.open_file(f"blogs/{page}"))
  except Exception as e:
    print(e)
    return "Error!"

def get_html(path):
  print(path)

  if len(path) > 2:
    return get_blog_html(path[1])
  else:
    return get_blog_main_html()

  return "Error!"

def init():
  pass