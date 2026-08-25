# -*- coding: utf-8 -*-
"""Stamp metadata on a rendered volume and install it into ~/personal/HLD-concepts."""
import os
import shutil
import sys

import fitz

DEST = '/Users/shivam.baghel/personal/HLD-concepts'
src, out_name, title = sys.argv[1], sys.argv[2], sys.argv[3]
doc = fitz.open(src)
doc.set_metadata({'title': title, 'subject': 'System design / interview playbook',
                  'author': '', 'keywords': '', 'creator': '', 'producer': ''})
tmp = src + '.stamped'
doc.save(tmp, garbage=4, deflate=True)
dest = os.path.join(DEST, out_name)
shutil.move(tmp, dest)
print('installed %s  (%d pages, %.1f MB)  %s'
      % (dest, len(doc), os.path.getsize(dest) / 1e6, title))
