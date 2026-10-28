""" Flask app for Tic Tac Toe game """
from flask import Flask, render_template, redirect, url_for
from Gameboard import Gameboard

app = Flask(__name__)

gameboard = Gameboard()
state = {"player": "X", "message": "", "winner": None, "line": None}


def find_winning_line():
    """Return the winning combination (list of cells) or None."""
    b = gameboard.board
    for combo in Gameboard.winning_combinations:
        if b[combo[0]] == b[combo[1]] == b[combo[2]]:
            return combo
    return None


@app.route('/')
def index():
    """Render the main page of the Tic Tac Toe game."""
    line = state["line"]
    coords = None
    if line:
        # Cell centers in a 300x300 grid (100px per cell)
        def center(n):
            return ((n - 1) % 3 * 100 + 50, (n - 1) // 3 * 100 + 50)
        (x1, y1), (x2, y2) = center(line[0]), center(line[2])
        # Extend the line slightly beyond the end cells
        dx, dy = (x2 - x1) * 0.3, (y2 - y1) * 0.3
        coords = (x1 - dx, y1 - dy, x2 + dx, y2 + dy)
    return render_template('index.html', board=gameboard.board,
                           player=state["player"], message=state["message"],
                           winner=state["winner"], line=coords)


@app.route('/move/<int:position>')
def move(position):
    """Register the click on a cell and update the game state."""
    if state["winner"] or position not in range(1, 10):
        return redirect(url_for('index'))
    player = state["player"]
    state["message"] = gameboard.player_move(player, position)
    if "Invalid" in state["message"]:
        return redirect(url_for('index'))
    result = gameboard.check_winner()
    if result == "-":
        state.update(winner="-", message="It's a draw!")
    elif result:
        state.update(winner=result, line=find_winning_line(),
                     message=f"Player {result} wins!")
    else:
        state["player"] = "O" if player == "X" else "X"
    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    """Start a new game."""
    gameboard.reset_board()
    state.update(player="X", message="", winner=None, line=None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
