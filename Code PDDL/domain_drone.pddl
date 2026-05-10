;Domain
(define (domain drone)
  (:requirements
    :strips
    :numeric-fluents
    :typing :disjunctive-preconditions
    :equality
    :existential-preconditions)

  (:types
    drone order position - object
  )

  (:predicates
    (at ?obj - object ?p - position) ;pos droni/ordini
    (connected ?p1 ?p2 - position) ;connessioni tra celle
    (is-restaurant ?p - position) ;punto di carico degli ordini
    (delivered ?ord - order) ;ordine consegnato
    (carrying ?d - drone ?ord - order) ;stato drone
    (destination ?ord - order ?p - position) ;destinazione ordine
    (is-recharge-station ?p - position) ;stazioni di ricarica
  )

  (:functions
    (count-order ?d - drone)
    (max-order ?d - drone)
    (battery-level ?d - drone)
    (total-cost)
  )

  
  ; MOVE | SPOSTA IL DRONE TRA DUE CELLE
  (:action move
    :parameters (?d - drone ?from - position ?to - position)
    :precondition (and
      (at ?d ?from)
      (connected ?from ?to)
      (>= (battery-level ?d) 5)
      
      ; LOGICA DI COLLISIONE
      (or
        (is-restaurant ?to)
        (not (exists (?d2 - drone)
            (and (not (= ?d ?d2)) (at ?d2 ?to))
          ))
      )
    )
    :effect (and
      (not (at ?d ?from))
      (at ?d ?to)
      (decrease (battery-level ?d) 5)
      (increase (total-cost) 10)
    )
  )

  
  ;LOAD-ORDER | CARICA UN ORDINE SUL DRONE
  (:action load-order
    :parameters (?ord - order ?d - drone ?p - position)
    :precondition (and
      (at ?d ?p)
      (at ?ord ?p)
      (is-restaurant ?p)
      (< (count-order ?d) (max-order ?d))
    )
    :effect (and
      (not (at ?ord ?p))
      (carrying ?d ?ord)
      (increase (count-order ?d) 1)
      (increase (total-cost) 2)
    )
  )

  
  ;DELIVERY-ORDER | CONSEGNA ORDINE
  (:action delivery-order
    :parameters (?ord - order ?d - drone ?p - position)
    :precondition (and
      (at ?d ?p)
      (destination ?ord ?p)
      (carrying ?d ?ord)
    )
    :effect (and
      (not (carrying ?d ?ord))
      (delivered ?ord)
      (at ?ord ?p)
      (decrease (count-order ?d) 1)
      (increase (total-cost) 2)
    )
  )

  
  ;RECHARGE | CARICA DRONE
  (:action recharge
    :parameters (?d - drone ?p - position)
    :precondition (and
      (at ?d ?p)
      (or (is-restaurant ?p) (is-recharge-station ?p))
      ;(< (battery-level ?d) 30) 
    )
    :effect (and
      (assign (battery-level ?d) 100)
      (increase (total-cost) 50)
    )
  )
)