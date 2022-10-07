import time, gc, socket,ntptime,dht
from machine import Pin
temp=0
hum=0
tt=[0,0,0,0,0,0,0,0]
d=dht.DHT11(Pin(13))

def flash(times):
    led = Pin(2,Pin.OUT)

    for i in range(times):
        led.value(not led.value())
        time.sleep(0.1)
        led.value(not led.value())
        time.sleep(0.1)

def readntp():
    t_ntp=[0,0,0,0,0,0,0,0]
    t=ntptime.time()
    t_tuple=time.localtime(t)
    time.sleep(0.5)
    t_ntp[0:7]=t_tuple[0:7]
    return(t_ntp)

def DHT11():
    d.measure()
    temp=d.temperature()
    hum=d.humidity()
    print('溫度:{}\u00b0C'.format(temp))
    print('濕度:{}%'.format(hum))
    print('')
    return(temp,hum)

def url(PORT):
    import socket
    LED0 = Pin(5, Pin.OUT)
    LED1 = Pin(4, Pin.OUT)
    LED2 = Pin(0, Pin.OUT)
    LED0.value(1)
    LED1.value(1)
    LED2.value(1)
    n1=0
    n2=0
    tt=[0,0,0,0,0,0,0,0]
    temp=0
    hum=0
    s=socket.socket()
    HOST='0.0.0.0'
    httpHeader = b"""\
    HTTP/1.0 200 OK

    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>MicroPython</title>
      </head>
      <body>
        <p><b><h1 align="center"> 翁志杰_L0220_通信網路技術實驗室鐵捲門</h1></b></p>
        <p><b><h1 align="center">連線{n2}次，啟閉{n1}次，目前時間{t0}年{t1}月{t2}日{t3}h{t4}m{t5}s</h1></b></p>
        <form align="center">
        <button name="Up" value="ON001" type="submit"
        style="width:400px;height:100px;font-size:40px;color:red;background:#3c99dc">上</button><br><br>
        <button name="Stop" value="ON001" type="submit"
        style="width:400px;height:100px;font-size:40px;color:red;background:#d5f3fe">停</button><br><br>
        <button name="Down" value="ON001" type="submit"
        style="width:400px;height:100px;font-size:40px;color:red;background:#66d3fa">下</button>
        </form>
      </body>
    </html>
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(30)

    while True:
        client,addr=s.accept()
        yy=client.settimeout(3.0)
        try:
            req=client.recv(512)
#            temp, hum = DHT11()
            tt=readntp()
            print(tt)
            time.sleep(0.1)
            gc.collect()
        except OSError:
            print(yy,' Oops! Timeout happened')
            gc.collect()
            req=0
            client,addr=s.accept()

        request = str(req)
        req=0
        LEDON0 = request.find('/?Up=ON001')
        LEDON2 = request.find('/?Stop=ON001')
        LEDOFF0 = request.find('/?Down=ON001')
        if LEDON0 == 6:
            LED0.value(0)
            time.sleep(0.1)
            LED0.value(1)
            n1=n1+1
            flash(1)
        if LEDON2 == 6:
            LED1.value(0)
            time.sleep(0.1)
            LED1.value(1)
            n1=n1+1
            flash(2)
        if LEDOFF0 == 6:
            LED2.value(0)
            time.sleep(0.1)
            LED2.value(1)
            n1=n1+1
            flash(3)

        n2+=1
        client.send(httpHeader.format(n2=n2,n1=n1,temp=temp,hum=hum,t0=tt[0],t1=tt[1],t2=tt[2],t3=tt[3]+8,t4=tt[4],t5=tt[5]))
        client.close()
        print(n2,'-'*40)
