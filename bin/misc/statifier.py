#!/usr/bin/python3

import os
from optparse import OptionParser
import shutil

class Statifier:

  def __init__(self, domain, languages):
    self.domain = domain
    self.languages = languages
    self.replace_dict = {
    }

  def wget(self, language, dir):
    command = 'wget -q --mirror -p --adjust-extension --header="Accept-Language: %s" -e robots=off --base=./ -k -P %s https://%s' % (language, dir, self.domain)
    # print(command)
    os.system(command)

  def sed(self, dir, rule):
    command = "find %s -type f -print0 | xargs -0 sed -r -i -e '%s'" % (dir, rule)
    # print(command)
    os.system(command)

  def fix_languages(self, language):
    for root, dirs, files in os.walk(self.domain):
      for filename in files:
        name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1][1:]
        if ext == 'html':
          path = root + os.sep + filename
          rel_root = root.split('/')[2:]
          rel_root = language + '/' + '/'.join(rel_root)

          f = open(path, 'rt')
          content = f.read()
          f.close()

          s_in = '<form action="https://%s/i18n/" method="post" class="c-header__languages">' % self.domain
          s_out = ''
          content = content.replace(s_in, s_out)

          s_in = '<button class="c-header__language is-active" type="submit" name="language" value="%s">%s</button>' % (language, language.upper())
          s_out = '<a href="/%s/">' + s_in + '</a>'
          s_out = s_out % rel_root
          content = content.replace(s_in, s_out)

          s_in = '<button class="c-header__language" type="submit" name="language" value="%s">%s</button>' % (language, language.upper())
          s_out = '<a href="/%s/">' + s_in + '</a>'
          s_out = s_out % rel_root
          content = content.replace(s_in, s_out)

          f = open(path, 'wt')
          f.write(content)
          f.close()

  def main(self):
    for language in self.languages:
      self.wget(language, self.domain)
      shutil.move(self.domain + os.sep + self.domain, self.domain + os.sep + language)

    for language in self.languages:
      self.fix_languages(language)


def main():
  parser = OptionParser()
  parser.add_option("-d", "--domain", dest="domain", help="domain")
  parser.add_option("-l", "--languages",
                  dest="languages", nargs=2,
                  help="languages")
  (options, args) = parser.parse_args()

  s = Statifier(options.domain, options.languages)
  s.main()

if __name__ == "__main__":
  main()

