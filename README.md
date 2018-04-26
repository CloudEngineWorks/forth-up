# forth-up
A Forth interpreter written in Python targeting CircuitPython and perhaps other Python environments.

Admittedly inefficient and a little insane, but is for fun until the wave of Forth aware programmers has a resurgence.
Until then, this project will stay in the back waters of language interpreters, land locked in an cove that only Python programmers that wish to explore being Forth programmers, that also use microprocessors, dwell.

But it gets worse, because this interpreter is not a standard Forth interpreter. Liberties have been taken with not implementing some things (of course you are welcome to add more features) and changing some central things about Forth.
Forth purists have left the site or at least they will after they glance at the list of changes and omissions.

Exploring the old Forth language with an eye to the modern trend toward functional programming has been the focus of this development. Forth has been called a procedural language, but is that really true? Here we can discuss its' interpretation. and extend it with pure functional features. So, to differentiate it from the classic Forth language, we call this interpreter 'Forth-Up.'  

## A Functional slant on the classic Forth -- Joy
The first experimental change was to the classic `if` `then` `else` syntax in Forth. The issue is that it is not an entirely post-fix operator (it has state while searching for `then` and possibly `else`). The aim here is to make Forth-Up as functional as possible and since the core of the post-fix operators already have nice functional qualities, it seemed like a good idea to coffer a substitute to the `if` flow of control operator, one that gets everything from the stack (not by looking ahead on programs word list).  This approach does leave one thing to be desired, it is sometimes needed to know if a function takes some of its arguments statically (from the program list) or from preexisting stack elements. To declare the that some function `foo` should consume program list arguments (statically) we use a prefix notation `1--foo` to say that foo needs one static argument and the rest (if any) will come from the stack.  
