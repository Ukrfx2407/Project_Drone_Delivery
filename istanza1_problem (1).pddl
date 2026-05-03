; Istanza 1
(define (problem drone_1)
  (:domain drone)
  (:objects 
    drone1 - drone
    ord1 ord2 ord3 - order
    p00 p01 p02 p03 p04
    p10 p11 p12 p13 p14
    p20 p21 p22 p23 p24
    p30 p31 p32 p33 p34
    p40 p41 p42 p43 p44 - position
  )
  
  
  (:init
    ;; INIZIALIZZAZIONE POSIZIONE
    (at drone1 p00) (is-restaurant p00) 
    
    (at ord1 p00) (destination ord1 p44)

    
    ;; SETTING VARIABILI (batteria a 100, ordine 0, maxorder 1)
    (= (battery-level drone1) 100) (= (count-order drone1) 0) (= (max-order drone1) 3) (= (total-cost) 0)

    ;; CONNESSIONI ORIZZONTALI GRIGLIA
    (connected p00 p01) (connected p01 p00) (connected p01 p02) (connected p02 p01) (connected p02 p03) (connected p03 p02) (connected p03 p04) (connected p04 p03)
    (connected p10 p11) (connected p11 p10) (connected p11 p12) (connected p12 p11) (connected p12 p13) (connected p13 p12) (connected p13 p14) (connected p14 p13)
    (connected p20 p21) (connected p21 p20) (connected p21 p22) (connected p22 p21) (connected p22 p23) (connected p23 p22) (connected p23 p24) (connected p24 p23)
    (connected p30 p31) (connected p31 p30) (connected p31 p32) (connected p32 p31) (connected p32 p33) (connected p33 p32) (connected p33 p34) (connected p34 p33)
    (connected p40 p41) (connected p41 p40) (connected p41 p42) (connected p42 p41) (connected p42 p43) (connected p43 p42) (connected p43 p44) (connected p44 p43)
    
    ;; CONNESSIONI VERTICALI GRIGLIA
    (connected p00 p10) (connected p10 p00) (connected p10 p20) (connected p20 p10) (connected p20 p30) (connected p30 p20) (connected p30 p40) (connected p40 p30)
    (connected p01 p11) (connected p11 p01) (connected p11 p21) (connected p21 p11) (connected p21 p31) (connected p31 p21) (connected p31 p41) (connected p41 p31)
    (connected p02 p12) (connected p12 p02) (connected p12 p22) (connected p22 p12) (connected p22 p32) (connected p32 p22) (connected p32 p42) (connected p42 p32)
    (connected p03 p13) (connected p13 p03) (connected p13 p23) (connected p23 p13) (connected p23 p33) (connected p33 p23) (connected p33 p43) (connected p43 p33)
    (connected p04 p14) (connected p14 p04) (connected p14 p24) (connected p24 p14) (connected p24 p34) (connected p34 p24) (connected p34 p44) (connected p44 p34)
  )
  
  
(:goal (and 
      (delivered ord1) 
    
    )
  )

  (:metric minimize (total-cost))
)