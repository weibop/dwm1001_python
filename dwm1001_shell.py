import sys, serial
#pip install pyserial
from time import sleep

class shell():
   def __init__(self, com, speed=115200):
      self.ser = serial.Serial(com, 115200)
      print(self.ser.name, "open")
      self.tEnter()
      return
   
   def dump_resp(self, time = 1):
      sleep(time)
      buf_len = self.ser.inWaiting()
      # print("in wait byte length: %d"%buf_len)
      data = self.ser.read(buf_len) 
      print("%s"%data.decode("utf-8") )
      return data
      
   def find_in_resp(self, keyword, time=1):
      sleep(time)
      buf_len = self.ser.inWaiting()
      data = self.ser.read(buf_len) 
      # print("%s"%data)
      keyword_b = bytearray(str.encode(str(keyword)))
      idx = self.find_str(data, keyword_b)
      return idx, data
   
   # input double enter and start shell:
   def dEnter(self):
      i = 5
      while(i > 0):      
         print("(trying to input double Enter...)")
         self.ser.write(b'\r')     # write a string
         sleep(0.2)
         self.ser.write(b'\r')     # write a string
         sleep(1)
         [result, data] = self.find_in_resp(b'\r\ndwm>')
         if result:
            print("dwm>")            
            return 0;
         i -= 1         
      print(" *** Error *** Double Enter timed out, can't enter shell mode.\n")    
      return -1;
      
   # input double enter and start shell:
   def tEnter(self):
      i = 5
      while(i > 0):      
         print("(trying to input triple Enter...)")
         self.ser.write(b'\r')     # write a string
         sleep(1.1)
         self.ser.write(b'\r')     # write a string
         sleep(0.2)
         self.ser.write(b'\r')     # write a string
         sleep(1)
         [result, data] = self.find_in_resp(b'\r\ndwm>')
         if result:
            print("dwm>")            
            return 0;
         i -= 1         
      print(" *** Error *** Triple Enter timed out, can't enter shell mode.\n")    
      return -1;
   
   # this starts shell by 'frst' and double enter:
   def cmd(self, string):
      string = str(string)
      string = string + '\r'
      barray = bytearray(str.encode(string))
      i = 0
      size = 1
      while( len(barray) > 0):
         this = min(size, len(barray))
         self.ser.write(barray[0:this])     # write a string
         barray = barray[this:]
         sleep(0.02)# need this delay for dwm1001 to parse uart data.
      return
      
   def cmd_dump(self, string):
      self.cmd(string)   
      return self.dump_resp()
      
   def find_str(self, s, char):
      index = 0
      if char in s:
         c = char[0]
         for ch in s:
            if ch == c:
               if s[index:index+len(char)] == char:
                  return index
            index += 1
      return -1
       
   def close(self):
      self.ser.close()             # close port
   
   
if __name__ == "__main__":
   print(__name__, "example ...")
   s = shell('COM3') #change this number to suit different setup
   s.dEnter()
   s.cmd('nmg')
   s.dump_resp()
   s.close()

