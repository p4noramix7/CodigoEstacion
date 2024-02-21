import serial
import os
import threading
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.animation as animation




fig = plt.figure()

graf1= fig.add_subplot(2,2,1)
graf2= fig.add_subplot(2,2,3)
graf3= fig.add_subplot(2,2,2)

data1 = []


try:
    PuertoSerie = serial.Serial('COM8', 9600)
except:
    print("Puerto incorrecto")


def readSerial():
    global PuertoSerie

    conexion=sqlite3.connect("db.db")
    while 1:
        sensor = PuertoSerie.readline()
        sensor=(sensor.decode("utf8").rstrip()).split(",")
        print(sensor)
        data1.append(sensor)

        conexion.execute("insert into Datos(Segundo,Temperatura,Presion,Altura) values (?,?,?,?)", (sensor[3], sensor[0], sensor[1], sensor[2]))
        conexion.commit()
    conexion.close()
threading.Thread(target=readSerial).start()
def update(i):

    global data1
    graf1.clear()
    graf2.clear()
    graf3.clear()
    graf1.set_title("Temperatura C°/s")
    graf2.set_title("Altura m/s")
    graf3.set_title("Presión Pa/s")
    x=[]
    yT=[]
    yA=[]
    yP=[]
    for i in data1:
        x.append(int(i[3]))
        yT.append(float(i[0]))
        yA.append(float(i[2]))
        yP.append(float(i[1]))
    if len(data1)>=50:
        data1.pop(0)
    graf1.plot(x, yT, "r-o")
    graf1.relim()
    graf1.autoscale_view()
    graf2.plot(x, yA, "r-o")
    graf2.relim()
    graf2.autoscale_view()
    graf3.plot(x, yP, "r-o")
    graf3.relim()
    graf3.autoscale_view()

animacion=animation.FuncAnimation(fig, update, interval=500)
plt.show()
