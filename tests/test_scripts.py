"""
Test student-created utility scripts.

EECS 485 Project 3

Andrew DeOrio <awdeorio@umich.edu>
"""
import subprocess
from pathlib import Path
import sqlite3


def test_executables():
    """Verify disaster_reliefrun, disaster_relieftest, disaster_reliefdb are executables."""
    assert_is_shell_script("bin/disaster_reliefrun")
    assert_is_shell_script("bin/disaster_relieftest")
    assert_is_shell_script("bin/disaster_reliefdb")
    assert_is_shell_script("bin/disaster_reliefinstall")


def test_disaster_reliefinstall():
    """Verify disaster_relieftest contains the right commands."""
    disaster_relieftest_content = Path("bin/disaster_reliefinstall")\
        .read_text(encoding='utf-8')
    assert "python3 -m venv" in disaster_relieftest_content
    assert "source env/bin/activate" in disaster_relieftest_content
    assert "pip install -r requirements.txt" in disaster_relieftest_content
    assert "pip install -e ." in disaster_relieftest_content
    assert "npm ci ." in disaster_relieftest_content


def test_disaster_reliefdb_random():
    """Verify disaster_reliefdb reset does a destroy and a create."""
    # Clean up
    db_path = Path("var/disaster_relief.sqlite3")
    if db_path.exists():
        db_path.unlink()

    # Run "disaster_reliefdb reset && disaster_reliefdb random"
    subprocess.run(["bin/disaster_reliefdb", "reset"], check=True)
    subprocess.run(["bin/disaster_reliefdb", "random"], check=True)

    # Connect to the database
    connection = sqlite3.connect("var/disaster_relief.sqlite3")
    connection.execute("PRAGMA foreign_keys = ON")

    # Get the number of posts from the database
    cur = connection.execute("SELECT count(*) FROM posts")
    num_rows = cur.fetchone()[0]
    assert num_rows > 100


def assert_is_shell_script(path):
    """Assert path is an executable shell script."""
    path = Path(path)
    assert path.exists()
    output = subprocess.run(
        ["file", path],
        check=True, stdout=subprocess.PIPE, universal_newlines=True,
    ).stdout
    assert "shell script" in output
    assert "executable" in output
