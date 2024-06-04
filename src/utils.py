import os
import importlib
from sys import platform

webroot = os.getcwd() + "/web/"


def get_root(path):
  rootdir = os.getcwd() + f'/{path}'

  if platform in ['nt', 'win32', 'win64']:
    rootdir = rootdir.split(':')[1].replace('\\', '/')

  return rootdir

def open_file(path):
  if not os.path.exists(path):
    return ''
  try:
    with open(path) as f:
      return f.read()
  except:
    return ''

def open_web_file(path):
  return open_file(webroot + path)


def open_page_file(page_name, file):
  return open_file(f'{get_root("pages")}/{page_name}/{file}')


def load_script(path, name):
  spec = importlib.util.spec_from_file_location(name, get_root(path))
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module