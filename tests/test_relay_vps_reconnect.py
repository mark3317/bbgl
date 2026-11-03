"""Real BBSC TCP relay on the public VPS; ephemeral identities, no account/save writes."""
import os,queue,socket,struct,threading,time
from pathlib import Path
HOST='77.73.67.175';PORT=20444
party=0xBB000000 | int.from_bytes(os.urandom(3),'little');guestid=party^0x00100000;otherid=party^0x00200000
clients=[]
class Client:
 def __init__(self,player,session):
  self.sock=socket.create_connection((HOST,PORT),timeout=5);self.sock.settimeout(.2)
  self.frames=[];self.lock=threading.Lock();self.stop=False
  threading.Thread(target=self.reader,daemon=True).start();clients.append(self)
  self.send(player,session,0x23)
 def reader(self):
  buf=b''
  while not self.stop:
   try: part=self.sock.recv(65536)
   except socket.timeout: continue
   except OSError: break
   if not part:break
   buf+=part
   while len(buf)>=4:
    n=struct.unpack_from('<I',buf)[0]
    assert n<=65536
    if len(buf)<n+4:break
    with self.lock:self.frames.append(buf[4:4+n])
    buf=buf[4+n:]
 def send(self,player,session,kind):
  p=b'SHAD\x40'+struct.pack('<II',player,session)+b'SHAD'+bytes([kind])
  self.sock.sendall(struct.pack('<I',len(p))+p)
 def peerleft(self):
  with self.lock:return [x for x in self.frames if len(x)==9 and x[0]==0x7e]
 def close(self):
  if self.stop:return
  self.stop=True
  try:self.sock.shutdown(socket.SHUT_RDWR)
  except OSError:pass
  self.sock.close()
def wait_for(pred,seconds):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  if pred():return True
  time.sleep(.05)
 return False
if __name__ == '__main__':
    try:
     old=Client(party,party);guest=Client(guestid,party);unrelated=Client(otherid,otherid)
     new=Client(party,party);time.sleep(.5)
     old.send(party,party,0x2a);time.sleep(.3)
     with guest.lock:assert not any(x.endswith(b'SHAD\x2a') for x in guest.frames)
     old.close();time.sleep(1)
     assert not guest.peerleft()
     print('PASS: replacement before old EOF and stale explicit leave preserve party',flush=True)
     new.close();time.sleep(.3)
     replacement=Client(party,party)
     time.sleep(10.5)
     assert not guest.peerleft()
     print('PASS: reconnect after EOF cancels delayed departure beyond timer deadline',flush=True)
     replacement.close()
     assert wait_for(lambda:guest.peerleft(),12)
     expected=struct.pack('<BII',0x7e,party,party)
     assert guest.peerleft()==[expected]
     assert not unrelated.peerleft()
     print('PASS: real final departure notifies exactly once, scoped to party',flush=True)
     print('VPS TCP recovery PASS: party={:08x}'.format(party),flush=True)
    finally:
     for c in clients:c.close()
