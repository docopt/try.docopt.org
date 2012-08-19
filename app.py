"""Naval Fate.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored|--drifting]
  naval_fate.py -h | --help
  naval_fate.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""
import os, sys, traceback, json
from StringIO import StringIO

from flask import Flask, render_template as render, request
from docopt import docopt, DocoptLanguageError


app = Flask(__name__)


def run_docopt(doc, argv):
    real_stdout, sys.stdout = sys.stdout, StringIO()
    real_stderr, sys.stderr = sys.stderr, StringIO()
    try:
        sys.stdout.write(json.dumps(docopt(doc, argv), sort_keys=True,
                                    separators=(',\n ', ': ')))
    except SystemExit as e:
        sys.stderr.write(e.code)
    except Exception as e:
        if type(e) is DocoptLanguageError:
            sys.stderr.write('DocoptLanguageError: %s' % e)
        else:  # in case something went wrong
            traceback.print_exc(file=sys.stderr)
    result = sys.stdout.getvalue() + sys.stderr.getvalue()
    sys.stdout = real_stdout
    sys.stderr = real_stderr
    return result


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        args = run_docopt(request.form['doc'], request.form['argv'])
        return render('index.html', args=args,
                      doc=request.form['doc'],
                      argv=request.form['argv'])
    else:
        return render('index.html', doc=__doc__,
                                    argv='ship Guardian move 10 50 --speed=20')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG')
    app.run(debug=debug, host='0.0.0.0', port=port)
