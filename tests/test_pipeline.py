import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import os
from app.pipeline import Pipeline


def test_pipeline_runs(tmp_path):
    db_file = tmp_path / "test.db"
    pipe = Pipeline(["AAPL"], "2023-01-01", "2023-01-05", str(db_file))
    pipe.run()
    assert db_file.exists()
    assert os.path.getsize(db_file) > 0
