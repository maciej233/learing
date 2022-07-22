import argparse
import textwrap
parser = argparse.ArgumentParser(description="Your personal nc program",
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=textwrap.dedent("""Exaples:
netcat.py -t 192.168.0.1 -p 5555 -l -c          # command shell
netcat.py -t 192.168.0.1 -p 5555 -u file.txt    # upload to file ./file.txt
netcat.py -t 192.168.0.1 -l  ...
"""))
a= parser.add_argument=()

print(dir(a))