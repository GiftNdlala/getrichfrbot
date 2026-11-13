"""Critical events must survive another stream's stdout suppression."""
import sys


def emit(*items, sep=' ', end='\n', flush=True):
    output = sys.__stdout__ or sys.stdout
    message = sep.join(str(item) for item in items)
    encoding = getattr(output, 'encoding', None)
    if encoding:
        message = message.encode(encoding, errors='replace').decode(encoding)
    print(message, file=output, end=end, flush=flush)
