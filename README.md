# Network CTF Challenge Website

A real-time competitive Capture The Flag (CTF) website designed for network analysis challenges using Wireshark. Multiple users can compete simultaneously to capture flags through **real network packet analysis** - just like picoCTF!

## 🚀 Features

- **Real Network Analysis**: Users must capture actual network traffic with Wireshark
- **Real-time Competition**: Multiple users can compete simultaneously
- **Challenge Locking**: Only one user can attempt a challenge at a time
- **Live Leaderboard**: Track scores and flag captures in real-time
- **Wireshark Integration**: Real packet analysis challenges
- **Modern UI**: Beautiful, responsive design with dark theme
- **GitHub Pages Ready**: Easy deployment for team access

## 🎯 How It Works

1. **Join Competition**: Enter your username to join the CTF
2. **Select Challenges**: Choose from 6 different network analysis challenges
3. **Start Wireshark**: Begin packet capture to analyze **real network traffic**
4. **Capture Flags**: Find hidden flags in actual network packets
5. **Compete**: Race against other team members to capture flags first

## 📋 Prerequisites

- **Wireshark**: Download and install [Wireshark](https://www.wireshark.org/) for packet analysis
- **Network Access**: All team members need access to the same network (hotspot/local network)
- **Modern Browser**: Chrome, Firefox, Safari, or Edge
- **Local Network**: All users must be on the same local network to capture shared traffic

## 🛠️ Setup Instructions

### 1. Local Development

1. Clone or download the project files:

   ```
   index.html
   styles.css
   script.js
   README.md
   ```

2. Open `index.html` in your web browser

3. Start the CTF competition!

### 2. GitHub Pages Deployment

1. Create a new GitHub repository
2. Upload all project files to the repository
3. Go to Settings → Pages
4. Select "Deploy from a branch" and choose "main"
5. Your CTF website will be available at: `https://yourusername.github.io/repository-name`

### 3. Team Access

- Share the GitHub Pages URL with your team members
- All members can access the website simultaneously
- **All users must be on the same local network** to capture shared traffic
- Real-time updates will be visible to all participants

## 🎮 Challenge Types

### 1. HTTP Traffic Analysis (Easy - 100 pts)

- **Objective**: Find hidden flags in HTTP request headers
- **Wireshark Filter**: `http`
- **Real Task**: Capture HTTP GET request to '/secret' with base64 encoded User-Agent
- **Look for**: Suspicious User-Agent strings, base64 encoded data

### 2. DNS Exfiltration (Medium - 200 pts)

- **Objective**: Analyze DNS queries for data exfiltration
- **Wireshark Filter**: `dns`
- **Real Task**: Find DNS query with hex-encoded data in subdomain
- **Look for**: Long subdomain names, hex encoding

### 3. FTP Credential Capture (Medium - 250 pts)

- **Objective**: Intercept FTP traffic for credentials
- **Wireshark Filter**: `ftp`
- **Real Task**: Capture FTP login with flag hidden in password field
- **Look for**: Plaintext passwords, authentication data

### 4. ICMP Covert Channel (Hard - 400 pts)

- **Objective**: Find hidden data in ICMP echo requests
- **Wireshark Filter**: `icmp`
- **Real Task**: Find ICMP packet with flag embedded in payload
- **Look for**: Hex patterns in payload

### 5. ARP Spoofing Detection (Hard - 500 pts)

- **Objective**: Detect malicious ARP spoofing attempts
- **Wireshark Filter**: `arp`
- **Real Task**: Detect ARP spoofing with flag in response
- **Look for**: Duplicate IP addresses, suspicious MAC addresses

### 6. TCP Stream Analysis (Medium - 300 pts)

- **Objective**: Analyze TCP streams for hidden flags
- **Wireshark Filter**: `tcp`
- **Real Task**: Find TCP stream with flag in payload
- **Look for**: Magic bytes, specific byte patterns

## 🔧 Wireshark Setup

### Basic Setup

1. Open Wireshark
2. Select your network interface (WiFi/Ethernet)
3. Start packet capture
4. Apply the appropriate filter for each challenge

### Advanced Filters

- **HTTP**: `http`
- **DNS**: `dns`
- **FTP**: `ftp`
- **ICMP**: `icmp`
- **ARP**: `arp`
- **TCP**: `tcp`

### Tips for Packet Analysis

- Use "Follow TCP Stream" for HTTP/FTP analysis
- Look for unusual packet sizes or patterns
- Check packet payloads for encoded data
- Monitor for suspicious IP addresses
- **All team members must capture the same network traffic**

## 🏆 Competition Rules

1. **Challenge Locking**: Only one user can attempt a challenge at a time
2. **First Come, First Serve**: First user to start a challenge gets exclusive access
3. **Flag Submission**: Submit flags in the format `CTF{...}`
4. **Points System**: Different challenges award different point values
5. **Real-time Updates**: Leaderboard updates automatically
6. **Real Network Traffic**: You must capture actual packets with Wireshark

## 🎨 Customization

### Adding New Challenges

Edit the `challenges` array in `script.js`:

```javascript
{
    id: 7,
    title: "Your Challenge Title",
    description: "Real network analysis task...",
    difficulty: "easy", // easy, medium, hard
    flag: "CTF{YOUR_FLAG_HERE}",
    hints: ["Hint 1", "Hint 2"],
    category: "Network Analysis",
    points: 150,
    trafficType: "http",
    requiredAction: "Capture specific network traffic"
}
```

### Modifying Styles

Edit `styles.css` to customize:

- Color scheme
- Layout
- Animations
- Responsive design

## 🔒 Security Notes

- This is a demonstration system for educational purposes
- Flags are stored in plain text for demo purposes
- In production, implement proper authentication and server-side validation
- Consider using WebSockets for real-time updates
- **All users must be on the same local network to capture shared traffic**

## 🐛 Troubleshooting

### Common Issues

1. **Wireshark not detecting packets**

   - Check network interface selection
   - Ensure you have proper permissions
   - Try running as administrator
   - **Verify all users are on the same network**

2. **Website not loading**

   - Check file paths
   - Ensure all files are in the same directory
   - Try a different browser

3. **Real-time updates not working**

   - Refresh the page
   - Check browser console for errors
   - Ensure JavaScript is enabled

4. **Can't capture network traffic**
   - Ensure all team members are on the same local network
   - Check Wireshark interface selection
   - Verify network permissions

## 📞 Support

For issues or questions:

1. Check the browser console for error messages
2. Verify all files are present and properly linked
3. Test with different browsers
4. Ensure Wireshark is properly installed
5. **Confirm all users are on the same local network**

## 🎯 Learning Objectives

This CTF helps develop:

- **Real network analysis skills**
- **Packet capture and analysis**
- **Protocol understanding (HTTP, DNS, FTP, etc.)**
- **Real-time problem solving**
- **Competitive cybersecurity mindset**
- **Wireshark proficiency**

## 📝 License

This project is open source and available for educational purposes.

---

**Happy Hacking! 🚀**

**Remember: You must capture REAL network traffic with Wireshark to find the flags!**
