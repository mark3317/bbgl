"""Opt-in: compile real DLL I/O functions and exchange frames through the public VPS."""
from pathlib import Path
import os,subprocess
ROOT=Path(__file__).resolve().parents[1]
def function(src,name):
 a=src.index(name);b=src.index('{',a);depth=1;i=b+1
 while depth:
  if src[i]=='{':depth+=1
  elif src[i]=='}':depth-=1
  i+=1
 return src[a:i]
def main():
 src=(ROOT/'mods-src/BBSC/emulator/mod/bbsc_relay.cpp').read_text(encoding='utf-8')
 globals=src[src.index('std::mutex send_mutex;'):src.index('void Log(')]
 cpp=r'''
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <algorithm>
#include <atomic>
#include <cassert>
#include <condition_variable>
#include <cstdint>
#include <cstring>
#include <deque>
#include <iostream>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
#include "bbsc_relay_io.h"
using u8=std::uint8_t;using u32=std::uint32_t;using u64=std::uint64_t;
namespace BbscMod { u32 P2PChannelSend(const void*,u32){assert(false);return 0;} }
namespace {
constexpr size_t EnvelopeSize=13;constexpr u8 EnvelopeType=0x40;
'''+globals+r'''
void Log(const std::string& text){std::cout<<text<<std::endl;}
u32 SessionKey(){return own_id;}
int last_read_result=0;
'''+function(src,'bool ReadAll(')+'\n'+function(src,'u32 SendFrame(')+'\n'+function(src,'std::string SocketError(')+'\n'+function(src,'DWORD WINAPI WriterThread(')+r'''
SOCKET Connect() {
 SOCKET s=socket(AF_INET,SOCK_STREAM,0);assert(s!=INVALID_SOCKET);
 sockaddr_in to{};to.sin_family=AF_INET;to.sin_port=htons(20444);
 assert(inet_pton(AF_INET,"77.73.67.175",&to.sin_addr)==1);
 assert(connect(s,reinterpret_cast<sockaddr*>(&to),sizeof(to))==0);
 BOOL yes=TRUE;assert(setsockopt(s,IPPROTO_TCP,TCP_NODELAY,reinterpret_cast<const char*>(&yes),sizeof(yes))==0);
 u_long on=1;assert(ioctlsocket(s,FIONBIO,&on)==0);return s;
}
}
int main(){
 WSADATA wsa{};assert(WSAStartup(MAKEWORD(2,2),&wsa)==0);
 own_id=0xBB000000|(GetCurrentProcessId()<<1)|1;peers=1;
 const SOCKET receiver=Connect();relay=Connect();
 auto writer=CreateThread(nullptr,0,WriterThread,nullptr,0,nullptr);assert(writer);CloseHandle(writer);
 std::atomic<unsigned> received{0};
 std::thread reader([&]{
  while(received<100){
   u32 size;assert(ReadAll(receiver,&size,4));assert(size<=65536);
   std::vector<char> data(size);assert(ReadAll(receiver,data.data(),size));
   if(size!=EnvelopeSize+2048 || data[17]!=0x7c)continue;
   u32 from=0,seq=0;std::memcpy(&from,data.data()+5,4);if(from!=own_id)continue;
   std::memcpy(&seq,data.data()+18,4);assert(seq==received);++received;
  }
 });
 for(u32 i=0;i<100;++i){
  std::vector<char> body(2048,42);std::memcpy(body.data(),"SHAD",4);body[4]=0x7c;
  std::memcpy(body.data()+5,&i,4);SendFrame(body.data(),body.size());Sleep(2);
 }
 reader.join();
 {std::scoped_lock lock{send_mutex};assert(send_queue_bytes==0 && tx_frames==100 && dropped_frames==0);
  std::cout<<"PASS: real DLL nonblocking reader/writer through VPS:100 ordered frames, zero drops; high_water="<<tx_high_water<<" bytes waits="<<tx_waits<<std::endl;}
 shutdown(receiver,SD_BOTH);closesocket(receiver);
 std::cout.flush();std::_Exit(0); // process owns persistent production writer thread
}
'''
 source=ROOT/'out/tests/relay-writer-vps.cpp';binary=source.with_suffix('.exe');source.write_text(cpp,encoding='utf-8')
 env=dict(os.environ);env['PATH']=r'C:\msys64\clang64\bin;'+env['PATH']
 subprocess.run([r'C:\msys64\clang64\bin\clang++.exe','-std=c++23','-I'+str(ROOT/'mods-src/BBSC/emulator/mod'),str(source),'-lws2_32','-o',str(binary)],check=True,env=env)
 subprocess.run([str(binary)],check=True,env=env,timeout=40)
if __name__=='__main__':main()
