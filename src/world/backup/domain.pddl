(define (domain vincentland)
	(:predicates
		(location ?l)
		(item ?i)
		(character ?c)
		(has ?cl ?i)
		(at ?c ?l)
		(player ?p))

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
   		:precondition (and (character ?charA) (player ?p) (item ?i) (has ?charA ?i) (location ?loc) (at ?charA ?loc) (at ?p ?loc))
   		:effect (and (has ?p ?i) (not (has ?charA ?i))))

   	(:action giveTo
   		:parameters (?p ?charB ?i ?loc)
   		:precondition (and (character ?charB) (player ?p) (item ?i) (has ?p ?i) (location ?loc) (at ?charB ?loc) (at ?p ?loc))
   		:effect (and (has ?charB ?i) (not (has ?p ?i))))
)