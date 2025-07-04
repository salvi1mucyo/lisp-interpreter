(begin

(define (map function input_list)
(if (equal? (length input_list) 0)
()
(append (list (function (car input_list))) (map function (cdr input_list)) )
)
)

(define (filter function input_list)
(if (equal? (length input_list) 0)
()
(if (function (car input_list))
(append (list (car input_list)) (filter function (cdr input_list)))
(filter function (cdr input_list))
)
)
)

(define (reduce function input_list initval)
(if (equal? (length input_list) 0)
initval
(reduce function (cdr input_list) (function initval (car input_list)))
)
)

)
