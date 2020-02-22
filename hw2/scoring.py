import json
import os
import sys
from subprocess import Popen, PIPE


def read_config():
    with open(sys.argv[1]) as read_in:
        return json.load(read_in)


def save_config(obj):
    with open(sys.argv[1], 'w') as save_out:
        json.dump(obj, save_out, indent=2)


# load user setting
config = read_config()
rubrics = config['rubrics']


def get_script(k):
    global config, rubrics
    for v in config['scripts']:
        if v['file'] == k:
            return v


def compute_score(rcd):
    global config, rubrics
    score = int(rcd['check-time']['adjusted-max-score'])
    comment = []
    for k, v in rcd.items():
        if 'scripts' in k:
            # apply default judgement
            if bool(v['applied']):
                score -= int(get_script(k)['deduct'])
                comment.append(get_script(k)['comment'])
            # check for rubrics
            if 'rubrics' in v:
                for r in v['rubrics']:
                    score -= int(rubrics[r]['deduct'])
                    comment.append(rubrics[r]['comment'])
            # check for adjustments
            if 'user' in v:
                score -= int(v['user']['deduct'])
                comment.append(v['user']['comment'])
            # check for messages
            # if 'messages' in v:
            #     comment.append('message: ' + ';'.join(v['messages']))
    return max(score, 0), comment


def finalize(s):
    filename = os.path.join(config['dir-root'], config['dir-work'], s + '.json')
    if os.path.exists(filename):
        with open(filename) as f:
            log = json.load(f)
        score, comment = compute_score(log)
        return score, comment
    else:
        return 0, ["no submission"]


if len(sys.argv) < 2:
    raise ValueError("please provide a configuration file")

with open(sys.argv[2], newline='') as txtfile:
    while True:
        sid = txtfile.readline()
        if not sid:
            break
        sid = sid.lstrip('\n').rstrip('\n')
        score, comments = finalize(sid + "@ad3.ucdavis.edu")
        print('%-10s\t%3i' % (sid, score), end='\t')
        print('; '.join(comments))
