#!/usr/bin/env python

def handler(signum,frame):
  print ( "Terminating" )
  sys.exit(1)

def setHandler():
  try:
    import signal, sys
  except Exception:
    return

  for i in (signal.SIGINT,signal.SIGHUP,signal.SIGTERM):
    signal.signal(i, handler)
