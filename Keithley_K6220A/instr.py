import visa
from time import sleep

class Instr(object):

    def __str__(self):
        return self._visainstrument

    def __repr__(self):
        return self._visainstrument

    # def __new__(self):
    #     return self

    def __init__(self, visa_name):
        self.visa_name = visa_name
        self.visa_resource_manager = visa.ResourceManager()
        self._visainstrument = self.visa_resource_manager.open_resource(self.visa_name)
        self._visainstrument.timeout = 10000
        # self._visainstrument.values_format = "ascii"
        # self._visainstrument.lock = NI_NO_LOCK


    def idn(self):
        print(self._visainstrument.query("*IDN?"))

    def clear(self):
        self._visainstrument.clear()
        print("Instrument cleared.")

    def cls(self):
        # Clear the instrument's Status Byte
        self._visainstrument.write("*CLS")
        return "Status byte cleared (*CLS)."

    def get_control_port(self): # NOT NECESSARY IF USING GPIB OR LAN CONNEXION WITH VXI-11 INSTEAD OF SOCKETS
        bla = self._visainstrument.query("SYSTem:COMMunicate:TCPip:CONTrol?")
        try:
            output = int(bla)
        except:
            print("Error while getting control port: value returned: {0}".format(bla))
            output = -1
        return output

    def trigger(self):
        self._visainstrument.trigger()
        return "Trigger sent."

    def read(self):
        # print("Reading...")
        return self._visainstrument.read()

    def query(self, command):
        # print("Querying {0}...".format(command))
        return self._visainstrument.query(command)

    def write(self, command):
        # print("Writing {0}".format(command))
        self._visainstrument.write(command)

    def prepare_for_stb(self):
        # Clear the instrument's Status Byte
        self.cls()
        # Enable for the OPC bit (bit 0, which has weight 1) in the instrument's
        # Event Status Register, so that when that bit's value transitions from 0 to 1
        # then the Event Status Register bit in the Status Byte (bit 5 of that byte)
        # will become set.
        self._visainstrument.write("*ESE 1")
        return "OPC bit enabled (*ESE 1)."

    def prepare_for_srq(self):
        # Clear the instrument's Status Byte
        self.cls()
        # Enable for the OPC bit (bit 0, which has weight 1) in the instrument's
        # Event Status Register, so that when that bit's value transitions from 0 to 1
        # then the Event Status Register bit in the Status Byte (bit 5 of that byte)
        # will become set.
        self._visainstrument.write("*ESE 1")
        # Enable for bit 5 (which has weight 32) in the Status Byte to generate an
        # SRQ when that bit's value transitions from 0 to 1.
        self._visainstrument.write("*SRE 32")
        print("OPC bit enabled (*ESE 1). Enable generation of SRQ (*SRE 32).")

    def wait_opc(self):
        self._visainstrument.query("*OPC?")

    def wait_for_stb(self):
        self._visainstrument.write("*OPC")
        done = False
        while not(done):
            bla = self._visainstrument.query("*STB?")
            try:
                stb_value = int(bla)
            except:
                print("Error in wait(): value returned: {0}".format(bla))
            else:
                done = (2**5 == (2**5 & stb_value))
                sleep(0.01)

    def wait_for_srq(self): # ONLY WORKS WITH GPIB ! NOT TESTED !
        self._visainstrument.write("*OPC")
        self._visainstrument.wait_for_srq(10)
