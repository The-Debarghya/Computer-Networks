#include <stdint.h>

#define ETH_P_ARP	0x0806		/* Address Resolution packet */
#define ETH_P_IP	0x0800		/* Internet Protocol packet	*/

struct ethernet_header{
    unsigned char destmac[6];
    unsigned char srcmac[6];
    uint16_t ethertype;
    unsigned char payload[];
} __attribute__((packed));

extern struct ethernet_header *ethernet_packet;
extern int ethernet_len;

void parse_ethernet();
void handle_packet();