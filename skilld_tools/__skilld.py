import os
import io
import json
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
import pdfkit
import jinja2


class __common():
    def __init__(self, parent=None):
      self.cwd = os.getcwd()
      self.home = os.environ['HOME']


    def init_dir(self, folder):
      if not os.path.exists(folder):
          os.makedirs(folder)


    def getConf(self, filepath):  
      with open(filepath) as data_file:
          data_loaded = json.load(data_file)
          return data_loaded


    def saveConf(self, filepath, data):
        with io.open(filepath, 'w', encoding='utf8') as outfile:
          __str = json.dumps(data, indent = 4, sort_keys = True, separators = (',', ': '), ensure_ascii = False)
          outfile.write(to_unicode(__str))


    def render(self, tpl_path, context):
        path, filename = os.path.split(tpl_path)
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename).render(context)


    def generate(self, template_path, data, destination):
        result = self.render(template_path, data)
        pdfkit.from_string(result, destination)

