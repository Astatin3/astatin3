from flask import Flask, render_template, session, request, send_from_directory
import utils

def run_flask(pages):
  app = Flask(__name__,
              static_url_path=utils.webroot,
              static_folder=utils.webroot,
              template_folder=utils.webroot)

  def find_page(path):
    try:
      page = pages[path]
      return navbar_template(page["title"], page["get_html"]())
    except:
      return navbar_template("ERROR", "<h1>Error!</h1>")

  def navbar_template(title: str, body: str):
    return (utils.openFile("static/navbar.html")
            .replace("<!-- title -->", title)
            .replace("<!-- body -->", body))

  @app.route('/')
  def flask_index():
    return find_page("index")

  @app.route('/<path:path>')
  def flask_page(path):
    return find_page(path)

  @app.route('/src/<path:file>')
  def flask_src_dir(file):
    return app.send_static_file("src/" + file)

  @app.route('/images/<path:file>')
  def flask_images_dir(file):
    return app.send_static_file("images/" + file)

  app.run(host='0.0.0.0', port=80, debug=True)