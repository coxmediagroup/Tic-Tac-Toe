; We probably won't do this as I think it's Linux only...double check before shipping.
; #!/usr/bin/sbcl --script

; Who wants to run a script and see compiler style notes?
(declaim (sb-ext:muffle-conditions style-warning))

(defpackage :tic-tac-toe
  (:use :cl))

(in-package :tic-tac-toe)

(defclass tic-tac-toe ()
  ((score-human :initform 0
                :accessor score-human)
   (score-ai :initform 0
             :accessor score-ai)
   (board :initform (make-array '(3 3) :initial-element " ")
          :accessor board)))

(defparameter *current-game* (make-instance 'tic-tac-toe)
  "A global variable holding all our lovely game state.")

(defparameter *win-conditions* '((0 1 2)
                                 (3 4 5)
                                 (6 7 8)
                                 (0 3 6)
                                 (1 4 7)
                                 (2 5 8)
                                 (0 4 8)
                                 (2 4 6))
  "This is an enumeration of all win conditions.
Specifically, A list of lists each specifying a row
of three Xs or Os constituting a win.")

(defmethod print-board ((game tic-tac-toe) &key moves)
  "Print each row of the board inside square brackets.
If moves is T, blank spaces (i.e. available moves) will
be numbered starting from 1."
  (let ((move-count 0)
        (board (board game)))
    (flet ((print-row (row-num &key moves)
             (with-output-to-string (result)
               (loop for i in '(0 1 2) do
                    (if (and moves
                             (string= (aref board row-num i) " "))
                        (format result " ~A" (incf move-count))
                        (format result " ~A" (aref board row-num i)))))))
      (when moves
        (format t "Your potential moves are:~%"))
      (format t "[~A ]~%[~A ]~%[~A ]~%"
              (print-row 0 :moves moves)
              (print-row 1 :moves moves)
              (print-row 2 :moves moves)))))

(defmethod print-score ((game tic-tac-toe))
  "Print the score of the computer and player in GAME."
  (format t "The score is... Scary Robots: ~A   Puny Humans: ~A~%"
          (score-ai game) (score-human game)))

(defmethod reset-board ((game tic-tac-toe))
  "Reset the board for a new game."
  (setf (board game) (make-array '(3 3) :initial-element " ")))

(defun print-help ()
  "Instructions for playing Tic-Tac-Toe."
  (format t "~%Welcome to the glorious world of Tic-Tac-Toe.
If you've never tic'd or tac'd before the rules are simple:
There is a 3 by 3 game board and each player takes turns
filling the 9 empty spaces with their sign, an X or an O.
Whoever gets 3 in a row (vertical, horizontal or diagonal)
first wins! Lectures on Game Trees and Combinatorics
will follow with milk and cookies.~%~%"))

(defun main ()
  "Print the instructions for playing Tic-Tac-Toe.
Afterwards, continually prompt the player to play and
start a new game each time they respond affirmatively."
  (print-help)
  (flet ((new-game? ()
           (reset-board *current-game*)
           (format t "This is the board with the potential moves numbered...~%")
           (print-board *current-game* :moves t)
           (yes-or-no-p "Would you like to play Tic-Tac-Toe?")))
    (loop until (not (new-game?)) do
         (take-turns *current-game*)
         (print-score *current-game*)))
  (format t "~%Thanks for playing!~%~%")
  (sb-ext:quit))

(defmethod take-turns ((game tic-tac-toe))
  "Ask the human if they would like to go first. Then loop back and forth
between the two players until the game is over."
  (let ((first-turn-p (yes-or-no-p "Would you like to go first?"))
        )
    (catch 'game-over
      (loop
         (take-turn game first-turn-p)
         (take-turn game (not first-turn-p))))))

(defmethod take-turn ((game tic-tac-toe) human-p)
  "If it's the computers turn, it selects a move.
Otherwise, print the options for the player and get
their selection, then move"
  (if human-p
      (select-move game :human)
      (select-move game))
  (when (game-over-p game human-p)
    (throw 'game-over nil)))

(defmethod game-over-p ((game tic-tac-toe) human-p)
  "Check the game board to see if a winner has emerged by first
iterating through the known *win-conditions* and then seeing
if the board is full. Return nil if the game isn't over,
otherwise change the score appropriately and inform the user."
  (let ((board (board game))
        (xs-and-os (if human-p '(:human :ai) '(:ai :human))))
    (loop for condition in *win-conditions* do
         (cond ((three-in-a-row "X" condition board)
                (display-results (first xs-and-os) game)
                (return t))
               ((three-in-a-row "O" condition board)
                (display-results (second xs-and-os) game)
                (return t))
               ((full-board-p)
                (display-results :draw game)
                (return t))
               (t (return nil))))))

(defun display-results (winner game)
  (ecase winner
    (:human
     (incf (score-human game))
     (format t "The human wins!~%"))
    (:ai
     (incf (score-ai game))
     (format t "The AI wins!~%"))
    (:draw
     (format t "No winner!~%"))))

(defun three-in-a-row (condition board letter)
  (loop for index in condition
        always (string= letter (row-major-aref board index))))

(defun full-board-p (board)
  (loop for index from 0 upto 8
        never (string= " " (row-major-aref board index))))

(defmethod select-move ((game tic-tac-toe) &optional human-p)
  )

;(main)
