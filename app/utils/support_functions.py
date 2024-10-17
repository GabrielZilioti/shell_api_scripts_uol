import os
import re
import subprocess



def parse_input(input_str):
    pattern = re.compile(r'(\S+)\s+(\S+)\s+(\d+)\s+size\s+(\d+)')
    results = []
    for line in input_str.strip().split('\n'):
        match = pattern.match(line)
        if match:
            results.append({
                "username": match.group(1),
                "folder": match.group(2),
                "numberMessages": int(match.group(3)),
                "size": match.group(4)
            })
    return results if len(results) > 1 else results[0]

def run_shell_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return parse_input(output.decode('utf-8')), error