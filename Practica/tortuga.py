import turtle
t = turtle.Turtle()
s = turtle.Screen()
t.speed(0)

s.listen()
def arriba():
    t.setheading(90)
    t.forward(50)
def abajo():
    t.setheading(270)
    t.forward(50)
def izquierda():
    t.setheading(180)
    t.forward(50)
def derecha():
    t.setheading(0)
    t.forward(50)
def estrella():
    i = 0
    while(i < 10):
        t.left(150)
        t.forward(50)
        i += 1
s.onkey(arriba, "Up")
s.onkey(abajo, "Down")
s.onkey(izquierda, "Left")
s.onkey(derecha, "Right")
s.onkey(estrella, "r")
print("Usa las teclas para controlarlo!")
s.mainloop()