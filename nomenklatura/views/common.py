import csv
import itertools
from datetime import datetime
from io import StringIO

from flask import Response


def csv_value(v):
    if v is None:
        return v
    if isinstance(v, datetime):
        return v.isoformat()
    return str(v)


def csvify(iterable, status=200, headers=None):
    lines = filter(lambda r: r is not None, [r.to_row() for r in iterable])
    items, rows = itertools.tee(lines, 2)
    keys = set()
    for row in items:
        keys = keys.union(row.keys())
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow([k for k in keys])
    for row in rows:
        writer.writerow([csv_value(row.get(k, '')) for k in keys])
    return Response(buf.getvalue(), headers=headers, status=status, mimetype='text/csv')


def dataset_filename(dataset, format):
    ts = datetime.utcnow().strftime('%Y%m%d')
    return '%s-%s.%s' % (dataset.name, ts, format)
