(define (domain vincentland)
	(:predicates
		(location ?l)
		(item ?i)
		(character ?c)
		(has ?cl ?i)
		(at ?c ?l)
		(player ?p)
        (cooperative ?c)
        (wants ?c ?i)
        (dead ?c)
        (weapon ?w)
        (adjacent ?la ?lb))

	(:action move
		:parameters  (?p ?to ?from)
		:precondition (and (location ?to) (location ?from) (player ?p) (at ?p ?from))
		:effect (and (at ?p ?to) (not (at ?p ?from))))

	(:action getfromlocation
   		:parameters (?p ?i ?loc)
   		:precondition (and (item ?i) (player ?p) (location ?loc) (has ?loc ?i) (at ?p ?loc))
   		:effect (has ?p ?i))

   	(:action given
   		:parameters (?charA ?p ?i ?loc)
   		:precondition (and (character ?charA) (player ?p) (item ?i) (has ?charA ?i) (location ?loc) (at ?charA ?loc) (at ?p ?loc) (cooperative ?charA))
   		:effect (and (has ?p ?i) (not (has ?charA ?i))))

   	(:action giveto
   		:parameters (?p ?charB ?i ?loc)
   		:precondition (and (character ?charB) (player ?p) (item ?i) (has ?p ?i) (location ?loc) (at ?charB ?loc) (at ?p ?loc))
   		:effect (and (has ?charB ?i) (not (has ?p ?i)) (cooperative ?charB)))

    (:action kill
        :parameters (?p ?charA ?i ?loc ?w)
        :precondition (and (player ?p) (character ?charA) (at ?charA ?loc) (at ?p ?loc) (item ?i) (location ?loc) (has ?charA ?i) (weapon ?w) (has ?p ?w))
        :effect (and (not (character ?charA)) (has ?loc ?i) (dead ?charA) (item ?charA)))

    (:action escort
        :parameters (?p ?charA ?locA ?locB)
        :precondition (and (player ?p) (character ?charA) (location ?locA) (location ?locB) (at ?p ?locA) (at ?charA ?locA))
        :effect (and (at ?p ?locB) (at ?charA ?locB) (not (at ?p ?locA)) (not (at ?charA ?locA))))

    (:action drop
        :parameters (?p ?loc ?i)
        :precondition (and (player ?p) (location ?loc) (item ?i) (has ?p ?i) (at ?p ?loc))
        :effect (and (not (has ?p ?i)) (has ?loc ?i)))
)