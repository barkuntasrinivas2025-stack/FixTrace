import argparse

from app.main import diagnose_port, run


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fixtrace",
        description="Deterministic failure diagnosis with controlled AI explanations",
    )

    subparsers = parser.add_subparsers(dest="command")

    log_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a log file",
    )
    log_parser.add_argument(
        "log_file",
        help="Path to the diagnostic log file",
    )

    port_parser = subparsers.add_parser(
        "diagnose-port",
        help="Diagnose TCP port reachability",
    )
    port_parser.add_argument("host")
    port_parser.add_argument("port", type=int)

    args = parser.parse_args()

    if args.command == "analyze":
        print(run(args.log_file))
        return

    if args.command == "diagnose-port":
        analysis = diagnose_port(args.host, args.port)

        print(f"FAILURE: {analysis.classification}")
        print(f"CONFIDENCE: {analysis.confidence}")
        print(f"HYPOTHESIS: {analysis.hypothesis}")

        return

    parser.print_help()


if __name__ == "__main__":
    main()
