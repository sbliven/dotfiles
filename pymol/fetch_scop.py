#!/usr/bin/python
from pymol import cmd,util
import urllib
import sys, os
import thread

def fetch_scop(sid, name=None, state=0, async=1, ver="1.75B", url="http://scop.berkeley.edu/astral/pdbstyle/", path=None, file=None, **kwargs):
    """DESCRIPTION

    Download the structure of a particular SCOP domain from the internet. 

USAGE

    fetch sid [,name [,state [,async [,version [,base-url ]]]]]

PYMOL API

    cmd.fetch_scop(string sid, string name, int state, int async,
        string version, string url, string path, string file, **kwargs)

ARGUMENTS

    sid = string: the SCOP id of your domain (i.e. "d1dlwa_" or "14982")

    name = string: name of the object {default: sid}

    state = integer: number of the state into which
    the content should be loaded, or 0 for append {default:0}

    async = integer: 0 to force synchronous execution {default:1}

    version = string: SCOP version to use {default: 1.75B}

    url = string: URL to fetch proteins from 
    {default: http://scop.berkeley.edu/astral/pdbstyle/}

    Other arguments will be passed directly to load.

NOTES

    Fetch_scop command loads structures asyncronously by default, meaning that
    the next command may get executed before the structures have been loaded.
    If you need synchronous behavior in order to insure that all structures are
    loaded before the next command is executed, please provide the optional
    argument "async=0".

    Fetch requires a direct connection to the internet and thus may
    not work behind certain types of network firewalls.

    Files are cached locally for future use. To change the cache location, use
        set fetch_path, /path/to/use
    You can also use the file parameter to control the output location precisely.

EXAMPLES

    
AUTHOR

    Spencer Bliven
"""
    def fetch_scop_async(sid, name, state, ver, url, file, **kwargs):
        fetch_path = cmd.get("fetch_path")
        if name is None:
            name = sid

        filename = file or os.path.join( fetch_path, "%s.pdb"%sid )
        if not os.path.isfile(filename):
            try:
                fullURL = "%s/ver=%s&id=%s&output=text" %(url,ver,sid)
                #print "Fetching %s"%fullURL
                result = urllib.urlretrieve(fullURL,filename)
                if not check_format(result):
                    print "Error-fetch-scop: unable to load '%s'"%sid
                    if os.path.isfile(filename):
                        os.remove(filename)
                    return
            except IOError, err:
                print str(err)
                return


        cmd.load(filename, name, state, format="pdb", **kwargs)

    if int(async):
        print "Fetchin async"
        thread.start_new_thread(fetch_scop_async, (sid, name, state, ver, url, file),kwargs)
    else:
        print "Fetchin sync"
        fetch_scop_async(sid, name, state, ver, url, file,**kwargs)

cmd.extend("fetch_scop",fetch_scop)

def check_format(result):
    """Unknown sids give an HTML file. Delete it and report error to the user
    """
    filename,httpMessage = result
    # Should always exist (otherwise would throw IOError above, but check anyway.
    if not os.path.isfile(filename):
        print "Error. File not found: %s" % filename
        return False

    if httpMessage.has_key('content-type') and httpMessage['content-type'] != 'text/plain':
        return False

    print str(httpMessage.items())

    return True


