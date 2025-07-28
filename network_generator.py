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
        
    def generate_http_traffic(self):
        """Generate HTTP traffic with flag in User-Agent header using raw packets"""
        flag = self.flags["http"]
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
            # Send to your router's IP (usually 192.168.1.1 or 192.168.0.1)
            # This will go through your Wi-Fi interface
            http_packet = IP(dst="192.168.1.1")/TCP(dport=80)/Raw(load=http_request)
            send(http_packet, verbose=False)
            print(f"[HTTP] Sent flag: {flag}")
        except Exception as e:
            print(f"[HTTP] Error sending packet: {e}")
    
    def generate_dns_traffic(self):
        """Generate DNS traffic with flag in subdomain"""
        flag = self.flags["dns"]
        hex_flag = binascii.hexlify(flag.encode()).decode()
        
        # Create DNS query with flag in subdomain
        dns_query = f"{hex_flag}.ctf-challenge.local"
        
        # Send DNS query using scapy
        try:
            dns_packet = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=dns_query))
            send(dns_packet, verbose=False)
            print(f"[DNS] Sent flag: {flag}")
        except Exception as e:
            print(f"[DNS] Error sending packet: {e}")
    
    def generate_ftp_traffic(self):
        """Generate FTP traffic with flag in password using raw packets"""
        flag = self.flags["ftp"]
        
        ftp_commands = [
            f"USER admin\r\n",
            f"PASS {flag}\r\n"
        ]
        
        # Send FTP commands as raw packets
        try:
            for cmd in ftp_commands:
                ftp_packet = IP(dst="192.168.1.1")/TCP(dport=21)/Raw(load=cmd)
                send(ftp_packet, verbose=False)
                time.sleep(0.1)
            print(f"[FTP] Sent flag: {flag}")
        except Exception as e:
            print(f"[FTP] Error sending packet: {e}")
    
    def generate_icmp_traffic(self):
        """Generate ICMP traffic with flag in payload"""
        flag = self.flags["icmp"]
        hex_flag = binascii.hexlify(flag.encode()).decode()
        
        # Send ICMP packet with flag in payload
        try:
            icmp_packet = IP(dst="192.168.1.1")/ICMP()/Raw(load=hex_flag)
            send(icmp_packet, verbose=False)
            print(f"[ICMP] Sent flag: {flag}")
        except Exception as e:
            print(f"[ICMP] Error sending packet: {e}")
    
    def generate_arp_traffic(self):
        """Generate ARP traffic with flag in payload"""
        flag = self.flags["arp"]
        hex_flag = binascii.hexlify(flag.encode()).decode()
        
        # Send ARP packet with flag in payload
        try:
            arp_packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, psrc="192.168.1.100", pdst="192.168.1.200")/Raw(load=hex_flag)
            send(arp_packet, verbose=False)
            print(f"[ARP] Sent flag: {flag}")
        except Exception as e:
            print(f"[ARP] Error sending packet: {e}")
    
    def generate_tcp_traffic(self):
        """Generate TCP traffic with flag in payload"""
        flag = self.flags["tcp"]
        hex_flag = binascii.hexlify(flag.encode()).decode()
        
        # Send TCP packet with flag in payload
        try:
            tcp_packet = IP(dst="192.168.1.1")/TCP(dport=80)/Raw(load=hex_flag)
            send(tcp_packet, verbose=False)
            print(f"[TCP] Sent flag: {flag}")
        except Exception as e:
            print(f"[TCP] Error sending packet: {e}")
    
    def generate_caesar_challenges(self):
        # Caesar I: TCP port 1337, shift 3, marker 'CAESAR1'
        flag1 = self.caesar_cipher("CTF{EASY_CAESAR_ONE}", 3)
        pkt1 = IP(dst="192.168.1.1")/TCP(dport=1337)/Raw(load=f"CAESAR1:{flag1}")
        send(pkt1, verbose=False)
        print(f"[CAESAR1] Sent: {flag1}")

        # Caesar II: UDP port 4242, shift 5, marker 'CAESAR2'
        flag2 = self.caesar_cipher("CTF{EASY_CAESAR_TWO}", 5)
        pkt2 = IP(dst="192.168.1.1")/UDP(dport=4242)/Raw(load=f"CAESAR2:{flag2}")
        send(pkt2, verbose=False)
        print(f"[CAESAR2] Sent: {flag2}")

        # Caesar III: ICMP, shift 7, marker 'CAESAR3'
        flag3 = self.caesar_cipher("CTF{EASY_CAESAR_THREE}", 7)
        pkt3 = IP(dst="192.168.1.1")/ICMP()/Raw(load=f"CAESAR3:{flag3}")
        send(pkt3, verbose=False)
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
        pkt1 = IP(dst="192.168.1.1")/TCP(dport=2024)/Raw(load="PLAINTEXT:CTF{EASY_PLAINTEXT}")
        send(pkt1, verbose=False)
        print("[PLAINTEXT] Sent: CTF{EASY_PLAINTEXT}")

        # Easy DNS Flag: subdomain 'easydnsflag'
        dns_query = "easydnsflag.ctf.local"
        pkt2 = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=dns_query))
        send(pkt2, verbose=False)
        print("[EASY_DNS_FLAG] Sent: CTF{EASY_DNS_FLAG}")

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
            flag = self.caesar_cipher("CTF{EASY_CAESAR_ONE}", 3)
            pkt = IP(dst="192.168.1.1")/TCP(dport=1337)/Raw(load=f"CAESAR1:{flag}")
            send(pkt, verbose=False)
            print(f"[CAESAR1] Sent: {flag}")
        elif challenge_id == 8:
            # Caesar II
            flag = self.caesar_cipher("CTF{EASY_CAESAR_TWO}", 5)
            pkt = IP(dst="192.168.1.1")/UDP(dport=4242)/Raw(load=f"CAESAR2:{flag}")
            send(pkt, verbose=False)
            print(f"[CAESAR2] Sent: {flag}")
        elif challenge_id == 9:
            # Caesar III
            flag = self.caesar_cipher("CTF{EASY_CAESAR_THREE}", 7)
            pkt = IP(dst="192.168.1.1")/ICMP()/Raw(load=f"CAESAR3:{flag}")
            send(pkt, verbose=False)
            print(f"[CAESAR3] Sent: {flag}")
        elif challenge_id == 10:
            # Plaintext
            pkt = IP(dst="192.168.1.1")/TCP(dport=2024)/Raw(load="PLAINTEXT:CTF{EASY_PLAINTEXT}")
            send(pkt, verbose=False)
            print("[PLAINTEXT] Sent: CTF{EASY_PLAINTEXT}")
        elif challenge_id == 11:
            # Easy DNS
            dns_query = "easydnsflag.ctf.local"
            pkt = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=dns_query))
            send(pkt, verbose=False)
            print("[EASY_DNS_FLAG] Sent: CTF{EASY_DNS_FLAG}")
        else:
            print(f"Unknown challenge ID: {challenge_id}")

    def run_all_traffic(self):
        """Generate all types of network traffic"""
        print("🚀 Starting CTF Network Traffic Generator...")
        print("📡 Generating traffic for all challenges...")
        print("=" * 50)
        while True:
            print(f"\n⏰ {time.strftime('%H:%M:%S')} - Generating traffic...")
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