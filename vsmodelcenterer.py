#!/usr/bin/python3

import pyjson5
import os
import sys

def left(element):
    # Check both Vintage Story and Blender symmetry conventions
    return element['name'].startswith('L ') or element['name'].startswith('left ') or element['name'].endswith('Left') or element['name'].endswith('.L')

def right(element):
    return element['name'].startswith('R ') or element['name'].startswith('right ') or element['name'].endswith('Right') or element['name'].endswith('.R')

def ensure_value(jobj, path, value):
    epsilon = 0.01
    if (jobj[path] == value):
        return False
    if isinstance(value, float):
        if value >= jobj[path] - epsilon and value <= jobj[path] + epsilon:
            return False
        value = round(value, 2)
    jobj[path] = value
    return True

def transform_model(model):
    changed = False
    for element in model['elements']:
        if 'stepParentName' in element:
            continue
        width = element['to'][2] - element['from'][2]
        if 'rotationOrigin' in element:
            changed = ensure_value(element['rotationOrigin'], 2, 8.0) or changed
        changed = ensure_value(element['from'], 2, 8.0 - width / 2) or changed
        changed = ensure_value(element['to'], 2, 8.0 + width / 2) or changed
        changed = transform_children(element) or changed
    return changed

def transform_children(element):
    changed = False
    width = element['to'][2] - element['from'][2]
    if not ('children' in element):
        return changed
    for child in element['children']:
        if left(child) or right(child):
            continue
        childwidth = child['to'][2] - child['from'][2]
        if 'rotationOrigin' in child:
            changed = ensure_value(child['rotationOrigin'], 2, width / 2.0) or changed
        changed = ensure_value(child['from'], 2, (width - childwidth) / 2.0) or changed
        changed = ensure_value(child['to'], 2, child['from'][2] + childwidth) or changed
        changed = transform_children(child) or changed
    return changed

def transform_file(f):
    fi = open(f, 'r+')
    try:
        verb = 'loading'
        in_text = fi.read()
        verb = 'parsing'
        j = pyjson5.decode(in_text, maxdepth=4096)
        verb = 'transforming'
        changed = transform_model(j)
        if (changed):
            verb = 'writing'
            fi.seek(0)
            fi.write(pyjson5.dumps(j))
            fi.truncate()
    except Exception as e:
        print('Exception while', verb, f)
        raise e
        return
    fi.close()
    if changed:
        print('Modified file ' + f)

def apply_function_to_files_recursive(source, function):
    if os.path.isdir(source):
        for root, dirs, files in os.walk(source):
            for f in files:
                function(os.path.join(root, f))
    else:
        function(source)
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: ' + sys.argv[0] + ' [file or folder]')
    else:
        apply_function_to_files_recursive(sys.argv[1], transform_file)
