import os
import re

PATTERN_RE = '^[^\.]+\.(gif|png|jpg|jpeg|tiff|bmp)$'

def find_patterns(d):
    patterns = []

    for root, dirs, files in os.walk(d):
        disp_root = os.path.relpath(root, d)
        if disp_root == '.':
            disp_root = ''
        p = []
        for f in files:
            if re.match(PATTERN_RE, f, re.I):
                p.append(os.path.join(disp_root, f))
        patterns.append((disp_root, p))

    patterns[:1] = patterns[0][1]    # Don't return relpath for root dir
    return patterns

def find_patterns_flat(d):
    patterns = []
    for root, dirs, files in os.walk(d):
        for f in files:
            if re.match(PATTERN_RE, f, re.I):
                patterns.append(os.path.join(root, f))
    return patterns
