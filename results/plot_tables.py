#!/usr/bin/env python3

import csv
import mmap
import sys
import os
from os import listdir
from os.path import isfile, join
from re import search
from graphviz import Digraph
import re

def file_contains(filename, id):
    with open(filename) as f:
        if id in f.read():
            return True
    return False

def find_files_cotains(id, folder=''):
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    result = []
    for f in files:
        if (file_contains(folder+f, id)):
            result.append(f)
    return result

def load_table(filename, folder=''):
    result={}
    with open(folder+filename) as fin:
        reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
        columns = next(reader)
        for c in columns:
            result[c] = []
        for row in reader:
            for c, v in zip(columns, row):
                result[c].append(v)
    return result

def is_relation(table):
    return 'source' in table and 'target' in table

def is_id(val):
    return re.search('^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', val) is not None

def get_label(row):
    if 'name' in row: return row['name']
    if 'time' in row: return 'Time'
    return '-'

def get_row(id, table):
    for i in range(len(table['id'])):
        row_id = table['id'][i]
        if(row_id != id):
            continue
        cols = table.keys()
        return {c:table[c][i] for c in cols}
    return None

def create_node(row, file):
    global styles
    attrs = styles['general']
    file = file.replace('.csv', '')
    if(file in ['consent', 'collect', 'combine', 'disclose', 'erase', 'profile', 'pseudonymize', 'retrieve', 'store', 'update']):
        attrs = styles['activity']
    elif(file in ['personal_data', 'consent_request','withdraw_request']):
        attrs = styles['entity']
    elif(file in ['subject', 'controller', 'processor']):
        attrs = styles['agent']
    elif(file in ['time']):
        attrs = styles['annotation']

    id = row['id']
    label = '{}\n{}\n{}...'.format(get_label(row), file, id[:8])
    dot.node(id, label, fillcolor=attrs['fillcolor'], style='filled', shape=attrs['shape'])

# def plot_id(id, tracked_ids, folder=''):
def plot_id(id, folder=''):
    files = find_files_cotains(id, folder)
    for f in files:
        if (not f == 'relation.csv'):
            table = load_table(f, folder)
            row = get_row(id, table)
            if(row is not None):
                create_node(row, f)
                return (row, f)
    return None, None



# def find_all_pairs(id, relations, tracked_ids):
def find_all_pairs(id, relations):
    result = []
    for src, dst in zip(relations['source'], relations['target']):
        if (src == id):# and dst not in tracked_ids):
            result.append((src, dst))
            # return dst
        if (dst == id):# and src not in tracked_ids):
            result.append((src, dst))
            # return src
    return result

styles = {
    'general': {
        'fillcolor': 'white',
        'shape':     'circle'
    },
    'activity': {
        'fillcolor': '#a3caea',
        'shape':     'box'
    },
    'entity': {
        'fillcolor': '#f8ea2f',
        'shape':     'ellipse'
    },
    'agent': {
        'fillcolor': '#f0aeae',
        'shape':     'house'
    },
    'annotation': {
        'fillcolor': 'white',
        'shape':     'note'
    }
}


relations = load_table('tables/relation.csv')
total_relations = len(relations['id'])

id = sys.argv[1]
folder = 'tables/' if len(sys.argv) < 3 else sys.argv[2]
tracked_ids = []
tracked_ctrl_proc_ids = []
dot = Digraph(comment='The Tables')

is_controller = lambda a: 'controller' in a
is_processor = lambda a: 'processor' in a

queue = [id]
rel = []
while(len(queue) > 0):
    current_id = queue.pop(0)
    if current_id not in tracked_ids:
        tracked_ids.append(current_id)

        _, f = plot_id(current_id, folder)
        pairs_id = find_all_pairs(current_id, relations)

        if is_controller(f) or is_processor(f):
            tracked_ctrl_proc_ids.append(current_id)

        for src, dst in pairs_id:
            if(current_id == src and dst not in tracked_ids): queue.append(dst)
            if (not is_controller(f) and not is_processor(f)):
                if(current_id == dst and src not in tracked_ids): queue.append(src)
                if((src, dst) not in rel): rel.append((src, dst))
            elif src in tracked_ctrl_proc_ids and dst in tracked_ctrl_proc_ids:
                # TODO: improve this conditional. It should consider all IDs, not just those already visited.
                if((src, dst) not in rel): rel.append((src, dst))


dot.edges(rel)



dot.render('graph-prov-{}.gv'.format(id), view=True)
