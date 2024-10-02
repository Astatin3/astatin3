from flask import Flask
import src.utils as utils

def run_flask(pages, tabs):
  app = Flask(__name__,
              static_url_path=utils.webroot,
              static_folder=utils.webroot,
              template_folder=utils.webroot)

  def find_page(path):
    try:
      page = pages[path[0]]
      content, is_raw = page["get_html"](path)
      if is_raw:
        return content
      else:
        return navbar_template(page["title"], content)
    except Exception as e:
      print(f"Error loading page /{'/'.join(path)}, error: {e}")
      return navbar_template("ERROR", "<h1>Error!</h1>")

  def tab_template(tabs):
    html = ""
    for tab in tabs:
      html += (utils.open_web_file("static/tab.html")
               .replace("<!-- title -->", tab["title"])
               .replace("<!-- href -->", "/"+tab["href"]))

    return html


  def navbar_template(title: str, body: str):
    return (utils.open_web_file("static/navbar.html")
            .replace("<!-- title -->", title)
            .replace("<!-- body -->", body)
            .replace("<!-- tabs -->", tab_template(tabs)))


  def error_path_traversal():
    return (utils.open_web_file("static/navbar.html")
            .replace("<!-- title -->", "Nu uh")
            .replace("<!-- body -->", "Nu uh")
            .replace("<!-- tabs -->", tab_template(z)))


  @app.route('/')
  def flask_index():
    return find_page(["index"])

  @app.route('/<path:page>')
  def flask_page(page):
    if '..' in page:
      return error_path_traversal()
    return find_page(page.split('/'))

  @app.route('/src/<path:file>')
  def flask_src_dir(file):
    if '..' in file:
      return error_path_traversal()
    return app.send_static_file("src/" + file)

  @app.route('/images/<path:file>')
  def flask_images_dir(file):
    if '..' in file:
      return error_path_traversal()
    return app.send_static_file("images/" + file)

  app.run(host='0.0.0.0', port=8080, debug=False)
