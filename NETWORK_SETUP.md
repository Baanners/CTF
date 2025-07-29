# 🌐 Network Traffic Setup Guide

## **Why Traffic Wasn't Visible to Other Users**

The previous version of the network generator was sending traffic to specific IP addresses that might not be reachable or visible to all users on the network. Here's what was fixed:

### **Previous Issues:**

- ❌ Traffic sent only to `192.168.1.1` (router)
- ❌ Single destination for each packet type
- ❌ No broadcast to all network devices
- ❌ Limited DNS server targets

### **New Solutions:**

- ✅ **Automatic network detection** - detects your actual network
- ✅ **Broadcast traffic** - sends to all devices on network
- ✅ **Multiple destinations** - router, DNS servers, broadcast
- ✅ **Dynamic flag system** - flags change every 90 seconds

## **🚀 How to Run the Network Generator**

### **Step 1: Test Network Detection**

```bash
python test_network.py
```

**Expected Output:**

```
🌐 Network Detection Test
========================================
Local IP: 192.168.8.24
Broadcast IP: 192.168.8.255
Router IP: 192.168.8.1
Network Prefix: 192.168.8

📡 Traffic will be sent to:
• Broadcast: 192.168.8.255 (all devices)
• Router: 192.168.8.1
• Google DNS: 8.8.8.8
• Cloudflare DNS: 1.1.1.1
• OpenDNS: 208.67.222.222

✅ All users on the same network should see this traffic!
```

### **Step 2: Run the Network Generator**

```bash
python network_generator.py
```

**Expected Output:**

```
🎯 CTF Network Traffic Generator
========================================
This script generates the network traffic needed for CTF challenges.
Users must capture this traffic with Wireshark to find the flags.
========================================
🌐 Detected network: {'local_ip': '192.168.8.24', 'broadcast_ip': '192.168.8.255', 'router_ip': '192.168.8.1', 'network_prefix': '192.168.8'}

🚀 Starting CTF Network Traffic Generator...
📡 Generating traffic for all challenges...
==================================================

⏰ 14:30:15 - Generating traffic (Cycle 1)...
[HTTP] Sent flag to multiple destinations: CTF{HTTP_H3AD3R_FL4G}
[DNS] Sent flag to multiple DNS servers: CTF{DNS_3XF1LTR4T10N}
[FTP] Sent flag to multiple destinations: CTF{FTP_CR3D3NT14LS}
[ICMP] Sent flag to multiple destinations: CTF{1CMP_C0V3RT_CH4NN3L}
[ARP] Sent flag via broadcast: CTF{ARP_SP00F1NG_D3T3CT3D}
[TCP] Sent flag to multiple destinations: CTF{TCP_STR34M_FL4G}
[CAESAR1] Sent: FWI{HDV\FDHVDU_RQH}
[CAESAR2] Sent: FWI{HDV\FDHVDU_WZR}
[CAESAR3] Sent: FWI{HDV\FDHVDU_WKUHH}
[PLAINTEXT] Sent: CTF{EASY_PLAINTEXT}
[EASY_DNS_FLAG] Sent: CTF{EASY_DNS_FLAG}
✅ All traffic generated. Waiting 30 seconds before next cycle...
```

## **📡 What Traffic is Generated**

### **1. HTTP Traffic (Challenge 1)**

- **Destination**: Broadcast + Router + DNS servers
- **Port**: 80
- **Flag Location**: User-Agent header (base64 encoded)
- **Wireshark Filter**: `http`

### **2. DNS Traffic (Challenge 2)**

- **Destination**: Multiple DNS servers (8.8.8.8, 1.1.1.1, 208.67.222.222)
- **Port**: 53
- **Flag Location**: Subdomain query
- **Wireshark Filter**: `dns`

### **3. FTP Traffic (Challenge 3)**

- **Destination**: Broadcast + Router + DNS servers
- **Port**: 21
- **Flag Location**: Password field
- **Wireshark Filter**: `ftp`

### **4. ICMP Traffic (Challenge 4)**

- **Destination**: Broadcast + Router + DNS servers
- **Flag Location**: Payload (hex encoded)
- **Wireshark Filter**: `icmp`

### **5. ARP Traffic (Challenge 5)**

- **Destination**: Broadcast to all devices
- **Flag Location**: Payload (hex encoded)
- **Wireshark Filter**: `arp`

### **6. TCP Traffic (Challenge 6)**

- **Destination**: Broadcast + Router + DNS servers
- **Port**: 80
- **Flag Location**: Payload (hex encoded)
- **Wireshark Filter**: `tcp`

### **7-9. Caesar Cipher Challenges**

- **Challenge 7**: TCP port 1337, shift 3, marker 'CAESAR1'
- **Challenge 8**: UDP port 4242, shift 5, marker 'CAESAR2'
- **Challenge 9**: ICMP, shift 7, marker 'CAESAR3'

### **10-11. Easy Challenges**

- **Challenge 10**: TCP port 2024, marker 'PLAINTEXT'
- **Challenge 11**: DNS query with subdomain

## **🔄 Dynamic Flag System**

### **Flag Progression:**

Every 3 cycles (90 seconds), all flags automatically advance:

**HTTP Challenge Example:**

1. `CTF{HTTP_H3AD3R_FL4G}` (original)
2. `CTF{HTTP_ST0L3N_FL4G}` (after first steal)
3. `CTF{HTTP_N3W_FL4G}` (after second steal)
4. `CTF{HTTP_R3ST0L3N_FL4G}` (after third steal)
5. `CTF{HTTP_F1N4L_FL4G}` (after fourth steal)

### **Stealing System:**

- ✅ Flags change automatically every 90 seconds
- ✅ Users must capture current flag from network traffic
- ✅ Old flags become invalid after advancement
- ✅ Creates dynamic attack/defense gameplay

## **🔧 Troubleshooting**

### **If Users Still Can't See Traffic:**

1. **Check Network Detection:**

   ```bash
   python test_network.py
   ```

2. **Verify All Users Are on Same Network:**

   - Same Wi-Fi network or hotspot
   - Same subnet (e.g., 192.168.8.x)

3. **Check Wireshark Settings:**

   - Capture on correct interface (Wi-Fi, not loopback)
   - Promiscuous mode enabled
   - No filters applied initially

4. **Test Specific Challenge:**
   ```bash
   python network_generator.py
   # Then in another terminal:
   python -c "from network_generator import CTFNetworkGenerator; g = CTFNetworkGenerator(); g.generate_specific_challenge(1)"
   ```

### **Common Issues:**

**Issue**: "No traffic visible in Wireshark"
**Solution**: Ensure you're capturing on the Wi-Fi interface, not loopback

**Issue**: "Only some traffic visible"
**Solution**: Check firewall settings, some packets might be blocked

**Issue**: "Flags not changing"
**Solution**: Wait 90 seconds for automatic flag advancement

## **✅ Success Indicators**

When working correctly, you should see:

1. **Network Detection**: Shows your actual network IPs
2. **Multiple Destinations**: Traffic sent to broadcast + router + DNS
3. **Regular Cycles**: Traffic generated every 30 seconds
4. **Flag Advancement**: Flags change every 3 cycles (90 seconds)
5. **All Users See Traffic**: Everyone on same network can capture packets

## **🎯 Final Notes**

- **Run the network generator on the host machine** (the one sharing the hotspot/network)
- **All users must be on the same local network**
- **Wireshark must capture on the correct network interface**
- **Traffic is sent every 30 seconds** with flags changing every 90 seconds
- **Broadcast packets ensure all devices see the traffic**

This setup ensures that all users on the same network can capture the CTF traffic and participate in the competition!
