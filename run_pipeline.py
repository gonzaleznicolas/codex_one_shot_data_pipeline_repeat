import argparse

from app.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(description="Run stock data pipeline")
    parser.add_argument("--symbols", nargs="+", required=True)
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--db", required=True, help="SQLite database path")
    args = parser.parse_args()

    pipe = Pipeline(args.symbols, args.start, args.end, args.db)
    pipe.run()


if __name__ == "__main__":
    main()
