import argparse
import io
import re
import subprocess
import sys
import pytest
from pathlib import Path

from connect4 import Connect4, main


@pytest.mark.parametrize("stdin, column", [("1", 0), ("dummy\n2", 1), ("-1\n3", 2)])
def test_choose_player_column(
    monkeypatch: pytest.MonkeyPatch, stdin: str, column: int
) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
    assert Connect4().choose_player_column(1) == column


def test_place_piece():
    c4 = Connect4()
    for _ in range(6):
        assert c4.place_piece(1, 1) is True
    # because we've run out of space
    assert c4.place_piece(1, 1) is False


def test_print_grid(capsys: pytest.CaptureFixture[str]):
    c4 = Connect4()

    c4.print_grid()
    output = capsys.readouterr()
    assert output.err == ""
    assert output.out == ".......\n.......\n.......\n.......\n.......\n.......\n"

    c4.place_piece(1, 1)
    c4.place_piece(2, 4)
    c4.print_grid()
    output = capsys.readouterr()
    assert output.err == ""
    assert output.out == ".......\n.......\n.......\n.......\n.......\n.1..2..\n"


def test_has_won():
    c4 = Connect4()
    for _ in range(4):
        assert c4.has_won() is None
        assert c4.place_piece(1, 1) is True
    assert c4.has_won() == 1


def test_play(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    monkeypatch.setattr("sys.stdin", io.StringIO("1\n2\n" * 4))
    assert Connect4().play() == 1

    output = capsys.readouterr()
    assert output.err == ""
    assert output.out.endswith("Player 1 won!\n")


def test_play_full_column(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    # First, fill up the 1st column to check that path
    # Then fill 2 and 3 alternately so player 1 wins
    input = ("1\n" * 7) + ("2\n3\n" * 4)
    monkeypatch.setattr("sys.stdin", io.StringIO(input))
    assert Connect4().play() == 1

    output = capsys.readouterr()
    assert output.err == ""
    assert output.out.endswith("Player 1 won!\n")


def test_help():
    res = subprocess.run(
        [sys.executable, Path(__file__).parent.joinpath("connect4.py"), "--help"],
        capture_output=True,
        encoding="utf8",
    )
    assert res.returncode == 0
    assert res.stderr == ""
    assert "Connect 4" in res.stdout
    assert (
        re.search(r"-h, --help\s+show this help message and exit", res.stdout)
        is not None
    )


def test_main(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    with pytest.raises(EOFError):
        main([])


@pytest.mark.parametrize(
    "arg", ["--players=0", "--rows=-1", "--columns=-1", "--winning-count=0"]
)
def test_bad_args(arg: str):
    with pytest.raises(argparse.ArgumentError):
        main([arg])


def test_play_draw(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    # Fill up each column alternating
    # This only works to force a draw because we're running with 4 players
    # With 2 or 3 they'd fill in the same row and Player 1 would win on column 4
    input = ""
    for column in range(7):
        input += f"{column+1}\n" * 6
    input += "1\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(input))
    assert Connect4(players=4).play() == -1

    output = capsys.readouterr()
    assert output.err == ""
    assert output.out.endswith("Draw!\n")
