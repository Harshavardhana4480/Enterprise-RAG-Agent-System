from pathlib import Path


def test_documents_exist():

    raw_dir = Path("data/raw")

    files = list(raw_dir.iterdir())

    assert len(files) > 0

    for file in files:

        assert file.exists()
        assert file.is_file()