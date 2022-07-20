import pandas  as pd
import numpy as np
import matplotlib.pyplot as plt
#df = pd.read_csv("DadosGeofisicos.txt")
#df.to_csv("DadosGeofisicos.csv")
l=17
f=""
dados = pd.read_csv('DadosGeofisicos{}.csv'.format(f))

#Auxiliar to check index
"""
def check_index():
    date=dados["Data"].values
    c=0
    for i in date[::1]:
        if (i[12]=="0" and i[11]=="0"):
            print(c)
            break
        c=c+1
    r=0
    for i in date[::-1]:
        if (i[12]=="0" and i[11]=="0"):
            print(r)
            break
        r=r-1
    return c,r
c,r=check_index()
"""
def day_of_week(day=l):
    l=day
    lista_raspberry=[26015,103910,181802,259775,337417,415072,492929,570770,-30895]
    list_impa=[24, 48, 72, 96, 120, 144, 168, 192, 216]
    for i in range(len(lista_raspberry)-1):
        index_range=slice(lista_raspberry[i],lista_raspberry[i+1])
        temp=dados["Temp_Celcius"].values[index_range]
        press=dados["Pressure_hPa"].values[index_range]
        ax=dados["accelaration X (m/s^2)"].values[index_range]
        ay=dados["accelaration Y (m/s^2)"].values[index_range]
        az=dados["accelaration Z (m/s^2)"].values[index_range]
        mx=dados["Magnetometer X (micro-Teslas)"].values[index_range]
        my=dados["Magnetometer Y (micro-Teslas)"].values[index_range]
        mz=dados["Magnetometer Z (micro-Teslas)"].values[index_range]
        #configure below to set x values (now is for 24 h so 0 to 24)
        x=np.linspace(0,24 ,len(temp))
        fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,8))
        ax1.set_title("Temperatura (ºC)")
        ax1.plot(x, temp,label="Raspberry Pi")
        ax2.set_title("Pressão (hPa)")
        ax2.plot(x, press,label="Raspberry Pi")
        #ax2.set_xlabel('Week parts')
        ax2.set_xlabel('hours')
        ax1.legend()
        ax2.legend()
        #specify x-axis locations
        x_ticks = [0, 1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        #specify x-axis labels
        x_labels = [0, 1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        #add x-axis values to plot
        #plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.savefig("images/temp_press{}.png".format(l))
        plt.show()

        fig1, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,8))
        ax1.set_title("Aceleração ($m/s^2$)")
        ax1.plot(x, ax,label="x")
        ax1.plot(x, ay,label="y")
        ax1.plot(x, az,label="z")
        ax1.legend()
        ax2.set_title("Campo Magnético ($\mu T$)")
        ax2.plot(x, mx,label="x")
        ax2.plot(x, my,label="y")
        ax2.plot(x, mz,label="z")
        ax2.legend()
        ax2.set_xlabel('hours')
        plt.savefig("images/accelartion_magnetometer{}.png".format(l))
        #ax2.set_xlabel('Week parts')
        plt.show()
        l=l+1

#for week graphs
def week():
    index_range=slice(26015,-30895)

    temp=dados["Temp_Celcius"].values[index_range]
    press=dados["Pressure_hPa"].values[index_range]
    ax=dados["accelaration X (m/s^2)"].values[index_range]
    ay=dados["accelaration Y (m/s^2)"].values[index_range]
    az=dados["accelaration Z (m/s^2)"].values[index_range]
    mx=dados["Magnetometer X (micro-Teslas)"].values[index_range]
    my=dados["Magnetometer Y (micro-Teslas)"].values[index_range]
    mz=dados["Magnetometer Z (micro-Teslas)"].values[index_range]
    #configure below to set x values
    x=np.linspace(17,24 ,len(temp))

    fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,8))
    ax1.set_title("Temperatura (ºC)")
    ax1.plot(x, temp_estacao,label="Raspberry Pi")

    ax2.set_title("Pressão (hPa)")
    ax2.plot(x, press,label="Raspberry Pi")

    #ax2.set_xlabel('Week parts')
    ax2.set_xlabel('Jun')
    ax1.legend()
    ax2.legend()
    plt.savefig("images/temp_press{}.png".format("_week"))
    plt.show()
    fig1, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,8))
    ax1.set_title("Aceleração ($m/s^2$)")
    ax1.plot(x, ax,label="x")
    ax1.plot(x, ay,label="y")
    ax1.plot(x, az,label="z")
    ax1.legend()
    ax2.set_title("Campo Magnético ($\mu T$)")
    ax2.plot(x, mx,label="x")
    ax2.plot(x, my,label="y")
    ax2.plot(x, mz,label="z")
    ax2.legend()
    ax2.set_xlabel('Jun')
    plt.savefig("images/accelertion_magnetometer{}.png".format("_week"))
    #ax2.set_xlabel('Week parts')
    plt.show()

def dia(name_file):
    f="1"
    dados = pd.read_csv('DadosGeofisicos{}.csv'.format(f))

    temp=dados["Temp_Celcius"].values
    press=dados["Pressure_hPa"].values
    ax=dados["accelaration X (m/s^2)"].values
    ay=dados["accelaration Y (m/s^2)"].values
    az=dados["accelaration Z (m/s^2)"].values
    mx=dados["Magnetometer X (micro-Teslas)"].values
    my=dados["Magnetometer Y (micro-Teslas)"].values
    mz=dados["Magnetometer Z (micro-Teslas)"].values

    x=np.linspace(0,24 ,len(temp))
    x_ticks = [0, 1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    #specify x-axis labels
    x_labels = [0, 1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    #add x-axis values to plot
    #plt.xticks(ticks=x_ticks, labels=x_labels)
    fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,8))
    ax1.set_title("Temperatura (ºC)")
    ax1.plot(x, temp,label="Raspberry Pi")
    ax2.set_title("Pressão (hPa)")
    ax2.plot(x, press,label="Raspberry Pi")
    #ax2.set_xlabel('Week parts')
    ax2.set_xlabel('Jun')
    ax1.legend()
    ax2.legend()
    plt.savefig("images/temp_press{}.png".format(name_file))
    plt.show()
    fig1, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,8))
    ax1.set_title("Aceleração ($m/s^2$)")
    ax1.plot(x, ax,label="x")
    ax1.plot(x, ay,label="y")
    ax1.plot(x, az,label="z")
    ax1.legend()
    ax2.set_title("Campo Magnético ($\mu T$)")
    ax2.plot(x, mx,label="x")
    ax2.plot(x, my,label="y")
    ax2.plot(x, mz,label="z")
    ax2.legend()
    ax2.set_xlabel('Jun')
    
    plt.savefig("images/accelartion_magnetometer{}.png".format(name_file))
    #ax2.set_xlabel('Week parts')
    plt.show()
    mag,dec,H,inc,X,Y=magnetic_p(mx,my,mz)
    return print( "magnitude campo magnetico: {} \ndeclinacao: {}\ninclinacao: {}\n\
    X: {} Y: {}".format(mag,dec,inc,inc,X,Y))
def magnetic_p(mx,my,mz):
    mag=np.average((mx**2+my**2+mz**2)**0.5)
    dec=np.average(np.arctan(my/mx))*180/np.pi
    dec=dec-90
    H=np.average((mx**2+my**2)**0.5)
    inc=np.average(np.arctan(mz/H))*180/np.pi
    #X=H*np.cos(dec)
    #Y=H*np.sin(dec)
    print( "Magnitude campo magnético: {} \nDeclinação: {}\nInclinação: {}".format(mag,dec,inc,inc))
    return mag,dec,H,inc