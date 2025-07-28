# GitHub Pages Deployment Guide

## Quick Setup for CTF Website

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., `ctf-challenge-website`)
5. Make it **Public** (required for GitHub Pages)
6. Click "Create repository"

### Step 2: Upload Files

1. In your new repository, click "uploading an existing file"
2. Drag and drop these files into the upload area:
   - `index.html`
   - `styles.css`
   - `script.js`
   - `README.md`
   - `network_generator.py`
   - `requirements.txt`
3. Add a commit message: "Initial CTF website upload"
4. Click "Commit changes"

### Step 3: Enable GitHub Pages

1. Go to your repository's **Settings** tab
2. Scroll down to "Pages" in the left sidebar
3. Under "Source", select "Deploy from a branch"
4. Choose "main" branch
5. Click "Save"

### Step 4: Access Your Website

1. Wait 2-3 minutes for deployment
2. Your website will be available at:
   ```
   https://yourusername.github.io/repository-name
   ```
3. Share this URL with your team members

## 🚀 Network Traffic Setup

### For Real CTF Challenges:

The CTF requires **real network traffic** to be captured with Wireshark. To generate this traffic:

1. **Install Python Requirements:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Network Traffic Generator:**

   ```bash
   python network_generator.py
   ```

3. **This will generate:**
   - HTTP traffic with flags in headers
   - DNS queries with encoded data
   - FTP traffic with hidden credentials
   - ICMP packets with flag payloads
   - ARP traffic with spoofed data
   - TCP streams with hidden flags

### Team Setup:

1. **One person runs the traffic generator** on the shared network
2. **All team members connect to the same local network** (hotspot/WiFi)
3. **Each member opens the CTF website** and starts Wireshark
4. **Capture the generated traffic** to find the flags

## Team Access

### For Team Members:

1. Open the GitHub Pages URL in any modern browser
2. Enter your username and click "Join Competition"
3. Start Wireshark and capture network traffic
4. Find flags in the captured packets!

### Network Requirements:

- All team members must be on the same network (hotspot/local network)
- Each member needs Wireshark installed
- Internet connection for the website
- **One person must run the traffic generator**

## Troubleshooting

### If website doesn't load:

1. Check the repository is public
2. Verify all files are uploaded
3. Wait 5-10 minutes for deployment
4. Check the "Actions" tab for deployment status

### If real-time features don't work:

1. Refresh the page
2. Check browser console for errors
3. Try a different browser
4. Ensure JavaScript is enabled

### If network traffic isn't captured:

1. Ensure all users are on the same local network
2. Check Wireshark interface selection
3. Verify the traffic generator is running
4. Check firewall settings

## Customization

### Adding Your Own Challenges:

1. Edit `script.js` in your repository
2. Modify the `challenges` array
3. Update `network_generator.py` to generate new traffic
4. Commit and push changes
5. GitHub Pages will auto-update

### Changing Colors/Design:

1. Edit `styles.css` in your repository
2. Modify CSS variables and styles
3. Commit and push changes

## Security Notes

- This is a demo system for educational purposes
- All data is client-side only
- No server-side validation
- Suitable for local network competitions
- **Network traffic generator creates real packets**

## 🎯 How to Use

### For CTF Organizer:

1. Deploy the website to GitHub Pages
2. Run `python network_generator.py` on the shared network
3. Share the website URL with team members
4. Monitor the competition!

### For CTF Participants:

1. Connect to the shared local network
2. Open the CTF website
3. Start Wireshark capture
4. Look for the generated traffic
5. Find flags in the captured packets
6. Submit flags to score points!

---

**Your CTF website is now ready for real network analysis competitions! 🚀**
