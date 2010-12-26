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

(defparameter *current-game* (make-instance 'tic-tac-toe))

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

(defun main ()
  (loop
     (print-score (score *current-game*))
     (reset-board (board *current-game*))
     (print-board (board *current-game*))
     (take-turns *current-game*)))

(defmethod take-turns ((game tic-tac-toe))
  )
