""" helper functions for the gitinterface """

import json
import logging
import subprocess
import re
try:
  from GitTokens import GITHUBTOKEN
except ImportError:
  raise ImportError("""Failed to import GITHUBTOKEN please point the pythonpath to your GitTokens.py file which contains your "Personal Access Token" for Github

                    I.e.:
                    Filename: GitTokens.py
                    Content:
                    ```
                    GITHUBTOKEN = "e0b83063396fc632646603f113437de9"
                    ```
                    (without the triple quotes)
                    """
                   )


def versionComp( v1, v2 ):
  """ compare version strings, problem is comparing
  v1r8p0 to v02-07-00 e.g. in lcio otherwise we could use normal string comparison

  needed for LCIO

  pre version are older than non-pre version

  """
  if v1 == v2:
    return 0

  pattern = re.compile( 'v([0-9]+)[r]([0-9]+)[-p]([0-9]+)')

  result1 = re.match( pattern, v1 )

  result2 = re.match( pattern, v2 )

  ## matching result1
  if result1 is not None and result2 is not None:
    ## both match, we can use string comparison
    pass
  elif result1 is not None and result2 is None:
    ## only 1 matches, 2 is always assumed to be bigger
    return -1
  elif result1 is None and result2 is not None:
    ## only 2 matches, 1 is considered bigger
    return 1
  else:
    ## neither matches, we can use string comparison
    pass

  if 'pre' in v1 and 'pre' in v2:
    ## use string comparison later
    pass

  elif 'pre' in v1:
    if v1.split('-pre')[0]==v2:
      return -1 # version 2 is not pre, so bigger
    return -1 if v1.split('-pre')[0] < v2 else 1

  elif 'pre' in v2:
    if v1==v2.split('-pre')[0]:
      return 1 # version 1 is not pre, so bigger
    return -1 if v1 <= v2.split('-pre')[0] else 1
  
  if v1 < v2:
    return -1
  else:
    return 1
  

def parseForReleaseNotes( commentBody ):
  """ will look for "BEGINRELEASENOTES / ENDRELEAENOTES" and extend releaseNoteList if there are entries """

  relNotes = []
  if not all( tag in commentBody for tag in ("BEGINRELEASENOTES", "ENDRELEASENOTES") ):
    return relNotes

  releaseNotes=commentBody.split("BEGINRELEASENOTES")[1].split("ENDRELEASENOTES")[0]
  relNotes.append( releaseNotes )
  # for entry in releaseNotes.split("*"):
  #   if entry.strip():
  #     relNotes.append( entry.strip() )

  return relNotes

def ghHeaders( ):
  """ return authorization header for github as used by curl

  :returns: tuple to be used in commands list
  """
  return '-H','Authorization: token %s' % GITHUBTOKEN


def getCommands( *args ):
  """ create a flat list

  :param *args: list of strings or tuples/lists
  :returns: flattened list of strings
  """
  comList = []
  for arg in args:
    if isinstance( arg, (tuple, list) ):
      comList.extend( getCommands( *arg ) )
    else:
      comList.append(arg)
  return comList


def curl2Json( *commands, **kwargs ):
  """ return the json object from calling curl with the given commands

  :param *commands: list of strings or tuples/lists, will be passed to `getCommands` to be flattend
  :returns: json object returned from the github or gitlab API
  """
  log = logging.getLogger("GitHub")
  commands = getCommands( *commands )
  commands.insert( 0, 'curl' )
  commands.insert( 1, '-s' )
  if kwargs.get("checkStatusOnly", False):
    commands.insert( 1, '-I' )
  cleanedCommands = list(commands)
  ## replace the github token with Xs
  if '-H' in cleanedCommands:
    cleanedCommands[commands.index('-H')+1] = cleanedCommands[commands.index('-H')+1].rsplit(" ", 1)[0] + " "+ "X"*len(cleanedCommands[commands.index('-H')+1].rsplit(" ", 1)[1])
  log.debug( "Running command: %r",  cleanedCommands )
  jsonText = subprocess.check_output( commands )
  try:
    jsonList = json.loads( jsonText )
  except ValueError:
    if kwargs.get("checkStatusOnly", False):
      return jsonText
    raise
  return jsonList



AUTHORMAP = {}
def authorMapping( username, commands ):
  """return the name of the author for given username, if not found query github
  PR for author via the commands given
  """
  log = logging.getLogger("Author")
  author = AUTHORMAP.get(username)
  if author is not None:
    log.debug( "Found author in map: %s", author)
    return author

  log.debug( "Checking Commits for Author ")
  commits = curl2Json( commands )
  author = commits[-1]['commit']['author']['name'] ## use the last commit of PR to get author
  AUTHORMAP[username] = author
  log.debug( "Found author: %s", author )
  return author


def checkRate():
  """ return the result for check_rate call """
  rate = curl2Json( ghHeaders(), "https://api.github.com/rate_limit" )
  logging.getLogger("Rate").info("Remaining calls to github API are %s of %s", rate['rate']['remaining'], rate['rate']['limit'] )

