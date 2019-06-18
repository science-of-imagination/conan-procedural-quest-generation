(define (domain vincentland)
    (:requirements :action-costs)
    (:predicates
        (location ?l)
        (item ?i)
        (information ?info)
        (character ?c)
        (defended ?c)
        (sneaky ?c)
        (has ?cl ?i)
        (at ?c ?l)
        (player ?p)
        (cooperative ?c)
        (wants ?c ?i)
        (dead ?c)
        (weapon ?w)
        (adjacent ?la ?lb)
        (monster ?m)
        (captive ?captor ?captive)
        (damaged ?i)
        (experimented ?i)
        (explored ?l)
        (used ?i))

    (:functions
        (total-cost))

    (:action capture
        :parameters (?p ?char ?loc)
        :precondition (and (player ?p) (character ?char) (location ?loc) (at ?p ?loc) (at ?char ?loc))
        :effect (and (captive ?p ?char) (increase (total-cost) 2)))

    (:action damage
        :parameters (?p ?i ?loc ?w)
        :precondition (and (player ?p) (item ?i) (location ?loc) (weapon ?w) (or (and (at ?p ?loc) (has ?loc ?i)) (has ?p ?i)) (has ?p ?w))
        :effect (and (damaged ?i) (increase (total-cost) 2)))

    (:action defend
        :parameters (?p ?todefend ?loc)
        :precondition (and (player ?p) (or (character ?todefend) (item ?todefend)) (location ?loc) (at ?p ?loc) (or (at ?todefend ?loc) (has ?loc ?todefend)))
        :effect (and (defended ?todefend) (increase (total-cost) 2)))

    (:action escort
        :parameters (?p ?charA ?locA ?locB)
        :precondition (and (player ?p) (character ?charA) (location ?locA) (location ?locB) (at ?p ?locA) (at ?charA ?locA) (cooperative ?charA))
        :effect (and (at ?p ?locB) (at ?charA ?locB) (not (at ?p ?locA)) (not (at ?charA ?locA)) (increase (total-cost) 4)))

    (:action exchange
        :parameters (?p ?char ?i2 ?i1 ?loc)
        :precondition (and (player ?p) (character ?char) (item ?i1) (item ?i2) (location ?loc) (has ?p ?i1) (has ?char ?i2) (at ?p ?loc) (at ?char ?loc))
        :effect (and (not (has ?p ?i1)) (has ?p ?i2) (not (has ?char ?i2)) (has ?char ?i1) (increase (total-cost) 1)))

    (:action experiment
        :parameters (?p ?i)
        :precondition (and (player ?p) (item ?i) (has ?p ?i))
        :effect (and (experimented ?i) (increase (total-cost) 2)))

    (:action explore
        :parameters (?p ?locA ?locB)
        :precondition (and (player ?p) (location ?locA) (location ?locB) (at ?p ?locA))
        :effect (and (explored ?locB) (not (at ?p ?locA)) (at ?p ?locB) (increase (total-cost) 3)))

    (:action getfromlocation
        :parameters (?p ?loc ?i)
        :precondition (and (player ?p) (location ?loc) (item ?i) (has ?loc ?i) (at ?p ?loc))
        :effect (and (has ?p ?i) (not (has ?loc ?i)) (increase (total-cost) 2)))

    (:action giveto
        :parameters (?p ?charB ?i ?loc)
        :precondition (and (character ?charB) (player ?p) (item ?i) (has ?p ?i) (location ?loc) (at ?charB ?loc) (at ?p ?loc))
        :effect (and (has ?charB ?i) (not (has ?p ?i)) (cooperative ?charB) (increase (total-cost) 2)))

    (:action move
        :parameters (?p ?to ?from)
        :precondition (and (location ?to) (location ?from) (player ?p) (at ?p ?from))
        :effect (and (at ?p ?to) (not (at ?p ?from)) (increase (total-cost) 2)))

    (:action kill
        :parameters (?p ?charA ?i ?loc ?w)
        :precondition (and (not (damaged ?w)) (player ?p) (or (character ?charA) (monster ?charA)) (at ?charA ?loc) (at ?p ?loc) (item ?i) (location ?loc) (has ?charA ?i) (weapon ?w) (has ?p ?w))
        :effect (and (not (character ?charA)) (has ?loc ?i) (dead ?charA) (item ?charA) (increase (total-cost) 3)))

    (:action listen
        :parameters (?p ?char ?loc ?info)
        :precondition (and (player ?p) (character ?char) (location ?loc) (at ?p ?loc) (at ?char ?loc) (information ?info) (has ?char ?info))
        :effect (and (has ?p ?info) (increase (total-cost) 2)))

    (:action read
        :parameters (?p ?loc ?i ?info)
        :precondition (and (player ?p) (item ?i) (information ?info) (location ?loc) (at ?p ?loc) (has ?loc ?i) (has ?i ?info))
        :effect (and (has ?p ?info) (increase (total-cost) 2)))

    (:action repair
        :parameters (?p ?loc ?i)
        :precondition (and (player ?p) (location ?loc) (item ?i) (damaged ?i) (or (and (at ?p ?loc) (has ?loc ?i))) (has ?p ?i))
        :effect (and (not (damaged ?i)) (increase (total-cost) 2)))


    (:action report
        :parameters (?p ?char ?info ?loc)
        :precondition (and (player ?p) (location ?loc) (character ?char) (information ?info) (at ?p ?loc) (at ?char ?loc) (has ?p ?info))
        :effect (and (has ?char ?info) (increase (total-cost) 2)))


    (:action spy
        :parameters (?p ?char ?loc ?info)
        :precondition (and (player ?p) (character ?char) (location ?loc) (at ?p ?loc) (at ?char ?loc) (sneaky ?p) (information ?info) (has ?char ?info))
        :effect (and (has ?p ?info) (increase (total-cost) 2)))


    (:action stealth
        :parameters (?p)
        :precondition (player ?p)
        :effect (and (sneaky ?p) (increase (total-cost) 2)))


    (:action take
        :parameters (?p ?char ?i2 ?loc)
        :precondition (and (player ?p) (or (character ?char) (monster ?char)) (item ?i2) (location ?loc) (has ?char ?i2) (at ?p ?loc) (at ?char ?loc) (or (cooperative ?char) (sneaky ?p)))
        :effect (and (has ?p ?i2) (not (has ?char ?i2)) (increase (total-cost) 2)))

    (:action use
        :parameters (?p ?i)
        :precondition (and (player ?p) (item ?i) (has ?p ?i))
        :effect (and (used ?i) (increase (total-cost) 1)))

)