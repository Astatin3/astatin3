import os

webroot = os.getcwd() + "/web/"

def openFile(path):
  if not os.path.exists(webroot + path):
    return ''
  try:
    with open(webroot + path) as f:
      return f.read()
  except:
    return ''
