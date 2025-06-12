# Windows Setup Instructions

1. Install [Python 3.11](https://www.python.org/downloads/windows/) and make sure it is added to your PATH.
2. Open *Command Prompt* and navigate to the project directory.
3. Create a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
5. Run the unit tests:
   ```cmd
   pytest
   ```
6. Run the data pipeline (example fetching AAPL data):
   ```cmd
   python run_pipeline.py --symbols AAPL --start 2023-01-01 --end 2023-01-10 --db stock_data.db
   ```
7. Inspect the SQLite database using the built in `sqlite3` CLI:
   ```cmd
   sqlite3 stock_data.db
   .tables
   SELECT * FROM prices LIMIT 5;
   .quit
   ```
