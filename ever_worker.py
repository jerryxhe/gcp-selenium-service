#!/usr/bin/env python2

import sys
if len(sys.argv) >= 2:
  email = sys.argv[1]
  from ever_util import *
  if email in email2token:
    reTitleFromAttachment(email2token[email], "2x")
    rename_attachments(email2token[email])
    index2mysql(email2token[email], "2x")
