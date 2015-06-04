#!/usr/bin/env python


"""
Core components for gpsdio_filtersplit
"""


import click
import gpsdio
import gpsdio.schema
import datetime
import hashlib
import datetime


@click.command(name='filtersplit')
@click.argument("infile", metavar="INFILENAME")
@click.argument("outfile", metavar="OUTFILENAME", default='%(split)s.msg')
@click.option(
    '-c', '--change', 'change_exprs', metavar='COL=EXPR',
    multiple=True,
    help="Add/change column named COL to the value of EXPR for each row",
)
@click.option(
    '-s', '--split', metavar='COL1,COL2,...', default="mmsi",
    help="Columns to split by.",
)
@click.option(
    '-b', '--buckets', metavar='BUCKETS', type=click.INT, default=None,
    help="Split to this many buckets, using a hash of the split columns to select bucket."
)
@click.option(
    '-f', '--filter', 'filter_expr', metavar='EXPR', default=None,
    help="Filter rows by expression",
)
@click.option(
    '-F', '--filter-env', 'filter_env_expr', metavar='STATEMENTS', default=None,
    help="Environment for filter expressions (anything defined in this python code is available to the filters)",
)
@click.option(
    '-t', '--timeresolution', metavar='EXPR', default='%Y-%m-%d',
    help="When splitting by a time column, use this expression to print timestamps to the filename. Example: %Y-%m-%d",
)
@click.pass_context
def gpsdio_filtersplit(ctx, infile, outfile, split, buckets, filter_expr, timeresolution, filter_env_expr, change_exprs):

    """
    Filter by expression and split by field. Filter expressions are passed to
    `eval()` and must be valid Python code. Column names are available as
    as variables and types are maintained.

    Examples:

        Speed range
        --filter '0.5 < speed < 10.0'

        Specific MMSI's
        --filter "mmsi in ['123456789', '987654321']"

        Bounding box
        --filter "20 <= lon <= 30 and -10 <= lat <= 30"

        Splitting into 4 buckets of mmsi:s for parallellization of further processing:
        --split "mmsi" --buckets 4

        Using external functions to evaluate rows
        --filter "fishing_score(lat, lon, speed, course) > 0.5" --filter-env scoring_functions.py

        Using a change expression to split by a lat/lon grid:

        --change "latgrid=round(row.get('lat',0)/10)*10" --change "longrid=round(row.get('lon',0)/10)*10" --split "latgrid,longrid"

    """

    change_exprs = {key: value
                    for key, value
                    in (item.split("=")
                        for item in change_exprs)}
    
    split = split.split(",")
    
    filter_env = {}
    if filter_env_expr:
        exec filter_env_expr in filter_env, filter_env

    if split is None:
        split = ["mmsi"]

    def getKey(row, key):
        value = row[key]
        if isinstance(value, datetime.datetime):
            return value.strftime(timeresolution)
        else:
            return value

    bucketinfo = {}

    splitkey = ''
    with gpsdio.open(infile,
                     driver=ctx.obj['i_drv'], do=ctx.obj['i_drv_opts'],
                     compression=ctx.obj['i_cmp'], co=ctx.obj['i_cmp_opts']) as f:
        for row in f:
            env_vars = dict(filter_env)
            env_vars.update(row)
            env_vars['row'] = env_vars

            for key, expr in change_exprs.iteritems():
                env_vars[key] = row[key] = eval(expr, env_vars)

            if filter_expr is not None:
                if not eval(filter_expr, env_vars):
                    continue

            try:
                splitkey = ','.join('%s=%s' % (key, getKey(row, key)) for key in split)
            except KeyError:
                pass
            else:
                if buckets is not None:
                    bucket = str(int(hashlib.sha224(splitkey).hexdigest(), 16) % buckets)
                    bucketinfo[splitkey] = bucket
                    splitkey = "bucket=%s" % (bucket,)

            with gpsdio.open(outfile % {'split': splitkey}, "a",
                             driver=ctx.obj['o_drv'], do=ctx.obj['o_drv_opts'],
                             compression=ctx.obj['o_cmp'], co=ctx.obj['o_cmp_opts']) as f:
                f.writerow(row)

    if buckets is not None:
        with gpsdio.open(outfile % {'split': 'bucketlist'}, "a",
                         driver=ctx.obj['o_drv'], do=ctx.obj['o_drv_opts'],
                         compression=ctx.obj['o_cmp'], co=ctx.obj['o_cmp_opts']) as f:
            for splitkey, bucket in bucketinfo.iteritems():
                f.writerow({'type': -1, 'splitkey': splitkey, 'bucket': bucket})




if __name__ == '__main__':
    gpsdio_filtersplit()
