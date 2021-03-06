"""
The report module contains the definitions for retrieving various reports.
"""
from qds_sdk.qubole import Qubole
from qds_sdk.resource import Resource
import argparse
import json


class ReportCmdLine:
    """
    qds_sdk.ReportCmdLine is the interface used by qds.py.
    """

    @staticmethod
    def parsers():
        argparser = argparse.ArgumentParser(prog="qds.py report",
                description="Report client for Qubole Data Service.")
        subparsers = argparser.add_subparsers(title="report name")

        # For listing the names of all reports
        index = subparsers.add_parser("list",
                description="show names of all available reports")
        index.set_defaults(func=ReportCmdLine.index)

        # Canonical Hive Commands Report
        chc = subparsers.add_parser("canonical_hive_commands",
                description="Show report for canonical hive commands")
        chc.add_argument("--start-date", default=argparse.SUPPRESS,
                help="""The date from which you want the report.  The report
                may contain some data prior to this date also.  api default =
                beginning of time""")
        chc.add_argument("--end-date", default=argparse.SUPPRESS,
                help="""The date till which you want the report.  The report
                may contain some date after this date also.  api default =
                now""")
        chc.add_argument("--offset", type=int, default=argparse.SUPPRESS,
                help="""The starting point of the results.  api default = 0""")
        chc.add_argument("--limit", type=int, default=argparse.SUPPRESS,
                help="""The number of results to fetch.  api default = 10""")
        chc.add_argument("--sort", dest="sort_column",
                default=argparse.SUPPRESS, choices=["frequency", "cpu",
                "fs_bytes_read", "fs_bytes_written"], help="""The column used
                to sort the report. Since this report returns top canonical
                hive commands, the sort order is always descending.  api
                default = frequency""")
        chc.set_defaults(func=ReportCmdLine.canonical_hive_commands)

        # Foo Bar Report
        #fb = subparsers.add_parser("foo_bar",
        #        description="Show report for foo bar")
        #fb.add_argument("--start-date", dest="start_date",
        #        help="""The date from which you want the report.
        #        api default = """)
        #fb.add_argument("--end-date",
        #        help="""The date till which you want the report.
        #        api default = """)
        #fb.add_argument("--offset",
        #        help="""The starting point of the results.
        #        api default = """)
        #fb.add_argument("--limit",
        #        help="""The number of results to fetch.
        #        api default = """)
        #fb.add_argument("--sort-column",
        #        help="""The column used to sort the report.
        #        api default = """)
        #fb.add_argument("--sort-order",
        #        help="""The sorting order used.
        #        api default = """)
        #fb.add_argument("--any-other",
        #        help="""Any other argument specific to this report.
        #        api default = """)
        #fb.set_defaults(func=ReportCmdLine.foo_bar)

        return argparser

    @staticmethod
    def run(args):
        parser = ReportCmdLine.parsers()
        parsed = parser.parse_args(args)
        return parsed.func(parsed)

    @staticmethod
    def index(args):
        result = Report.index()
        return json.dumps(result, indent=4)

    @staticmethod
    def canonical_hive_commands(args):
        data = vars(args)
        data.pop("func")    # We don't want to send this to the api
        result = Report.show("canonical_hive_commands", data)
        return json.dumps(result, indent=4)

    #@staticmethod
    #def foo_bar(args):
    #    data = vars(args)
    #    data.pop("func")    # We don't want to send this to the api
    #    result = Report.show("foo_bar", data)
    #    return json.dumps(result, indent=4)


class Report(Resource):
    """
    qds_sdk.Report is the base Qubole Reports class.
    """

    """all reports use the /reports endpoint"""
    rest_entity_path = "reports"

    @classmethod
    def show(cls, report_name, data):
        """
        Shows a report by issuing a GET request to the /reports/report_name
        endpoint.

        Args:
            `report_name`: the name of the report to show

            `data`: the parameters for the report
        """
        conn = Qubole.agent()
        return conn.get(cls.element_path(report_name), data)

    @classmethod
    def index(cls):
        """
        Shows a list of all available reports by issuing a GET request to the
        /reports endpoint.
        """
        conn = Qubole.agent()
        return conn.get(cls.rest_entity_path)
