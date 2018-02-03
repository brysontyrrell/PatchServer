import sys
sys.path.insert(0, '/Library/PatchServer/')

from patchserver.factory import create_app

application = create_app()
