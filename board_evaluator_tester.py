import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from board_evaluator import detect_win, detect_cat

def test_horizontal_win():
    assert 1 == detect_win([
        [0,0,0],
        [1,1,1],
        [0,2,2],
    ])
    assert 2 == detect_win([
        [0,0,0],
        [0,1,1],
        [2,2,2],
    ])
    assert 1 == detect_win([
        [0,0,0],
        [1,1,1],
        [2,2,0],
    ])
    assert 2 == detect_win([
        [0,0,0],
        [1,1,0],
        [2,2,2],
    ])

def test_vertical_win():
    assert 1 == detect_win([
        [0,1,0],
        [0,1,2],
        [0,1,2],
    ])
    assert 2 == detect_win([
        [0,0,2],
        [0,1,2],
        [0,1,2],
    ])
    assert 1 == detect_win([
        [0,1,2],
        [0,1,2],
        [0,1,0],
    ])
    assert 2 == detect_win([
        [0,1,2],
        [0,1,2],
        [0,2,2],
    ])

def test_diagonal_win():
    assert 1 == detect_win([
        [1,0,2],
        [0,1,2],
        [0,0,1],
    ])
    assert 2 == detect_win([
        [2,1,0],
        [0,2,1],
        [0,0,2],
    ])
    assert 1 == detect_win([
        [2,2,1],
        [0,1,0],
        [1,0,0],
    ])
    assert 2 == detect_win([
        [0,1,2],
        [1,2,0],
        [2,0,0],
    ])

def test_no_win():
    assert 0 == detect_win([
        [1,0,2],
        [0,2,2],
        [0,0,1],
    ])
    assert 0 == detect_win([
        [1,1,0],
        [0,2,1],
        [2,1,2],
    ])
    assert 0 == detect_win([
        [2,2,1],
        [0,2,0],
        [1,0,0],
    ])
    assert 0 == detect_win([
        [0,1,2],
        [1,2,0],
        [1,0,0],
    ])
