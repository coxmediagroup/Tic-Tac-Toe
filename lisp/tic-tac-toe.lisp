(defpackage :tic-tac-toe
  (:use :cl))

(in-package :tic-tac-toe)

(defclass board ()
  ((row1 :initform '(" " " " " ")
         :accessor row1)
   (row2 :initform '(" " " " " ")
         :accessor row2)
   (row3 :initform '(" " " " " ")
         :accessor row3)))

(defmethod print-object ((board board) stream)
  "This will ensure that the board object is always printed
with a reasonably nice representation and the options for
future moves will also be displayed."
  (let ((move-count 0))
    (flet ((print-row (row &key moves)
             (if moves
                 (with-output-to-string (result)
                   (loop for place in row do
                        (if (string= " " place)
                            (format result " ~A" (incf move-count))
                            (format result " ~A" place))))
                 (format nil "~{ ~A~}" row))))
    (format stream "[~A ]~%[~A ]~%[~A ]~%"
            (print-row (row1 board))
            (print-row (row2 board))
            (print-row (row3 board)))
    (format stream "~%Your potential moves are:~%")
    (format stream "[~A ]~%[~A ]~%[~A ]~%"
            (print-row (row1 board) :moves t)
            (print-row (row2 board) :moves t)
            (print-row (row3 board) :moves t)))))
