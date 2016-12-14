#!/usr/bin/python

"""multirtail.py: Watch logfiles and pipe them to rtail stdin."""

__author__ = "Magnus Lindvall <magnus.lindvall@stendahls.se>"

import os
import glob
import shlex
from subprocess import Popen, PIPE
from os import path
from os.path import basename
import yaml
import pyinotify

class Config(object):
    def __init__(self, cfgfile):
        if path.exists(cfgfile):
            try:
                with open(cfgfile, 'r') as cfgfile:
                    self.config = yaml.load(cfgfile)
            except Exception as e:
                print "Error '{0}' occured. Arguments {1}.".format(e.message, e.args)

    def get_config(self):
        return self.config

class Multirtail(pyinotify.ProcessEvent):
    def __init__(self, config):
        self.config = config.get_config()
        self._manager = pyinotify.WatchManager()
        self._notify = pyinotify.Notifier(self._manager, self)
        self._paths = {}
        paths = self.config['multirtail']['paths']
        for p in paths:
            for expanded_path in glob.glob(p):
                self._manager.add_watch(expanded_path, pyinotify.IN_MODIFY)
                fh = open(expanded_path, 'rb')
                fh.seek(0, os.SEEK_END)
                self._paths[os.path.realpath(expanded_path)] = [fh, '']

    def run(self):
        while True:
            self._notify.process_events()
            if self._notify.check_events():
                self._notify.read_events()

    def process_default(self, evt):
        pathname = evt.pathname
        fh, buf = self._paths[pathname]
        data = fh.read()
        lines = data.split('\n')
        if buf:
            lines[0] = buf + lines[0]
        if lines[-1]:
            buf = lines[-1]
        lines.pop()

        if self.config['multirtail']['debug']:
            print "%s changed" % pathname, "\n".join(lines)

        args = []
        args.extend([self.config['rtail']['cmd'],
                     '--id', basename(pathname), '--host',
                     self.config['rtail']['host']])
        args += shlex.split(self.config['rtail']['args'])

        if self.config['multirtail']['showchanges']:
            p = Popen(args, stdin=PIPE)
        else:
            f = open(os.devnull, 'w')
            p = Popen(args, stdin=PIPE, stdout=f)

        for line in lines:
            logline = (line + '\n')
            stdin = p.stdin.write(logline)
            if self.config['multirtail']['debug']:
                print "Pid: %s" % p.pid
                print "Stdin: %s" % stdin
        p.stdin.close()
        self._paths[pathname][1] = buf

def main():
    config = Config('config.yml')
    Multirtail(config).run()

if __name__ == '__main__':
    main()
