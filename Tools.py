#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()

class Tools():
    def push(self, comment):
        t.run('git add .')
        t.run('git commit -m "{}"'.format(comment))
        t.run('git push origin')

    def pull(self):
        t.run("""
git fetch --all
git reset --hard origin/master
""")

py.make_it_runnable()
py.fire(Tools)
