#!/usr/bin/env python

import argparse
import functools
import json
import os
import re
import signal
import subprocess
import time

parser = argparse.ArgumentParser(description='Run benchmarks')
parser.add_argument('--config',
                    dest='config',
                    default='config.json',
                    type=str,
                    help='a configuration file for benchmarking')

# All benchmarks are run against [wrk](https://github.com/wg/wrk)
WRK_CMD = ['wrk', '-t10', '-d10s', 'http://127.0.0.1:8080/hello']

HEADERS = ['name', 'version', 'lang', 'avg latency', 'requests/sec', 'transfer/sec']

def run_cmd(stage, cmd):
    ''' 
    Given a stage (setup, teardown) and a cmd ['python', 'bench.py'],
    run the command and wait for it to finish before returning from
    this function. cmd can optionally be a list of lists to provide
    the ability to run a series of commands in a stage.
    ''' 
    if cmd is None:
        print 'No %s command. Skipping.' % stage
        return

    print '%s: %s' % (stage, ' '.join(cmd))

    # Handle a list of lists for multiple step setup/teardowns
    if isinstance(cmd[0], list):
        for c in cmd:
            run_cmd(c, stage)

    p = subprocess.Popen(args=cmd)
    output, err = p.communicate()
    if err:
        print 'Error in %s: %s' % (stage, err)
        os.exit(1)
    p.wait() 


setup = functools.partial(run_cmd, 'setup')
teardown = functools.partial(run_cmd, 'teardown')


def load_config(config_file):
    '''
    Load a benchmark configuration file. By default,
    the script uses ./config.json
    '''
    with open(config_file) as json_file:
        return json.load(json_file)


def parse_wrk_output(output):
    '''
    Takes the following output from the wrk command line
    tool and converts the desired values into a dictionary.

    Running 10s test @ http://127.0.0.1:8080/hello
      10 threads and 10 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     0.85ms    4.69ms 104.87ms   97.47%
        Req/Sec     5.36k     1.58k   11.25k    72.06%
      534601 requests in 10.10s, 57.10MB read
    Requests/sec:  52912.31
    Transfer/sec:      5.65MB
    '''
    latency_re = re.compile(r"Latency\s*([\.\d\w]*)")
    requests_sec_re = re.compile(r"Requests/sec:\s*([\.\d]*)")
    transfer_sec_re = re.compile(r"Transfer/sec:\s*([\.\d\w]*)")
    return {
        'latency': latency_re.findall(output)[0],
        'requests_sec': float(requests_sec_re.findall(output)[0]),
        'transfer_sec': transfer_sec_re.findall(output)[0]
    }


def execute(cmd, env=None, wait=None):
    '''
    Build benchmark data for a given item in the configuration
    '''
    p = subprocess.Popen(args=cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         env=env)
    if wait is None:
        for line in iter(p.stdout.readline, b''):
            if line.strip() == 'begin benchmark':
                break
    else:
        time.sleep(wait)

    cmd_str = ' '.join(cmd)
    print 'benchmarking:', cmd_str 
    b = subprocess.Popen(WRK_CMD, stdout=subprocess.PIPE)
    
    output, err = b.communicate()

    if err is not None:
        print 'Error during benchmark run of %s : %s', (err, cmd_str)

    b_status = b.wait()
    p.terminate()
    return parse_wrk_output(output)

def generate_table(headers, rows):
    '''
    Given a list of headers and a list of list of rows,
    generate github flavored markdown for tables
    '''
    delim = ' | '
    table = ''
    table += delim.join(headers) + '\n'
    table += delim.join(['-------'] * len(headers)) + '\n'

    for row in rows:
        # Make sure we have a list of strings as requests/sec will
        # be a float for sortability
        row = [str(c) for c in row]
        table += delim.join(row) + '\n'
    return table


def update_readme(table):
    readme_file = open('readme.md')
    readme = readme_file.read()
    readme_file.close()

    readme = re.sub('benchmarks\n[\-]*[\s\S]*$', '', readme)
    readme += 'benchmarks\n'
    readme += '----------\n'
    readme += table

    readme_file = open('readme.md', 'w')
    readme_file.write(readme)
    readme_file.close()


if __name__ == '__main__':
    args = parser.parse_args()
    config = load_config(args.config)
    results = []
    for proc in config:
        setup(proc.get('setup'))
        benchmarks = execute(proc.get('command'),
                             env=proc.get('env'),
                             wait=proc.get('wait'))
        teardown(proc.get('teardown'))
        results.append((
            proc['name'],
            proc.get('version', ''),
            proc['language'],
            benchmarks['latency'],
            benchmarks['requests_sec'],
            benchmarks['transfer_sec'],
        ))

    sort_index = HEADERS.index("requests/sec")
    results = sorted(results, key=lambda r: -r[sort_index])
    table = generate_table(HEADERS, results)
    update_readme(table)
    runs = len(config)
    print 'Completed %s run%s' % (runs, 's' if runs > 1 else '')
