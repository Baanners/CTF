#!/usr/bin/env python3
"""
Network Traffic Generator for CTF Challenges
This script generates the actual network traffic that users need to capture with Wireshark.
Run this script on the same network where users are competing.
"""

import socket
import struct
import time
import threading
import base64
import binascii
from scapy.all import *

class CTFNetworkGenerator:
    def __init__(self):
        # Detect network interface and broadcast address
        self.network_info = self.detect_network()
        print(f"🌐 Detected network: {self.network_info}")
        
        # Initial flags - these will be updated based on game state
        self.flags = {
            "http": "CTF{HTTP_H3AD3R_FL4G}",
            "dns": "CTF{DNS_3XF1LTR4T10N}",
            "ftp": "CTF{FTP_CR3D3NT14LS}",
            "icmp": "CTF{1CMP_C0V3RT_CH4NN3L}",
            "arp": "CTF{ARP_SP00F1NG_D3T3CT3D}",
            "tcp": "CTF{TCP_STR34M_FL4G}",
            "caesar1": "CTF{EASY_CAESAR_ONE}",
            "caesar2": "CTF{EASY_CAESAR_TWO}",
            "caesar3": "CTF{EASY_CAESAR_THREE}",
            "plaintext": "CTF{EASY_PLAINTEXT}",
            "easydns": "CTF{EASY_DNS_FLAG}"
        }
        
        # Alternative flags for different steal states
        self.flag_variations = {
            "http": [
                "CTF{HTTP_H3AD3R_FL4G}",
                "CTF{HTTP_ST0L3N_FL4G}",
                "CTF{HTTP_N3W_FL4G}",
                "CTF{HTTP_R3ST0L3N_FL4G}",
                "CTF{HTTP_F1N4L_FL4G}"
            ],
            "dns": [
                "CTF{DNS_3XF1LTR4T10N}",
                "CTF{DNS_ST0L3N_FL4G}",
                "CTF{DNS_N3W_FL4G}",
                "CTF{DNS_R3ST0L3N_FL4G}",
                "CTF{DNS_F1N4L_FL4G}"
            ],
            "ftp": [
                "CTF{FTP_CR3D3NT14LS}",
                "CTF{FTP_ST0L3N_FL4G}",
                "CTF{FTP_N3W_FL4G}",
                "CTF{FTP_R3ST0L3N_FL4G}",
                "CTF{FTP_F1N4L_FL4G}"
            ],
            "icmp": [
                "CTF{1CMP_C0V3RT_CH4NN3L}",
                "CTF{1CMP_ST0L3N_FL4G}",
                "CTF{1CMP_N3W_FL4G}",
                "CTF{1CMP_R3ST0L3N_FL4G}",
                "CTF{1CMP_F1N4L_FL4G}"
            ],
            "arp": [
                "CTF{ARP_SP00F1NG_D3T3CT3D}",
                "CTF{ARP_ST0L3N_FL4G}",
                "CTF{ARP_N3W_FL4G}",
                "CTF{ARP_R3ST0L3N_FL4G}",
                "CTF{ARP_F1N4L_FL4G}"
            ],
            "tcp": [
                "CTF{TCP_STR34M_FL4G}",
                "CTF{TCP_ST0L3N_FL4G}",
                "CTF{TCP_N3W_FL4G}",
                "CTF{TCP_R3ST0L3N_FL4G}",
                "CTF{TCP_F1N4L_FL4G}"
            ],
            "caesar1": [
                "CTF{EASY_CAESAR_ONE}",
                "CTF{EASY_ST0L3N_ONE}",
                "CTF{EASY_N3W_ONE}",
                "CTF{EASY_R3ST0L3N_ONE}",
                "CTF{EASY_F1N4L_ONE}"
            ],
            "caesar2": [
                "CTF{EASY_CAESAR_TWO}",
                "CTF{EASY_ST0L3N_TWO}",
                "CTF{EASY_N3W_TWO}",
                "CTF{EASY_R3ST0L3N_TWO}",
                "CTF{EASY_F1N4L_TWO}"
            ],
            "caesar3": [
                "CTF{EASY_CAESAR_THREE}",
                "CTF{EASY_ST0L3N_THREE}",
                "CTF{EASY_N3W_THREE}",
                "CTF{EASY_R3ST0L3N_THREE}",
                "CTF{EASY_F1N4L_THREE}"
            ],
            "plaintext": [
                "CTF{EASY_PLAINTEXT}",
                "CTF{EASY_ST0L3N_TEXT}",
                "CTF{EASY_N3W_TEXT}",
                "CTF{EASY_R3ST0L3N_TEXT}",
                "CTF{EASY_F1N4L_TEXT}"
            ],
            "easydns": [
                "CTF{EASY_DNS_FLAG}",
                "CTF{EASY_ST0L3N_DNS}",
                "CTF{EASY_N3W_DNS}",
                "CTF{EASY_R3ST0L3N_DNS}",
                "CTF{EASY_F1N4L_DNS}"
            ]
        }
        
        # Track current flag index for each challenge
        self.current_flag_index = {
            "http": 0,
            "dns": 0,
            "ftp": 0,
            "icmp": 0,
            "arp": 0,
            "tcp": 0,
            "caesar1": 0,
            "caesar2": 0,
            "caesar3": 0,
            "plaintext": 0,
            "easydns": 0
        }
    
    def detect_network(self):
        """Detect the current network interface and broadcast address"""
        try:
            # Get the default gateway (router IP)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            # Extract network prefix (assuming /24 subnet)
            network_prefix = '.'.join(local_ip.split('.')[:-1])
            broadcast_ip = f"{network_prefix}.255"
            router_ip = f"{network_prefix}.1"
            
            return {
                "local_ip": local_ip,
                "broadcast_ip": broadcast_ip,
                "router_ip": router_ip,
                "network_prefix": network_prefix
            }
        except Exception as e:
            print(f"⚠️  Network detection failed: {e}")
            # Fallback to common network addresses
            return {
                "local_ip": "192.168.1.100",
                "broadcast_ip": "192.168.1.255",
                "router_ip": "192.168.1.1",
                "network_prefix": "192.168.1"
            }
        
    def get_current_flag(self, challenge_type):
        """Get the current flag for a challenge type"""
        if challenge_type in self.flag_variations:
            index = self.current_flag_index[challenge_type]
            return self.flag_variations[challenge_type][index]
        return self.flags.get(challenge_type, "FLAG_NOT_FOUND")
    
    def advance_flag(self, challenge_type):
        """Advance to the next flag for a challenge type (called when stolen)"""
        if challenge_type in self.current_flag_index:
            self.current_flag_index[challenge_type] = min(
                self.current_flag_index[challenge_type] + 1,
                len(self.flag_variations[challenge_type]) - 1
            )
            print(f"[FLAG UPDATE] {challenge_type} flag advanced to: {self.get_current_flag(challenge_type)}")
    
    def generate_http_traffic(self):
        """Generate HTTP traffic with flag in User-Agent header using raw packets"""
        flag = self.get_current_flag("http")
        encoded_flag = base64.b64encode(flag.encode()).decode()
        
        # Create HTTP request as raw packet
        http_request = f"""GET /secret HTTP/1.1
Host: ctf-challenge.local
User-Agent: {encoded_flag}
Accept: */*
Connection: close

"""
        
        # Send HTTP packet using scapy to make it visible on network
        try:
            # Send to multiple destinations to ensure visibility
            destinations = [
                self.network_info["broadcast_ip"],  # Broadcast to all devices
                self.network_info["router_ip"],     # Router
                "8.8.8.8",                          # Google DNS
                "1.1.1.1"                           # Cloudflare DNS
            ]
            
            for dst in destinations:
                try:
                    http_packet = IP(dst=dst)/TCP(dport=80)/Raw(load=http_request)
                    send(http_packet, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[HTTP] Error sending to {dst}: {e}")
            
            print(f"[HTTP] Sent flag to multiple destinations: {flag}")
        except Exception as e:
            print(f"[HTTP] Error sending packet: {e}")
    
    def generate_dns_traffic(self):
        """Generate DNS traffic with flag in subdomain"""
        flag = self.get_current_flag("dns")
        hex_flag = binascii.hexlify(flag.encode()).decode()
        
        # Create DNS query with flag in subdomain
        dns_query = f"{hex_flag}.ctf-challenge.local"
        
        # Send DNS query using scapy
        try:
            # Send to multiple DNS servers for better visibility
            dns_servers = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
            
            for dns_server in dns_servers:
                try:
                    dns_packet = IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=dns_query))
                    send(dns_packet, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[DNS] Error sending to {dns_server}: {e}")
            
            print(f"[DNS] Sent flag to multiple DNS servers: {flag}")
        except Exception as e:
            print(f"[DNS] Error sending packet: {e}")
    
    def generate_ftp_traffic(self):
        """Generate FTP traffic with flag in password using raw packets"""
        flag = self.get_current_flag("ftp")
        
        ftp_commands = [
            f"USER admin\r\n",
            f"PASS {flag}\r\n"
        ]
        
        # Send FTP commands as raw packets
        try:
            destinations = [
                self.network_info["broadcast_ip"],
                self.network_info["router_ip"],
                "8.8.8.8"
            ]
            
            for dst in destinations:
                for cmd in ftp_commands:
                    try:
                        ftp_packet = IP(dst=dst)/TCP(dport=21)/Raw(load=cmd)
                        send(ftp_packet, verbose=False)
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"[FTP] Error sending to {dst}: {e}")
            
            print(f"[FTP] Sent flag to multiple destinations: {flag}")
        except Exception as e:
            print(f"[FTP] Error sending packet: {e}")
    
    def generate_icmp_traffic(self):
        """Generate ICMP traffic with flag in payload"""
        flag = self.get_current_flag("icmp")
        hex_flag = binascii.hexlify(flag.encode()).decode()
        
        # Send ICMP packet with flag in payload
        try:
            destinations = [
                self.network_info["broadcast_ip"],
                self.network_info["router_ip"],
                "8.8.8.8",
                "1.1.1.1"
            ]
            
            for dst in destinations:
                try:
                    icmp_packet = IP(dst=dst)/ICMP()/Raw(load=hex_flag)
                    send(icmp_packet, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[ICMP] Error sending to {dst}: {e}")
            
            print(f"[ICMP] Sent flag to multiple destinations: {flag}")
        except Exception as e:
            print(f"[ICMP] Error sending packet: {e}")
    
    def generate_arp_traffic(self):
        """Generate ARP traffic with flag in payload"""
        flag = self.get_current_flag("arp")
        hex_flag = binascii.hexlify(flag.encode()).decode()
        
        # Send ARP packet with flag in payload
        try:
            # ARP broadcast to all devices on network
            arp_packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(
                op=1, 
                psrc=self.network_info["local_ip"], 
                pdst=self.network_info["broadcast_ip"]
            )/Raw(load=hex_flag)
            send(arp_packet, verbose=False)
            print(f"[ARP] Sent flag via broadcast: {flag}")
        except Exception as e:
            print(f"[ARP] Error sending packet: {e}")
    
    def generate_tcp_traffic(self):
        """Generate TCP traffic with flag in payload"""
        flag = self.get_current_flag("tcp")
        hex_flag = binascii.hexlify(flag.encode()).decode()
        
        # Send TCP packet with flag in payload
        try:
            destinations = [
                self.network_info["broadcast_ip"],
                self.network_info["router_ip"],
                "8.8.8.8",
                "1.1.1.1"
            ]
            
            for dst in destinations:
                try:
                    tcp_packet = IP(dst=dst)/TCP(dport=80)/Raw(load=hex_flag)
                    send(tcp_packet, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[TCP] Error sending to {dst}: {e}")
            
            print(f"[TCP] Sent flag to multiple destinations: {flag}")
        except Exception as e:
            print(f"[TCP] Error sending packet: {e}")
    
    def generate_caesar_challenges(self):
        # Caesar I: TCP port 1337, shift 3, marker 'CAESAR1'
        flag1 = self.caesar_cipher(self.get_current_flag("caesar1"), 3)
        destinations = [self.network_info["broadcast_ip"], self.network_info["router_ip"], "8.8.8.8"]
        for dst in destinations:
            try:
                pkt1 = IP(dst=dst)/TCP(dport=1337)/Raw(load=f"CAESAR1:{flag1}")
                send(pkt1, verbose=False)
                time.sleep(0.1)
            except Exception as e:
                print(f"[CAESAR1] Error sending to {dst}: {e}")
        print(f"[CAESAR1] Sent: {flag1}")

        # Caesar II: UDP port 4242, shift 5, marker 'CAESAR2'
        flag2 = self.caesar_cipher(self.get_current_flag("caesar2"), 5)
        for dst in destinations:
            try:
                pkt2 = IP(dst=dst)/UDP(dport=4242)/Raw(load=f"CAESAR2:{flag2}")
                send(pkt2, verbose=False)
                time.sleep(0.1)
            except Exception as e:
                print(f"[CAESAR2] Error sending to {dst}: {e}")
        print(f"[CAESAR2] Sent: {flag2}")

        # Caesar III: ICMP, shift 7, marker 'CAESAR3'
        flag3 = self.caesar_cipher(self.get_current_flag("caesar3"), 7)
        for dst in destinations:
            try:
                pkt3 = IP(dst=dst)/ICMP()/Raw(load=f"CAESAR3:{flag3}")
                send(pkt3, verbose=False)
                time.sleep(0.1)
            except Exception as e:
                print(f"[CAESAR3] Error sending to {dst}: {e}")
        print(f"[CAESAR3] Sent: {flag3}")

    def caesar_cipher(self, text, shift):
        result = ''
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result

    def generate_easy_challenges(self):
        # Plaintext Flag: TCP port 2024, marker 'PLAINTEXT'
        flag1 = self.get_current_flag("plaintext")
        destinations = [self.network_info["broadcast_ip"], self.network_info["router_ip"], "8.8.8.8"]
        for dst in destinations:
            try:
                pkt1 = IP(dst=dst)/TCP(dport=2024)/Raw(load=f"PLAINTEXT:{flag1}")
                send(pkt1, verbose=False)
                time.sleep(0.1)
            except Exception as e:
                print(f"[PLAINTEXT] Error sending to {dst}: {e}")
        print(f"[PLAINTEXT] Sent: {flag1}")

        # Easy DNS Flag: subdomain 'easydnsflag'
        flag2 = self.get_current_flag("easydns")
        dns_query = f"easydnsflag.{flag2.lower().replace('{', '').replace('}', '')}.ctf.local"
        dns_servers = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
        for dns_server in dns_servers:
            try:
                pkt2 = IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=dns_query))
                send(pkt2, verbose=False)
                time.sleep(0.1)
            except Exception as e:
                print(f"[EASY_DNS_FLAG] Error sending to {dns_server}: {e}")
        print(f"[EASY_DNS_FLAG] Sent: {flag2}")

    def generate_specific_challenge(self, challenge_id):
        """Generate traffic for a specific challenge only"""
        print(f"Generating traffic for challenge {challenge_id}...")
        
        if challenge_id == 1:
            self.generate_http_traffic()
        elif challenge_id == 2:
            self.generate_dns_traffic()
        elif challenge_id == 3:
            self.generate_ftp_traffic()
        elif challenge_id == 4:
            self.generate_icmp_traffic()
        elif challenge_id == 5:
            self.generate_arp_traffic()
        elif challenge_id == 6:
            self.generate_tcp_traffic()
        elif challenge_id == 7:
            # Caesar I
            flag = self.caesar_cipher(self.get_current_flag("caesar1"), 3)
            destinations = [self.network_info["broadcast_ip"], self.network_info["router_ip"], "8.8.8.8"]
            for dst in destinations:
                try:
                    pkt = IP(dst=dst)/TCP(dport=1337)/Raw(load=f"CAESAR1:{flag}")
                    send(pkt, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[CAESAR1] Error sending to {dst}: {e}")
            print(f"[CAESAR1] Sent: {flag}")
        elif challenge_id == 8:
            # Caesar II
            flag = self.caesar_cipher(self.get_current_flag("caesar2"), 5)
            destinations = [self.network_info["broadcast_ip"], self.network_info["router_ip"], "8.8.8.8"]
            for dst in destinations:
                try:
                    pkt = IP(dst=dst)/UDP(dport=4242)/Raw(load=f"CAESAR2:{flag}")
                    send(pkt, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[CAESAR2] Error sending to {dst}: {e}")
            print(f"[CAESAR2] Sent: {flag}")
        elif challenge_id == 9:
            # Caesar III
            flag = self.caesar_cipher(self.get_current_flag("caesar3"), 7)
            destinations = [self.network_info["broadcast_ip"], self.network_info["router_ip"], "8.8.8.8"]
            for dst in destinations:
                try:
                    pkt = IP(dst=dst)/ICMP()/Raw(load=f"CAESAR3:{flag}")
                    send(pkt, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[CAESAR3] Error sending to {dst}: {e}")
            print(f"[CAESAR3] Sent: {flag}")
        elif challenge_id == 10:
            # Plaintext
            flag = self.get_current_flag("plaintext")
            destinations = [self.network_info["broadcast_ip"], self.network_info["router_ip"], "8.8.8.8"]
            for dst in destinations:
                try:
                    pkt = IP(dst=dst)/TCP(dport=2024)/Raw(load=f"PLAINTEXT:{flag}")
                    send(pkt, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[PLAINTEXT] Error sending to {dst}: {e}")
            print(f"[PLAINTEXT] Sent: {flag}")
        elif challenge_id == 11:
            # Easy DNS
            flag = self.get_current_flag("easydns")
            dns_query = f"easydnsflag.{flag.lower().replace('{', '').replace('}', '')}.ctf.local"
            dns_servers = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
            for dns_server in dns_servers:
                try:
                    pkt = IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=dns_query))
                    send(pkt, verbose=False)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[EASY_DNS_FLAG] Error sending to {dns_server}: {e}")
            print(f"[EASY_DNS_FLAG] Sent: {flag}")
        else:
            print(f"Unknown challenge ID: {challenge_id}")

    def run_all_traffic(self):
        """Generate all types of network traffic"""
        print("🚀 Starting CTF Network Traffic Generator...")
        print("📡 Generating traffic for all challenges...")
        print("=" * 50)
        cycle_count = 0
        while True:
            cycle_count += 1
            print(f"\n⏰ {time.strftime('%H:%M:%S')} - Generating traffic (Cycle {cycle_count})...")
            
            # Automatically advance flags every 3 cycles (90 seconds)
            if cycle_count % 3 == 0:
                print("🔄 Advancing all flags for dynamic gameplay...")
                for challenge_type in self.current_flag_index.keys():
                    self.advance_flag(challenge_type)
            
            self.generate_http_traffic()
            time.sleep(2)
            self.generate_dns_traffic()
            time.sleep(2)
            self.generate_ftp_traffic()
            time.sleep(2)
            self.generate_icmp_traffic()
            time.sleep(2)
            self.generate_arp_traffic()
            time.sleep(2)
            self.generate_tcp_traffic()
            time.sleep(2)
            self.generate_caesar_challenges()
            time.sleep(2)
            self.generate_easy_challenges()
            time.sleep(2)
            print("✅ All traffic generated. Waiting 30 seconds before next cycle...")
            time.sleep(30)

def main():
    print("🎯 CTF Network Traffic Generator")
    print("=" * 40)
    print("This script generates the network traffic needed for CTF challenges.")
    print("Users must capture this traffic with Wireshark to find the flags.")
    print("=" * 40)
    
    generator = CTFNetworkGenerator()
    
    try:
        generator.run_all_traffic()
    except KeyboardInterrupt:
        print("\n🛑 Traffic generation stopped by user.")
        print("Thanks for using CTF Network Traffic Generator!")

if __name__ == "__main__":
    main() 