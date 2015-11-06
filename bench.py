#!/usr/bin/env python
import os
import re
import signal
import subprocess
import time

wrk_cmd = ['wrk', '-t10', '-d10s', 'http://127.0.0.1:8080/hello']

def run_cmd(cmd, stage):
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

def setup(cmd):
    run_cmd(cmd, 'setup')

def teardown(cmd):
    run_cmd(cmd, 'teardown')

def load_config():
    return [
        {
            'name': 'go',
            'language': 'go',
            'setup': ['go', 'build', 'webserver.go'],
            'command': ['./webserver'],
            'teardown': ['rm', 'webserver']
        }
    ]

def parse_wrk_output(output):
    latency_re = re.compile(r"Latency\s*([\.\d\w]*)")
    requests_sec_re = re.compile(r"Requests/sec:\s*([\.\d]*)")
    transfer_sec_re = re.compile(r"Transfer/sec:\s*([\.\d\w]*)")
    return {
        'latency': latency_re.findall(output)[0],
        'requests_sec': requests_sec_re.findall(output)[0],
        'transfer_sec': transfer_sec_re.findall(output)[0]
    }


def execute(cmd):
    p = subprocess.Popen(args=cmd, stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        if line.strip() == 'begin benchmark':
            break

    cmd_str = ' '.join(cmd)
    print 'benchmarking:', cmd_str 
    b = subprocess.Popen(wrk_cmd, stdout=subprocess.PIPE)
    
    output, err = b.communicate()

    if err is not None:
        print 'Error during benchmark run of %s : %s', (err, cmd_str)

    b_status = b.wait()
    p.terminate()
    return parse_wrk_output(output)


if __name__ == '__main__':
    config = load_config()
    for proc in config:
        setup(proc['setup'])
        benchmarks = execute(proc['command'])
        teardown(proc['teardown'])
        print benchmarks

    runs = len(config)
    print 'Completed %s run%s' % (runs, 's' if runs > 1 else '')
