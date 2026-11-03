// Exercise the actual packaged shadNet allocator, without network or databases.
#include "matching_types.h"
#include <cassert>
#include <set>
#include <cstdio>
void Unique(const Room& room) {
    std::set<unsigned> active_slots;
    for (const auto& member:room.members) {
        assert(member.memberId!=0);
        assert(active_slots.insert(member.memberId>>4).second);
    }
    assert(active_slots.size()==static_cast<size_t>(room.members.size()));
}
int main() {
    Room room;room.maxSlot=5;
    RoomMember proto;proto.npid="host";
    const auto host=room.addMember(proto)->memberId;
    proto.npid="guest-a";auto a=room.addMember(proto)->memberId;
    proto.npid="guest-b";auto b=room.addMember(proto)->memberId;
    assert(host==17 && a==34 && b==51);Unique(room);
    const auto old_a=a;
    assert(room.removeMember(a));proto.npid="guest-a";a=room.addMember(proto)->memberId;
    assert(a!=old_a && (a>>4)==(old_a>>4));
    assert(room.findById(b)->npid=="guest-b");Unique(room);
    for(int i=0;i<100;++i) {
        const bool first=(i%2)==0;auto& left=first?a:b;
        assert(room.removeMember(left));proto.npid=first?"guest-a":"guest-b";
        left=room.addMember(proto)->memberId;Unique(room);
        assert(room.findById(host)->npid=="host");
        assert(room.findById(a)->npid=="guest-a");
        assert(room.findById(b)->npid=="guest-b");
    }
    std::puts("PASS: production server allocator, non-last departure, 100 alternating rejoins, generation wrap, unique active slots");
}
