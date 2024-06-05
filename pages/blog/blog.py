import src.utils as utils
import json

def get_blog_main_html():
  blogs = utils.list_subdirs('blogs')
  blog_html = []
  for blog in blogs:
    try:
      blog_json = json.loads(utils.open_file(f"blogs/{blog}/blog.json"))
      html = utils.open_page_file('blog', 'blog_insert.html')
      html = html.replace("<!-- subtitle -->", blog_json['subtitle'])
      html = html.replace("<!-- title -->", blog_json['title'])
      html = html.replace("<!-- image -->", blog_json['image'])
      html = html.replace("<!-- href -->", blog)
      html = html.replace("<!-- name -->", blog)

      blog_html.append(html)
    except:
      continue
  html = utils.open_page_file('blog', 'blog_main_page.html')
  return html.replace('<!-- html -->', ''.join(blog_html))

def get_blog_html(page):
  try:
    blog_json = json.loads(utils.open_file(f"blogs/{page}/blog.json"))
    html = utils.open_page_file("blog", "blog_page.html")
    html = html.replace("<!-- html -->", utils.open_file(f"blogs/{page}/{blog_json['page']}"))
    html = html.replace("<!-- title -->", blog_json['title'])
    html = html.replace("<!-- image -->", blog_json['image'])
    html = html.replace("<!-- name -->", page)

    return html
  except Exception as e:
    print(e)
    return "Error!"



def get_blog_src(blog, src):
  try:
    return utils.open_file_raw(f"blogs/{blog}/{src}")
  except Exception as e:
    print(e)
    return "Error"

def get_html(path):
  print(path)

  match(len(path)):
    case 1:
      return get_blog_main_html(), False
    case 2:
      return get_blog_html(path[1]), False
    case 3:
      return get_blog_src(path[1], path[2]), True
    case _:
      return "Error!"

def init():
  pass