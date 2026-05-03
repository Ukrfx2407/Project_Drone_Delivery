; PDDL sample: simple numeric counter
(define (domain drone)
  (:requirements :strips :numeric-fluents :typing :disjunctive-preconditions)
  
  (:types 
    drone order position - object
  )

  (:predicates 
    (at ?obj - object ?p - position)
    (connected ?p1 ?p2 - position)
    (is-restaurant ?p - position) 
    (delivered ?ord - order)
    (carrying ?d - drone ?ord - order)
    (destination ?ord - order ?p - position)
    (is-recharge-station ?p - position)
  )

  (:functions 
    (count-order ?d - drone) 
    (max-order ?d - drone) 
    (battery-level ?d - drone)
    (total-cost)
  )

  (:action move
    :parameters (?d - drone ?from - position ?to - position)
    :precondition (and (at ?d ?from) (or (> (count-order ?d) 0) (not (is-restaurant ?from))) (connected ?from ?to) (>= (battery-level ?d) 5))
    :effect (and (not (at ?d ?from)) (increase (total-cost) 100) (at ?d ?to) (decrease (battery-level ?d) 5))
  )

  
  (:action load-order
    :parameters (?ord - order ?d - drone ?p - position)
    :precondition (and (at ?d ?p) (at ?ord ?p) (is-restaurant ?p) (< (count-order ?d) (max-order ?d)))
    :effect (and (increase (count-order ?d) 1) (carrying ?d ?ord) (increase (total-cost) 1) (not (at ?ord ?p)))
  )

  
  (:action delivery-order
    :parameters (?ord - order ?d - drone ?p - position)
    :precondition (and (at ?d ?p) (destination ?ord ?p) (carrying ?d ?ord))
    :effect (and (decrease (count-order ?d) 1) (delivered ?ord) (not (carrying ?d ?ord)) (increase (total-cost) 1) (at ?ord ?p) )
  )
  
  
   (:action recharge
    :parameters (?d - drone ?p - position)
    :precondition (and (at ?d ?p) (or (is-restaurant ?p) (is-recharge-station ?p)) (< (battery-level ?d) 100))
    :effect (and (increase (total-cost) 1) (assign (battery-level ?d) 100) ))
 
)