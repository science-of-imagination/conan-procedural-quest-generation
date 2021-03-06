(define (problem lumberjack)
    (:domain vincentland)
    (:objects lumberjack you wood forest camp bakery forge)
    (:init (location forest)
          (character lumberjack)
          (location forge)
          (location bakery)
          (location camp)
          (item wood)
          (has forest wood)
          (at lumberjack camp)
          (player you)
          (at you bakery))

    (:goal (and (has lumberjack wood)
            (at lumberjack camp)))
)