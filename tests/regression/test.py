import subprocess
import sys
import time


def main():
    start = time.time()
    results = []
    rule = sys.argv[1]
    paths = sys.argv[2:]

    for path in paths:
        sys.stdout.write('\033[0m')
        sys.stdout.write(path[:-1] + ' ... ')
        sys.stdout.flush()
        result = make(path, rule)
        make(path, 'clean')
        results.append(result)
        sys.stdout.write('\033[1m\033[')
        sys.stdout.write('32m[OK]\n' if result[0] == 0 else '31m[FAILED]\n')
        sys.stdout.flush()

    sys.stdout.write('\n')

    elapsed = time.time() - start
    return summarize(results, elapsed)


def make(path, rule):
    proc = subprocess.Popen(
        ['make', '-C', path, rule],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    errcode = proc.wait()
    return (errcode, stdout, stderr, path, rule)


def summarize(results, elapsed):
    failed = 0
    for errcode, stdout, stderr, path, rule in results:
        if errcode == 0:
            continue
        failed += 1
        print("======================================================================")
        print("ERROR: %s %s" % (path, rule))
        if stdout:
            print("- stdout -------------------------------------------------------------")
            print(stdout)
        if stderr:
            print("- stderr -------------------------------------------------------------")
            print(stderr)
            print("----------------------------------------------------------------------")
    print("Finished in %.3fs" % elapsed)
    print("%s tests, %s errors" % (len(results), failed))

    return 0 if not failed else 1


if __name__ == '__main__':
    ret = main()
    sys.stdout.write('\033[0m\n')
    sys.stdout.flush()
    sys.exit(ret)
