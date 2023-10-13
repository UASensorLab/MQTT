import paho.mqtt.client as mqtt
import random
import time
import serial
import sys
import time
import glob

from time import strftime, localtime
import keyboard
import os
global zcom

def on_connect(client,userdata,flags,re):
    if re == 0:
        print('test work')
        client.subscribe("test/topic")
    else:
        print("test not work")


client = mqtt.Client()
client.on_connect = on_connect


client.connect("149.165.159.142",1883,60)

def serial_ports():
    """
    Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# while True:
#     temperature = random.uniform(10,30)
#     humidity = random.uniform(10,80)
#     wind_speed = random.uniform(0,10)
#
#     client.publish("test/topic",f"temperature:{temperature}(,humidity:{humidity}%,wind_speed:{wind_speed}m/s")
#
#
# time.sleep(10)
import random

# Simulated data collection loop
print("### SIMULATED DATA COLLECTION STARTED ###")
try:
    while True:
        # Generate a random value (replace this with your desired random data generation)
        random_value = random.uniform(0, 100)  # Change the range as needed
        # Get the current timestamp
        ts = strftime("%d %b %Y %H:%M:%S", localtime())
        # Format and write the data to the file (or print it)
        data_point = f"{ts}, {random_value:.2f}\n"
        client.publish("test/topic", f"data:{data_point}")
        print(f"TIME: {ts}, VALUE: {random_value:.2f}")
        # Sleep for the specified time between data points
        tx = "1"
        time.sleep(2)
except KeyboardInterrupt:
    # Graceful shutdown when the user presses Ctrl-C
    print("\n### SIMULATED DATA COLLECTION STOPPED ###")
    print("### PROGRAM STOPPED ###")
# Close any necessary resources (e.g., files)
# ...

## MAIN PROGRAM  ##
# Get some Initial Data #
print("\n#########################################")
print("###      EVOM3CNX Version 5.A         ###")
print("### World Precision Instruments, LLC  ###")
print("###         AUGUST 2020               ###")
print("#########################################\n")
rx = False
results = serial_ports()
print("Serial Ports Found", results)
print("\n TESTING PORTS FOR EVOM3 ...")
for i in range(256):
    try:
        if (results[i] == "COM1" or results[i] == "COM2"):
            pass
        else:
            portstr = str(results[i])
            ser = serial.Serial(portstr, 38400, timeout=0, rtscts=True)
            wxx = '\r Q \r\n'
            wx3 = wxx.encode()
            q = ser.write(wx3)
            time.sleep(0.5)

            qq = ser.read(ser.in_waiting).decode()
            if len(qq) > 5:
                print(" FOUND EVOM3 PORT AS: ", portstr)
                rx = True
                zcom = portstr

            q = ser.write(wx3)
            ser.close()
    except:
        pass

if (rx == False):
    print("EVOM3 PORT NOT FOUND.. \n 1. Check Connection \n 2. Reboot EVOM3 \n")
    time.sleep(2)
while (rx == True):
    print("**********************************************************************")
    print("*                        SET UP REMOTE READOUT                       *")
    print("*                                                                    *")
    print("* (1) SELECT FILE NAME FOR OUTPUT FILE                               *")
    print("*                                                                    *")
    print("* (2) SELECT INITIAL OPERATING MODE: (R)ESISTANCE or (V)OLTAGE       *")
    print("*                                                                    *")
    print("* (3) SELECT TIME BETWEEN MEASUREMENTS [ FROM 0-99 SECONDS]          *")
    print("*                                                                    *")
    print("* (4) SELECT # OF DATA POINTS[ FROM 1-999, ZERO FOR CONTINUOUS]      *")
    print("*                                                                    *")
    print("* (5) SELECT WAIT BETWEEN DATA SETS [1-360 MINS, ZERO FOR CONTINUOUS]*")
    print("**********************************************************************\n")

    writefile = input(" (1) ENTER OUTPUT FILE NAME [ENTER for WPI_EVOM3.csv]: ")
    modex = input(" (2) MODE - 'R' FOR RESISTANCE OR 'V' FOR VOLTAGE :")
    tx = input(" (3) ENTER TIME BETWEEN MEASUREMENTS [0-99 SECONDS]:")
    dscs = input(" (4) NUMBER OF DATA POINTS [1-65000, ZERO FOR CONTINUOUS]:")
    tx2s = input(" (5) SELECT WAIT TIME BETWEEN DATA SETS[1-360 MINS, ZERO IF NONE]:")
    #  CMD format sent to EVOM3 is X [y] where [y] is the time(secs) between readings.
    if (zcom == ""): zcom = "COM4"  # Active COM port found "FT232R USB UART" is installed on PC
    if (len(writefile) < 4): writefile = "WPI_EVOM3.csv"
    if os.path.exists(writefile): os.remove(writefile)  # make sure file is closed and wiped
    modex = modex.upper()  # adjust capitals
    if (modex != "R" and modex != "V"): modex = "R"  # trap error
    if (
            tx == "" or tx == "0" or tx == "o" or tx == "O"): tx = "0.85"  # We need a little delay from zero, trap error entry #
    txx = int(float(tx))
    if (txx < 0): tx = "0"
    if (txx > 99): tx = "99"
    if (
            dscs == "" or dscs == "0" or dscs == "o" or dscs == "O"): dscs = "65536"  # Trap error entry, Set to continuous  2^16#
    if (tx2s == "" or tx2s == "O" or tx2s == "o"): tx2 = "0"  # Trap error entry
    dsc = int(float(dscs))  # convert string to integer
    tx2 = float(tx2s)  # convert string to float
    if (tx2 > 360): tx2 = 360  # Trap error entry
    if (tx2 < 0): tx2 = 0  # Trap error entry
    tag_modex = "RESISTANCE"
    if (modex == "V"): tag_modex = "VOLTAGE"

    # Open Port And Read #
    print("**********************************************************************\n")
    print(" OPENING OUTPUT FILE:" + writefile + " FOR OUTPUT")
    print(" OPENING PORT " + zcom + " FOR DATA INPUT ")
    print(" OPERATING MODE IS " + tag_modex)
    print(" TIME (SECS) BETWEEN MEASUREMENTS:" + str(tx))
    print(" NUMBER OF DATA POINTS PER SET:" + str(dsc))
    print(" WAIT TIME (MINS) BETWEEN DATA SETS:" + str(tx2) + "\n")
    print(" PRESS CTL-'x' KEY TO STOP DATA COLLECTION")
    print("********************************************************************\n\n")
    wx = open(writefile, 'w', -1)
    writeit = "   TIME    ,   DATA    ,   VALUE \n"
    t = wx.write(writeit)
    with serial.Serial(zcom, 38400, timeout=0, rtscts=True) as ser:  # open serial port
        ser.flush()
        # set mode
        wxx = 'M' + modex + ' \r\n'
        wx3 = wxx.encode()
        q = ser.write(wx3)
        # Open data port and start data feed
        wxx = 'X ' + str(tx) + ' \r\n'
        wx3 = wxx.encode()
        q = ser.write(wx3)
        # need to wait for characters to build in buffer
        ser.flush()
        time.sleep(1)
        while (ser.in_waiting < 5): print(ser.in_waiting)
        p = ser.readline().decode().rstrip('\n')
        print("Reading from EVOM3:", p)

        # TEST FOR FLOW CONTROL ON/OFF #
        sx = p[-3:]
        if (sx == "OFF"):  # Reset data port
            wxx = 'X  ' + str(tx) + ' \r\n'
            wx3 = wxx.encode()
            q = ser.write(wx3)
            time.sleep(1)
        # END TEST
        ntotal = 0  # ntotal is the total number of data points before this cycle
        ncount = 0  # ncount is the number of data points per cycle
        # MAIN LOOP
        print(" ### DATA COLLECTION STARTED ###")

        while not (keyboard.is_pressed('x')):  # 'X' means CTL-X #
            while (ncount < dsc + 1):  # total number of data points per set
                # Wait for buffer and this depends on time between readings
                if (ser.in_waiting > 7):
                    xr = ser.read(ser.in_waiting)  # read  bytes from EVOM3
                    xr2 = xr.decode()
                    xy = xr.decode().rstrip('\n')

                    iflag = 0
                    if (xr2 == xy): iflag = 1  # checks to see if we have a byte error
                    x = xy.lstrip('\r')  # strip initial "return" character

                    try:  # see if data is a number or not
                        x = float(x)
                        xfmt = str("%6.1f" % x)
                    except:  # if data read is an EVOM3 warning, reset data to zero
                        x = "0000.0"
                        xfmt = "0000.0"
                    if (ncount == 0):  # First data point is garbage
                        ncount = ncount + 1
                        iflag = 0
                    if (iflag == 1):
                        strncount = str(ncount + ntotal)  # number of data points total
                        ts = strftime("%d %b %Y %H:%M:%S", localtime())  # get and format time stamp
                        writeit = ts + "," + strncount + "," + xfmt + "\n"  # formulate record
                        print("TIME:", ts, " DATAPOINT:", strncount, " VALUE:", xfmt)  # write record to console


                        t = wx.write(writeit)  # write record to file
                        ncount = ncount + 1  # increment data point counter
                    #           ## wait for next data point is done by CMD to EVOM3
                    ser.flush()  # ensures we don't have left over garbage in serial
                print("\r#WAITING#/ ", end="")
            print("\n * DATA CYCLE COMPLETED...WAITING FOR NEXT CYCLE IN ", str(tx2), " MINS *\n")
            if (keyboard.is_pressed('x')):  # Graceful shutdown
                print(" ### DATA COLLECTION STOPPED ### ")
                print(" ### PROGRAM STOPPED         ### ")
                # close up files and cleanup
                ser.flush()
                rx = False
                wxx = 'X ' + str(tx) + ' \r\n'
                wx3 = wxx.encode()
                q = ser.write(wx3)
                ser.close()
                wx.close()
                time.sleep(2)
                sys.exit()
            # PUT THE EVOM3 INTO VOLTAGE MODE STOP DATA COLLECTION DURING SLEEP #
            ser.flush()
            wxx = 'X \r\n'
            wx3 = wxx.encode()
            q = ser.write(wx3)  # STOP DATA
            # need to wait for characters to build in buffer
            time.sleep(0.5)
            while (ser.in_waiting < 5): print(ser.in_waiting)
            p = ser.readline().decode().rstrip('\n')
            p = p.upper()
            print("STOP RESPONSE", p, end="")
            wxx = 'MV \r\n'
            wx3 = wxx.encode()
            q = ser.write(wx3)  # SET VOLTAGE MODE
            # need to wait for characters to build in buffer
            time.sleep(1)
            while (ser.in_waiting < 5): print(ser.in_waiting)
            p = ser.readline().decode().rstrip('\n')
            p = p.upper()
            print(p, "WHILE WAITING  ")
            print("PAUSING FOR " + str(tx2 * 60) + " SECONDS")

            # GO TO SLEEP
            # time.sleep(tx2*60) # sleep for timeout period by tx2 (which is in minutes, but sleep is in seconds)
            twait = int(tx2 * 60)
            for remaining in range(twait, 0, -5):
                print("\r#/ ", end="")
                time.sleep(1)
                print("\r#--", end="")
                time.sleep(1)
                print("\r#| ", end="")
                time.sleep(1)
                print("\r#/ ", end="")
                time.sleep(1)
                print("\r#--", end="")
                time.sleep(1)
                print("\r#| ", end="")

            # WAKE UP AND RESTORE TO ORIGINAL MODE #
            print("\n")
            ser.flush()  # MIGHT BE SOMETHING IN THE BUFFER
            wxx = 'M' + modex + '\r\n'  # SET THE MODE CORRECTLY
            wx3 = wxx.encode()
            q = ser.write(wx3)  # SEND THE COMMAND
            ser.flush()
            # need to wait for characters to build in buffer
            time.sleep(0.5)
            # while(ser.in_waiting <5):print(ser.in_waiting)
            p = ser.readline().decode().rstrip('\n')
            print(p.upper(), " RESTORED ")

            # CHECK THAT THE DATA CONENCTION IS OKAY
            ser.flush()
            wxx = 'X ' + str(tx) + ' \r\n'
            wx3 = wxx.encode()
            q = ser.write(wx3)  # Start Command

            # need to wait for characters to build in buffer
            time.sleep(0.5)

            # while(ser.in_waiting <5):#print(ser.in_waiting)
            p = ser.readline().decode().rstrip('\n')
            print(p)

            # Test for flow control on or off #
            sx = p[-3:]
            if (sx == "OFF"):
                # ser.flush()
                wxx = 'X  ' + str(tx) + ' \r\n'
                wx3 = wxx.encode()
                q = ser.write(wx3)  # Start Command
                time.sleep(1)
            # END TEST
            # flush the serial so the EVOM3 can settle down
            ser.flush()
            ntotal = ntotal + ncount - 1
            ncount = 0  # reset counter for each data set

            # End of Data Capture Loop #

        print(" ### DATA COLLECTION STOPPED ### ")
        print(" ### PROGRAM STOPPED         ### ")
        #       close up files and cleanup
        rx = False
        ser.flush()
        wxx = 'X ' + str(tx) + ' \r\n'
        wx3 = wxx.encode()
        q = ser.write(wx3)
        ser.close()
        wx.close()
        time.sleep(2)

#  PROGRAM END  #
try:
    ser.close()  # this is here to close serial port in case of an untrapped error
    wx.close()  # this is here to close data file in case of an untrapped error
except:
    pass
#  PROGRAM END  #


