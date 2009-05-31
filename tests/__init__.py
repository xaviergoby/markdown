import os
import markdown
import codecs
import difflib
import nose
import util 
from plugins import MdSyntaxError, HtmlOutput, MdSyntaxErrorPlugin
from test_apis import *

test_dir = os.path.abspath(os.path.dirname(__file__))

def normalize(text):
    return ['%s\n' % l for l in text.strip().split('\n')]

def check_syntax(file, config):
    input_file = file + ".txt"
    input = codecs.open(input_file, encoding="utf-8").read()
    output_file = file + ".html"
    expected_output = codecs.open(output_file, encoding="utf-8").read()
    output = normalize(markdown.markdown(input, 
                                         config.get('DEFAULT', 'extensions'),
                                         config.get('DEFAULT', 'safe_mode'),
                                         config.get('DEFAULT', 'output_format')))
    diff = [l for l in difflib.unified_diff(normalize(expected_output),
                                            output, output_file, 
                                            'actual_output.html', n=3)]
    if diff:
        raise util.MdSyntaxError('Output from "%s" failed to match expected '
                                 'output.\n\n%s' % (input_file, ''.join(diff)))

def test_markdown_syntax():
    for dir_name, sub_dirs, files in os.walk(test_dir):
        # Get dir specific config settings.
        config = util.CustomConfigParser({'extensions': '', 
                                          'safe_mode': False,
                                          'output_format': 'xhtml1'})
        config.read(os.path.join(dir_name, 'test.cfg'))
        # Loop through files and generate tests.
        for file in files:
            root, ext = os.path.splitext(file)
            if ext == '.txt':
                yield check_syntax, os.path.join(dir_name, root), config

nose.main(addplugins=[HtmlOutput(), MdSyntaxErrorPlugin()])
