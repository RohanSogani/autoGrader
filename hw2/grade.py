import os, sys, time, platform, json, shutil
from subprocess import Popen, PIPE


def read_config():
    with open(sys.argv[1]) as read_in:
        return json.load(read_in)


def save_config(obj):
    with open(sys.argv[1], 'w') as save_out:
        json.dump(obj, save_out, indent=2)


# ------------------------------------------------------------------------------
# global variables
# ------------------------------------------------------------------------------

if len(sys.argv) < 2:
    raise ValueError("please provide a configuration file")

# load user setting
config = read_config()
rubrics = config['rubrics']

# ------------------------------------------------------------------------------
# functions
# ------------------------------------------------------------------------------


def print_rubrics():
    global rubrics
    for i, _ in enumerate(rubrics):
        print(i, end=' ')
        print(json.dumps(_, indent=4))


def add_rubric(deduct, comment):
    global rubrics
    r = {
        'deduct': int(deduct),
        'comment': comment
    }
    rubrics.append(r)
    save_config(config)
    return len(rubrics) - 1


def log_message(arr, msg):
    arr.append(msg)
    print(msg)


def question(msg):
    return input('%s%s%s ' % ('\033[91m', msg, '\033[0m'))


def print_warning(msg):
    print('%s%s%s' % ('\033[91m', msg, '\033[0m'))


def print_message(msg):
    print('%s%s%s' % ('\033[92m', msg, '\033[0m'))


def time_stamp(file):
    # we need a slightly different command for macOS
    if platform.system() == 'Darwin':
        cmd = f'''
        stat -f "%m" -t "%Y" {file}
        '''
    else:
        cmd = f'''        
        stat -c "%Y" {file}
        '''

    # run it
    bash = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    o, e = bash.communicate(cmd.encode('utf-8'))
    outs = o.decode('utf-8').strip().split('\n')
    errs = e.decode('utf-8').split('\n')
    t = int(outs[0])
    return t, outs, errs


def time_check(person):  # checking if the submission is over-due
    # user defined variables
    global config
    due = int(config['due-time-stamp'])
    tot = int(config['max-score'])
    tar = config['tarball']
    work_dir = os.path.join(config['dir-root'], config['dir-submissions'], person)

    # check for tarball's submission timestamp
    t, outs, errs = time_stamp(os.path.join(work_dir, tar))
    hour = 3600

    # can update the rubric manually here
    try:
        print(t)
        if t <= due + hour * 0:
            tot = tot
            log_message(errs, 'on time')
        elif due + hour * 0 < t <= due + hour * 1:
            tot *= 0.9
            log_message(errs, 'late by 0+ hour')
        elif due + hour * 1 < t <= due + hour * 2:
            tot *= 0.8
            log_message(errs, 'late by 1+ hours')
        elif due + hour * 2 < t <= due + hour * 3:
            tot *= 0.7
            log_message(errs, 'late by 2+ hours')
        elif due + hour * 3 < t <= due + hour * 4:
            tot *= 0.6
            log_message(errs, 'late by 3+ hours')
        else:
            tot *= 0
            log_message(errs, 'late by 4+ hours')
    except:
        print_warning('Is it exception')
        raise

    ret = {
        'messages': errs,
        'time': t,
        'adjusted-max-score': int(tot)
    }
    return ret


def reset_workdir(person):
    global config
    # reset the directory
    dst_dir = os.path.join(config['dir-root'], config['dir-work'], person)
    src_dir = os.path.join(config['dir-root'], config['dir-submissions'], person)
    src = os.path.join(src_dir, config['tarball'])
    dst = os.path.join(dst_dir, config['tarball'])
    try:
        shutil.rmtree(dst_dir, True)  # delete the old one
        os.mkdir(dst_dir)  # recreate the new one
        shutil.copy(src, dst)
#    except OSError:
#        print_warning(f'Resetting the directory {dst_dir} failed')
#        raise # this should not happen, thus raise
    except FileNotFoundError as err:
        print_warning(err)
        return True
    else:
        print(f'>> Successfully reset the directory {dst_dir}')
        return False


def message_filter(x):  # filter function that removes empty strings
    if len(x) == 0:
        return False
    if 'Warning: File \'Makefile\' has modification time' in x:
        return False
    if 'warning:  Clock skew detected.' in x:
        return False
    return True


def process_job(task, person):
    # the command to run
    global config
    workdir = os.path.join(config['dir-root'], config['dir-work'], person)
    script = os.path.join(config['dir-root'], task['file'])
    cmd = f'''
    cd {workdir}
    bash {script} {config['tarball']}
    '''

    # run the command and gather outputs
    bash = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    o, e = bash.communicate(cmd.encode('utf-8'))
    msg = []
    try:
        msg += filter(message_filter, o.decode('utf-8').strip().split('\n'))
        msg += filter(message_filter, e.decode('utf-8').split('\n'))
    except UnicodeDecodeError as e:
        question('Cannot decode output string? Please check manually.')
        msg.append(str(e))

    # if there is no output and no errors, consider the result as a pass
    ret = {}
    if len(msg) == 0:

        # the script passed
        print(f'pass {script}')
        ret['applied'] = False

    else:

        # the script failed
        print_warning(f'Failed {task["file"]} with Errors:')
        for _ in msg:
            print(_)
        ret['messages'] = msg

        # there is a default deduction rule
        print_message(f'Default rubric: (-{int(task["deduct"])}) {task["comment"]}')

        # check if we should apply the default rubric
        if ('apply' in task) and bool(task['apply']):
            # yes apply it
            ret['applied'] = True

        else:
            # check if we want to apply a rubric
            print_message('Use a rubric? Available rubrics are:')
            print_rubrics()
            print_message('Enter "y" to discard the current ')
            print_message('Enter "n" to cancel the discard')
            print_message('Enter "l" to list currently applied rubrics')
            print_message('Enter Integer for existing rubrics')
            print_message('Enter "a" to add existing rubrics')
            print_message('Enter "r" to remove existing rubrics')
            print_message('Enter "m" to edit manual adjustments')

            def fun_write_log(key, value, append):
                if key not in ret:
                    ret[key] = []
                if append:
                    ret[key].append(value)
                else:
                    ret[key] = value
                return None

            def fun_set_default_rubric(value):
                return fun_write_log('applied', bool(value), False)

            def fun_add_rubric():
                i = add_rubric(question(f'\tdeduct:'), question(f'\tcomment:'))
                return fun_write_log('rubrics', i, True)

            def fun_rm_rubric():
                i = question(f'  Enter the rubric index to delete')
                if i.isdigit() and int(i) in ret['rubrics']:
                    ret['rubrics'].remove(int(i))
                return None

            def fun_list():
                print('applied', ret['applied'] if 'applied' in ret else False)
                print('rubrics', ret['rubrics'] if 'rubrics' in ret else [])
                print('user', ret['user'] if 'user' in ret else [])
                return None

            def fun_default(idx):
                if idx.isdigit():
                    return fun_write_log('rubrics', int(idx), True)
                else:
                    print_warning('Unrecognizable choice. Please choose again.')
                    return None

            switcher = {
                'y': lambda: fun_set_default_rubric(False),
                'n': lambda: fun_set_default_rubric(True),
                'l': lambda: fun_list(),
                'a': lambda: fun_add_rubric(),
                'r': lambda: fun_rm_rubric(),
                'm': lambda: fun_write_log('user', {
                        'deduct': int(question(f'\tdeduct:')),
                        'comment': question(f'\tcomment:')
                    }, False)
            }

            # apply it by default, just for convenience
            ret['applied'] = True

            while True:
                choice = question('Your choice?')
                if not choice:
                    break

                # Get the function from switcher dictionary
                func = switcher.get(choice, lambda: fun_default(choice))
                func()

    return ret


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
    return max(score, 0), comment


def record(fname, obj, key, value, t):
    obj[key] = value
    obj[key]['timestamp'] = t
    with open(fname, 'w') as out:
        json.dump(obj, out, indent=2)


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------

# start processing timer
start_time = time.time()

# initialize students
students = []

# prepare a list of all submitted students
results, _ = Popen(['ls', os.path.join(config['dir-root'], config['dir-submissions'])],
                   stdout=PIPE, stderr=PIPE, encoding='utf8').communicate()
for item in results.split():
    if '@' in item:  # only consider kerberos@ad3.ucdavis.edu
        students.append(item)

# now grading one by one
print()
s_n = len(students)
s_i = 0
for s in students:

    # the path of the record file
    filename = os.path.join(config['dir-root'], config['dir-work'], s + '.json')

    # the student has not been graded
    missing = False
    if os.path.exists(filename):
        with open(filename) as f:
            log = json.load(f)
    else:
        missing = reset_workdir(s)
        log = dict()

    s_i += 1
    print('>> (%i/%i) working on student %s <<' % (s_i, s_n, s))

    # missing submission, we fake the state
    if missing or (('check-time' in log) and (log['check-time']['time'] == -1)):
        record(filename, log, 'check-time', {
            'messages': "submission is missing",
            'time': -1,
            'adjusted-max-score': 0
        }, -1)
        print()
        print()
        continue

    # step 1, we check the submission time
    if 'check-time' not in log:
        record(filename, log, 'check-time', time_check(s), -1)

    # step 2, we iterate over all grading scripts
    for job in config['scripts']:
        name = job['file']
        timestamp, _, _ = time_stamp(os.path.join(config['dir-root'], job['file']))
        if (name not in log) or ('timestamp' not in log[name]) or (int(log[name]['timestamp']) < timestamp):
            record(filename, log, name, process_job(job, s), timestamp)

    # check score
    # print(json.dumps(log, indent=2))
    print_message(f'Done!, score: {compute_score(log)}')
    print()
    print()

print("Time to process", len(students), "students was %s seconds" % (time.time() - start_time))
