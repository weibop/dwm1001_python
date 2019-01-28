from dwm1001_shell import shell 
import sys
from time import sleep

class shell_test():
   def __init__(self):
      #open a file for test result
      self.f = open(str(sys.argv[1])+'_shell_cmd_test_results.log', 'w')
      return
   
   def check(self, shell, cmd, kw):
      print('checking \'' + cmd + '\' ...   ', end='')
      # input the command
      shell.cmd(cmd)
      # check if keyword is inside the response text
      [idx, data] = shell.find_in_resp(kw)  
      self.f.write(cmd + ' : ')
      if (idx == -1):
         self.f.write('\t\t*** fail ***\n')
         print('\t\t\t*** fail ***')
         print('rsp text: %s' %data.decode())
      else:
         self.f.write('pass\n')
         print('pass')
      return
      
   def check_rst(self, shell, cmd, enter = 2):
      print('checking \'' + cmd + '\' ...   ', end='')
      # input the command
      shell.cmd(cmd)
      sleep(1.5)
      # double Enter to re-enter shell mode
      if (enter == 3):# for lp mode
         rv = shell.tEnter()
      else:
         rv = shell.dEnter()
      self.f.write(cmd + ' : ')
      if (rv == -1):
         self.f.write('\t\t*** fail ***')
         print('\t\t\t*** fail ***')
      else:
         self.f.write('pass\n')
         # print('rsp text: ' + data)
         print('pass')
      return
      
   def close(self):
      self.f.close()
      
   
   
if __name__ == "__main__":
   print(__name__, " start ...")
   
#open COM port
s = shell(sys.argv[1])
#open test instance
st = shell_test()

st.check(s, '?', 'this help')
st.check(s, 'help', 'this help')

st.check(s, 'gc 12', 'gpio12: 0')
st.check(s, 'gg 12', 'gpio12: 0')
st.check(s, 'gs 12', 'gpio12: 1')
st.check(s, 'gt 12', 'gpio12: 0')

st.check(s, 'f', 'tot=')
st.check(s, 'si', 'panid')
st.check(s, 'ut', 'uptime:')
st.check_rst(s, 'reset')
# st.check_rst(s, 'frst')# do this elsewhere

st.check(s, 'twi 0x32 0x0f', 'twi: addr=0x32, reg[0x0f]=0x33')
st.check(s, 'aid', 'acc: 0x33')
st.check(s, 'av', 'acc: x =')
st.check(s, 'scs 2', 'ok')
st.check(s, 'scg', 'sensitivity=2')

st.check(s, 'les', 'dwm>')#
st.check(s, 'lec', 'dwm>')#
st.check(s, 'lep', 'dwm>')#

st.check(s, 'utps 0xc5 0x28496a8b', 'utps: pg_delay=xC5 tx_power=x28496A8B')#
st.check(s, 'utpg', 'utpg: pg_delay=xC5 tx_power=x28496A8B')#



st.check(s, 'nmg', 'tn (')
st.check_rst(s, 'nmp')
st.check(s, 'nmg', 'tn (pasv')
st.check_rst(s, 'nmo')
st.check(s, 'nmg', 'tn (off')
st.check_rst(s, 'nma')
st.check(s, 'nmg', 'an (act')
st.check_rst(s, 'nmi')
st.check(s, 'nmg', 'ani (act')
st.check_rst(s, 'nmt')
st.check(s, 'nmg', 'mode: tn (act,twr,np,le)')
st.check_rst(s, 'nmtl', 3)
st.check(s, 'nmg', 'mode: tn (act,twr,lp,le)')
st.check_rst(s, 'nmb')
st.check(s, 'nmg', 'bn (act')
st.check_rst(s, 'frst')

# st.check(s, 'bpc', 'BW/TxPwr comp')
st.check(s, 'la', 'AN: cnt=')
st.check(s, 'lb', '[')
st.check(s, 'nis 0', 'nis: ok')
st.check(s, 'nls hi_123', 'nls: ok')
# st.check(s, 'ln', 'dwm>')# this resp depends on mode
# st.check(s, 'lr', 'bh: cnt') # this resp depends on mode
# st.check(s, 'lrn', 'bhnext: cnt') # this resp depends on mode
st.check(s, 'lr', 'dwm>')
st.check(s, 'lrn', 'dwm>')
st.check(s, 'udi', 'dl: len=')
st.check(s, 'uui', 'ul: len=')
st.check(s, 'stg', 'uptime')
st.check(s, 'stc', 'dwm>')

st.check(s, 'tlv 0x15 0x00', 'OUTPUT FRAME:')
st.check(s, 'aurs 1 1', 'err code: 0')
st.check(s, 'aurg', 'err code: 0, upd rate: 1, 1(stat)')
st.check(s, 'aps 123 345 234', 'err code: 0')
st.check(s, 'apg', 'x:')
st.check(s, 'acas 0 0 0 1 0 2 0', 'err code: 0')
st.check(s, 'acts 0 1 1 1 0 1 0 2 0', 'err code: 0')
st.check(s, 'akc', 'ok')
st.check(s, 'aks 11111111222222223333333344444444', 'key_set: 11111111222222223333333344444444')

st.check(s, 'anc', 'ok')
st.check(s, 'ans 123abc', 'data: 123ABC')
st.check(s, 'ang', 'data: 123ABC')

st.check_rst(s, 'frst')

s.close()
st.close()