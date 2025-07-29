#!/usr/bin/env python3
"""
Test script to verify network detection and show what IP addresses will be used
"""

import socket

def detect_network():
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

if __name__ == "__main__":
    print("🌐 Network Detection Test")
    print("=" * 40)
    
    network_info = detect_network()
    
    print(f"Local IP: {network_info['local_ip']}")
    print(f"Broadcast IP: {network_info['broadcast_ip']}")
    print(f"Router IP: {network_info['router_ip']}")
    print(f"Network Prefix: {network_info['network_prefix']}")
    
    print("\n📡 Traffic will be sent to:")
    print(f"• Broadcast: {network_info['broadcast_ip']} (all devices)")
    print(f"• Router: {network_info['router_ip']}")
    print(f"• Google DNS: 8.8.8.8")
    print(f"• Cloudflare DNS: 1.1.1.1")
    print(f"• OpenDNS: 208.67.222.222")
    
    print("\n✅ All users on the same network should see this traffic!") 