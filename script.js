// In script.js, at the top:
// Firebase configuration will be handled inside the CTFSystem class
// CTF Challenge System - Real Network Analysis with Firebase Realtime
class CTFSystem {
  constructor() {
    this.currentUser = null;
    this.challenges = [];
    this.leaderboard = [];
    this.activeUsers = new Set();
    this.challengeStates = new Map(); // Track challenge status
    this.websocket = null;
    this.isConnected = false;
    this.networkTraffic = new Map(); // Store real network traffic data

    // Firebase configuration
    this.firebaseConfig = {
      apiKey: "AIzaSyCrlgwWQ5QFib3fhdSTBgOMHJqAJVl4fLM",
      authDomain: "wireshark-f1fe7.firebaseapp.com",
      databaseURL:
        "https://wireshark-f1fe7-default-rtdb.asia-southeast1.firebasedatabase.app",
      projectId: "wireshark-f1fe7",
      storageBucket: "wireshark-f1fe7.firebasestorage.app",
      messagingSenderId: "651462050730",
      appId: "1:651462050730:web:4b8e1efff8a9b5a48da1d3",
    };

    // Initialize Firebase
    if (typeof firebase !== "undefined") {
      firebase.initializeApp(this.firebaseConfig);
      this.db = firebase.database();
      this.setupFirebaseListeners();
    } else {
      console.error("Firebase SDK not loaded");
    }

    this.initializeChallenges();
    this.setupEventListeners();
    this.startRealTimeUpdates();
    this.generateNetworkTraffic();
  }

  setupFirebaseListeners() {
    // Listen for real-time updates to leaderboard
    this.db.ref("leaderboard").on("value", (snapshot) => {
      const data = snapshot.val();
      console.log("Firebase leaderboard data received:", data);

      if (data) {
        // Convert Firebase object to array and ensure proper structure
        this.leaderboard = Object.keys(data).map((key) => ({
          username: key,
          ...data[key],
        }));
        console.log("Leaderboard updated:", this.leaderboard);
        this.updateLeaderboard();
      } else {
        this.leaderboard = [];
        console.log("Leaderboard cleared");
        this.updateLeaderboard();
      }
    });

    // Listen for real-time updates to challenge states
    this.db.ref("challenges").on("value", (snapshot) => {
      const data = snapshot.val();
      console.log("Firebase challenges data received:", data);

      if (data) {
        this.challengeStates.clear();
        Object.keys(data).forEach((challengeId) => {
          const state = data[challengeId];
          console.log(`Setting challenge ${challengeId} state:`, state);
          this.challengeStates.set(parseInt(challengeId), state);
        });
        console.log("Updated challenge states:", this.challengeStates);
        this.renderChallenges();
      } else {
        // Initialize challenge states in Firebase if they don't exist
        this.initializeChallengeStates();
      }
    });

    // Listen for real-time updates to active users
    this.db.ref("users").on("value", (snapshot) => {
      const data = snapshot.val();
      if (data) {
        this.activeUsers = new Set(Object.keys(data));
      }
    });
  }

  initializeChallengeStates() {
    // Initialize all challenges as available in Firebase
    this.challenges.forEach((challenge) => {
      this.db.ref(`challenges/${challenge.id}`).set({
        status: "available",
        occupiedBy: null,
        completedBy: null,
        startTime: null,
        score: 0, // Initialize score as 0
      });
    });
  }

  // Add method to reset all users
  resetAllUsers() {
    if (
      confirm(
        "Are you sure you want to reset all users? This will clear all scores and challenge progress."
      )
    ) {
      this.db
        .ref("users")
        .remove()
        .then(() => {
          this.db
            .ref("leaderboard")
            .remove()
            .then(() => {
              this.db
                .ref("challenges")
                .remove()
                .then(() => {
                  this.showNotification(
                    "All users and data have been reset!",
                    "success"
                  );
                  // Re-initialize challenge states
                  this.initializeChallengeStates();
                });
            });
        })
        .catch((error) => {
          console.error("Error resetting users:", error);
          this.showNotification("Error resetting users", "error");
        });
    }
  }

  initializeChallenges() {
    this.challenges = [
      {
        id: 1,
        title: "HTTP Traffic Analysis",
        description:
          "Start Wireshark and capture HTTP traffic. Look for a GET request to '/secret' with a suspicious User-Agent header containing base64 encoded data. Decode the User-Agent to find the flag.",
        difficulty: "easy",
        flag: "CTF{HTTP_H3AD3R_FL4G}",
        hints: [
          "Filter: http",
          "Look for User-Agent header",
          "Base64 decode the User-Agent",
        ],
        category: "Network Analysis",
        points: 100,
        trafficType: "http",
        requiredAction: "Capture HTTP GET request to /secret",
      },
      {
        id: 2,
        title: "DNS Exfiltration",
        description:
          "Monitor DNS queries on your network. Look for unusually long subdomain names that contain hex-encoded data. The flag is hidden in the DNS query data.",
        difficulty: "medium",
        flag: "CTF{DNS_3XF1LTR4T10N}",
        hints: [
          "Filter: dns",
          "Look for long subdomain names",
          "Check for hex patterns",
        ],
        category: "Network Analysis",
        points: 200,
        trafficType: "dns",
        requiredAction: "Find DNS query with hex-encoded data",
      },
      {
        id: 3,
        title: "FTP Credential Capture",
        description:
          "Capture FTP traffic on port 21. Look for plaintext credentials being transmitted. The flag is hidden in the password field of an FTP login attempt.",
        difficulty: "medium",
        flag: "CTF{FTP_CR3D3NT14LS}",
        hints: [
          "Filter: ftp",
          "Monitor port 21",
          "Look for USER and PASS commands",
        ],
        category: "Network Analysis",
        points: 250,
        trafficType: "ftp",
        requiredAction: "Capture FTP login with hidden flag in password",
      },
      {
        id: 4,
        title: "ICMP Covert Channel",
        description:
          "Analyze ICMP echo requests (ping packets). Look for packets with unusual payload sizes or patterns. The flag is embedded in the ICMP payload data.",
        difficulty: "hard",
        flag: "CTF{1CMP_C0V3RT_CH4NN3L}",
        hints: [
          "Filter: icmp",
          "Check payload length",
          "Look for hex patterns in payload",
        ],
        category: "Network Analysis",
        points: 400,
        trafficType: "icmp",
        requiredAction: "Find ICMP packet with flag in payload",
      },
      {
        id: 5,
        title: "ARP Spoofing Detection",
        description:
          "Monitor ARP traffic for spoofing attempts. Look for duplicate IP addresses or suspicious MAC address changes. The flag is in the spoofed ARP response.",
        difficulty: "hard",
        flag: "CTF{ARP_SP00F1NG_D3T3CT3D}",
        hints: [
          "Filter: arp",
          "Look for duplicate IPs",
          "Check MAC address changes",
        ],
        category: "Network Analysis",
        points: 500,
        trafficType: "arp",
        requiredAction: "Detect ARP spoofing with flag in response",
      },
      {
        id: 6,
        title: "TCP Stream Analysis",
        description:
          "Follow TCP streams to find hidden data. Look for specific byte patterns or magic bytes in the TCP payload. The flag is embedded in the stream data.",
        difficulty: "medium",
        flag: "CTF{TCP_STR34M_FL4G}",
        hints: [
          "Filter: tcp",
          "Follow TCP stream",
          "Look for magic bytes 0x435446",
        ],
        category: "Network Analysis",
        points: 300,
        trafficType: "tcp",
        requiredAction: "Find TCP stream with flag in payload",
      },
      // --- New Caesar Cipher Challenges ---
      {
        id: 7,
        title: "Caesar Cipher I (Easy)",
        description:
          "Capture a TCP packet on port 1337. The flag is Caesar-ciphered with a shift of 3. Decode it to get the answer.",
        difficulty: "easy",
        flag: "CTF{EASY_CAESAR_ONE}",
        hints: [
          "Filter: tcp.port == 1337",
          "Look for 'CAESAR1' in the payload",
          "Shift letters back by 3",
        ],
        category: "Crypto",
        points: 50,
        trafficType: "tcp",
        requiredAction:
          "Find and decode the Caesar cipher flag (shift 3) in TCP port 1337",
      },
      {
        id: 8,
        title: "Caesar Cipher II (Easy)",
        description:
          "Capture a UDP packet on port 4242. The flag is Caesar-ciphered with a shift of 5. Decode it to get the answer.",
        difficulty: "easy",
        flag: "CTF{EASY_CAESAR_TWO}",
        hints: [
          "Filter: udp.port == 4242",
          "Look for 'CAESAR2' in the payload",
          "Shift letters back by 5",
        ],
        category: "Crypto",
        points: 50,
        trafficType: "udp",
        requiredAction:
          "Find and decode the Caesar cipher flag (shift 5) in UDP port 4242",
      },
      {
        id: 9,
        title: "Caesar Cipher III (Easy)",
        description:
          "Capture an ICMP packet with a unique string. The flag is Caesar-ciphered with a shift of 7. Decode it to get the answer.",
        difficulty: "easy",
        flag: "CTF{EASY_CAESAR_THREE}",
        hints: [
          "Filter: icmp && frame contains 'CAESAR3'",
          "Shift letters back by 7",
        ],
        category: "Crypto",
        points: 50,
        trafficType: "icmp",
        requiredAction:
          "Find and decode the Caesar cipher flag (shift 7) in ICMP packet",
      },
      // --- More Easy Challenges ---
      {
        id: 10,
        title: "Plaintext Flag (Easy)",
        description:
          "Capture a TCP packet on port 2024. The flag is in plain text in the payload.",
        difficulty: "easy",
        flag: "CTF{EASY_PLAINTEXT}",
        hints: [
          "Filter: tcp.port == 2024",
          "Look for 'PLAINTEXT' in the payload",
        ],
        category: "Network",
        points: 50,
        trafficType: "tcp",
        requiredAction: "Find the plain text flag in TCP port 2024",
      },
      {
        id: 11,
        title: "Easy DNS Flag",
        description:
          "Capture a DNS query with a unique subdomain. The flag is in the subdomain, in plain text.",
        difficulty: "easy",
        flag: "CTF{EASY_DNS_FLAG}",
        hints: [
          "Filter: dns && frame contains 'easydnsflag'",
          "Check the subdomain for the flag",
        ],
        category: "Network",
        points: 50,
        trafficType: "dns",
        requiredAction:
          "Find the flag in a DNS query with subdomain 'easydnsflag'",
      },
    ];

    // Initialize challenge states
    this.challenges.forEach((challenge) => {
      this.challengeStates.set(challenge.id, {
        status: "available", // available, occupied, completed
        occupiedBy: null,
        completedBy: null,
        startTime: null,
      });
    });
  }

  generateNetworkTraffic() {
    // Generate realistic network traffic data that users need to capture
    this.networkTraffic.set(1, {
      packets: [
        {
          time: "10:15:30.123",
          source: "192.168.1.100",
          destination: "10.0.0.50",
          protocol: "HTTP",
          info: "GET /secret HTTP/1.1",
          payload: "User-Agent: Q1RGe0hUVFBfSDNBREVSM19GTDRHfQ==", // Base64 encoded flag
        },
      ],
    });

    this.networkTraffic.set(2, {
      packets: [
        {
          time: "10:16:45.456",
          source: "192.168.1.101",
          destination: "8.8.8.8",
          protocol: "DNS",
          info: "Standard query A CTF7B444E535F334646314C54523454494F4E7D.example.com",
          payload: "Hex encoded flag in subdomain",
        },
      ],
    });

    this.networkTraffic.set(3, {
      packets: [
        {
          time: "10:17:20.789",
          source: "192.168.1.102",
          destination: "192.168.1.1",
          protocol: "FTP",
          info: "USER admin",
          payload: "PASS CTF7B4654505F4352334433543134537D",
        },
      ],
    });

    this.networkTraffic.set(4, {
      packets: [
        {
          time: "10:18:10.012",
          source: "192.168.1.103",
          destination: "192.168.1.1",
          protocol: "ICMP",
          info: "Echo (ping) request",
          payload: "CTF7B31434D505F4330563352545F4348344E4E334C7D",
        },
      ],
    });

    this.networkTraffic.set(5, {
      packets: [
        {
          time: "10:19:05.345",
          source: "00:11:22:33:44:55",
          destination: "FF:FF:FF:FF:FF:FF",
          protocol: "ARP",
          info: "Who has 192.168.1.100? Tell 192.168.1.200",
          payload: "CTF7B4152505F5350303046314E475F44335433435445447D",
        },
      ],
    });

    this.networkTraffic.set(6, {
      packets: [
        {
          time: "10:20:15.678",
          source: "192.168.1.104",
          destination: "10.0.0.100",
          protocol: "TCP",
          info: "SYN, ACK",
          payload: "4354467B5443505F53545233344D5F464C34477D", // Hex encoded flag
        },
      ],
    });
  }

  setupEventListeners() {
    // Join competition button
    document.getElementById("joinBtn").addEventListener("click", () => {
      this.joinCompetition();
    });

    // Reset button
    document.getElementById("resetBtn").addEventListener("click", () => {
      this.resetAllUsers();
    });

    // Recalculate scores button
    document.getElementById("recalculateBtn").addEventListener("click", () => {
      this.recalculateAllScores();
    });

    // Username input enter key
    document.getElementById("username").addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        this.joinCompetition();
      }
    });

    // Wireshark capture button
    document.getElementById("startCapture").addEventListener("click", () => {
      this.toggleWiresharkCapture();
    });

    // Modal close button
    document.querySelector(".close").addEventListener("click", () => {
      this.closeModal();
    });

    // Close modal when clicking outside
    window.addEventListener("click", (e) => {
      if (e.target.classList.contains("modal")) {
        this.closeModal();
      }
    });
  }

  joinCompetition() {
    const username = document.getElementById("username").value.trim();
    if (!username) {
      this.showNotification("Please enter a username", "error");
      return;
    }

    console.log("Attempting to join competition with username:", username);

    // Check if Firebase is initialized
    if (!this.db) {
      console.error("Firebase database not initialized");
      this.showNotification(
        "Error: Firebase not connected. Please check your internet connection.",
        "error"
      );
      return;
    }

    this.currentUser = username;

    try {
      // Add user to Firebase
      this.db
        .ref(`users/${username}`)
        .set({
          username: username,
          joinedAt: firebase.database.ServerValue.TIMESTAMP,
          lastActivity: firebase.database.ServerValue.TIMESTAMP,
        })
        .then(() => {
          console.log("User added to Firebase successfully");

          // Add user to leaderboard in Firebase
          return this.db.ref(`leaderboard/${username}`).set({
            username: username,
            score: 0,
            flags: [],
            lastActivity: firebase.database.ServerValue.TIMESTAMP,
          });
        })
        .then(() => {
          console.log("User added to leaderboard successfully");

          document.getElementById("username").disabled = true;
          document.getElementById("joinBtn").disabled = true;
          document.getElementById("startCapture").disabled = false;

          this.showNotification(
            `Welcome ${username}! You can now start capturing flags using Wireshark.`,
            "success"
          );

          // Show challenges section after registration
          this.showChallengesSection();

          // Initialize challenges if not already done
          this.renderChallenges();
        })
        .catch((error) => {
          console.error("Firebase error:", error);
          this.showNotification(
            `Error joining competition: ${error.message}`,
            "error"
          );
        });
    } catch (error) {
      console.error("Error in joinCompetition:", error);
      this.showNotification(`Error: ${error.message}`, "error");
    }
  }

  showChallengesSection() {
    // Show challenges section and hide welcome message
    const challengesSection = document.querySelector(".challenges-section");
    const welcomeMessage = document.getElementById("welcome-message");

    if (challengesSection) {
      challengesSection.style.display = "block";
    }

    if (welcomeMessage) {
      welcomeMessage.style.display = "none";
    }
  }

  hideChallengesSection() {
    // Hide challenges section and show welcome message
    const challengesSection = document.querySelector(".challenges-section");
    const welcomeMessage = document.getElementById("welcome-message");

    if (challengesSection) {
      challengesSection.style.display = "none";
    }

    if (welcomeMessage) {
      welcomeMessage.style.display = "block";
    }
  }

  simulateOtherUsers() {
    // No-op: Remove all simulated/bot users
  }

  renderChallenges() {
    const challengesContainer = document.getElementById("challenges");
    challengesContainer.innerHTML = "";

    this.challenges.forEach((challenge) => {
      const state = this.challengeStates.get(challenge.id);
      const card = document.createElement("div");
      card.className = `challenge-card ${state.status}`;
      card.dataset.challengeId = challenge.id;

      card.innerHTML = `
                <div class="challenge-title">${challenge.title}</div>
                <div class="challenge-difficulty difficulty-${
                  challenge.difficulty
                }">${challenge.difficulty.toUpperCase()}</div>
                <div class="challenge-description">${
                  challenge.description
                }</div>
                <div style="margin-top: 10px; font-size: 12px; color: #ffd700;">
                    Points: ${challenge.points} | Category: ${
        challenge.category
      }
                </div>
            `;

      if (state.status === "occupied") {
        card.innerHTML += `<div style="margin-top: 10px; font-size: 12px; color: #ff6b6b;">
                    🔒 Occupied by: ${state.occupiedBy}
                </div>`;
      } else if (state.status === "completed") {
        const scoreEarned = state.score || challenge.points;
        card.innerHTML += `<div style="margin-top: 10px; font-size: 12px; color: #4ecdc4;">
                    ✅ Completed by: ${state.completedBy} | Score: +${scoreEarned}
                </div>`;
      }

      card.addEventListener("click", () => {
        this.openChallenge(challenge);
      });

      challengesContainer.appendChild(card);
    });
  }

  openChallenge(challenge) {
    const state = this.challengeStates.get(challenge.id);

    if (
      state &&
      state.status === "occupied" &&
      state.occupiedBy !== this.currentUser
    ) {
      this.showNotification(
        `Challenge is currently occupied by ${state.occupiedBy}`,
        "error"
      );
      return;
    }

    if (state && state.status === "completed") {
      this.showNotification(
        "This challenge has already been completed",
        "error"
      );
      return;
    }

    // Occupy the challenge in Firebase
    if (!state || state.status === "available") {
      const newState = {
        status: "occupied",
        occupiedBy: this.currentUser,
        startTime: firebase.database.ServerValue.TIMESTAMP,
      };
      this.db.ref(`challenges/${challenge.id}`).set(newState);
    }

    const modal = document.getElementById("challengeModal");
    const modalContent = document.getElementById("modalContent");

    modalContent.innerHTML = `
            <h2>${challenge.title}</h2>
            <div class="challenge-content">
                <h3>Challenge Description</h3>
                <p>${challenge.description}</p>
                
                <h3>Your Task</h3>
                <div style="background: rgba(255,215,0,0.1); padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #ffd700;">
                    <p><strong>${challenge.requiredAction}</strong></p>
                </div>
                
                <h3>Wireshark Instructions</h3>
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <p><strong>1.</strong> Start Wireshark capture on your network interface</p>
                    <p><strong>2.</strong> Apply filter: <code>${this.getWiresharkFilter(
                      challenge
                    )}</code></p>
                    <p><strong>3.</strong> Look for packets that match the challenge criteria</p>
                    <p><strong>4.</strong> Analyze the packet contents to find the flag</p>
                    <p><strong>5.</strong> The flag format is: <code>CTF{...}</code></p>
                </div>
                
                <h3>Hints</h3>
                <ul>
                    ${challenge.hints
                      .map((hint) => `<li>${hint}</li>`)
                      .join("")}
                </ul>
                
                <h3>Submit Your Flag</h3>
                <p style="color: #ffd700; font-style: italic;">You must capture the actual network traffic using Wireshark to find this flag!</p>
                <div class="flag-input">
                    <input type="text" id="flagInput" placeholder="Enter flag (format: CTF{...})" />
                    <button class="btn btn-primary" onclick="ctfSystem.submitFlag(${
                      challenge.id
                    })">Submit Flag</button>
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background: rgba(255,107,107,0.1); border-radius: 8px; border-left: 4px solid #ffd700;">
                    <h4>⚠️ Important Notes:</h4>
                    <ul>
                        <li>You must use Wireshark to capture real network traffic</li>
                        <li>All team members must be on the same local network</li>
                        <li>Flags are hidden in actual packet data</li>
                        <li>You can see other users' activities in real-time</li>
                    </ul>
                </div>
            </div>
        `;

    modal.style.display = "block";
  }

  getWiresharkFilter(challenge) {
    const filters = {
      1: "http", // HTTP traffic
      2: "dns", // DNS queries
      3: "ftp", // FTP traffic
      4: "icmp", // ICMP packets
      5: "arp", // ARP packets
      6: "tcp", // TCP streams
      7: "tcp.port == 1337", // TCP port 1337
      8: "udp.port == 4242", // UDP port 4242
      9: "icmp && frame contains 'CAESAR3'", // ICMP with specific payload
      10: "tcp.port == 2024", // TCP port 2024
      11: "dns && frame contains 'easydnsflag'", // DNS with specific subdomain
    };
    return filters[challenge.id] || "ip";
  }

  submitFlag(challengeId) {
    const flagInput = document.getElementById("flagInput");
    const submittedFlag = flagInput.value.trim();
    const challenge = this.challenges.find((c) => c.id === challengeId);

    if (!submittedFlag) {
      this.showNotification("Please enter a flag", "error");
      return;
    }

    if (submittedFlag === challenge.flag) {
      // Update challenge state in Firebase
      const newState = {
        status: "completed",
        completedBy: this.currentUser,
        completedAt: firebase.database.ServerValue.TIMESTAMP,
        score: challenge.points, // Add the score to the challenge data
      };
      this.db.ref(`challenges/${challengeId}`).set(newState);

      // Update leaderboard in Firebase
      this.db
        .ref(`leaderboard/${this.currentUser}`)
        .once("value")
        .then((snapshot) => {
          const userData = snapshot.val() || {
            username: this.currentUser,
            score: 0,
            flags: [],
          };

          // Ensure flags array exists
          if (!userData.flags) {
            userData.flags = [];
          }

          console.log("Current user data:", userData);
          console.log("Adding points:", challenge.points);

          userData.score += challenge.points;
          userData.flags.push(challengeId);
          userData.lastActivity = firebase.database.ServerValue.TIMESTAMP;

          console.log("Updated user data:", userData);

          return this.db.ref(`leaderboard/${this.currentUser}`).set(userData);
        })
        .then(() => {
          console.log("Firebase update completed successfully");

          // Calculate actual score from completed challenges
          const { totalScore, completedChallenges } = this.calculateUserScore(
            this.currentUser
          );
          console.log(
            "Calculated total score:",
            totalScore,
            "from challenges:",
            completedChallenges
          );

          // Update with calculated score
          return this.db.ref(`leaderboard/${this.currentUser}`).update({
            score: totalScore,
            flags: completedChallenges,
            lastActivity: firebase.database.ServerValue.TIMESTAMP,
          });
        })
        .then(() => {
          console.log("Score calculation update completed");

          // Force a refresh of the leaderboard data
          return this.db.ref("leaderboard").once("value");
        })
        .then((snapshot) => {
          const data = snapshot.val();
          if (data) {
            this.leaderboard = Object.keys(data).map((key) => ({
              username: key,
              ...data[key],
            }));
            console.log("Leaderboard refreshed:", this.leaderboard);
            this.updateLeaderboard();
          }
        })
        .catch((error) => {
          console.error("Error updating leaderboard:", error);
        });

      this.showNotification(
        `🎉 Flag captured! +${challenge.points} points`,
        "success"
      );
      this.closeModal();
      this.renderChallenges();
      this.broadcastChallengeUpdate(challengeId, newState);
    } else {
      this.showNotification(
        "Incorrect flag. Use Wireshark to capture the real network traffic!",
        "error"
      );
    }
  }

  // Calculate total score from completed challenges
  calculateUserScore(username) {
    let totalScore = 0;
    let completedChallenges = [];

    console.log("Calculating score for user:", username);
    console.log("Current challenge states:", this.challengeStates);

    this.challengeStates.forEach((state, challengeId) => {
      console.log(`Challenge ${challengeId}:`, state);
      if (state.status === "completed" && state.completedBy === username) {
        const challenge = this.challenges.find((c) => c.id === challengeId);
        const score = state.score || challenge.points;
        console.log(
          `Found completed challenge ${challengeId} with score ${score}`
        );
        totalScore += score;
        completedChallenges.push(challengeId);
      }
    });

    console.log(
      "Final calculation - Total score:",
      totalScore,
      "Challenges:",
      completedChallenges
    );
    return { totalScore, completedChallenges };
  }

  // Recalculate all user scores from completed challenges
  recalculateAllScores() {
    console.log("Recalculating all scores...");

    // Get all users from Firebase
    this.db
      .ref("users")
      .once("value")
      .then((snapshot) => {
        const users = snapshot.val();
        if (users) {
          Object.keys(users).forEach((username) => {
            const { totalScore, completedChallenges } =
              this.calculateUserScore(username);
            console.log(
              `Recalculating for ${username}: score=${totalScore}, challenges=${completedChallenges}`
            );

            // Update leaderboard for this user
            this.db.ref(`leaderboard/${username}`).update({
              score: totalScore,
              flags: completedChallenges,
              lastActivity: firebase.database.ServerValue.TIMESTAMP,
            });
          });
        }
      });
  }

  // updateUserScore is now handled by Firebase in submitFlag method

  updateLeaderboard() {
    const leaderboardContainer = document.getElementById("leaderboard");
    leaderboardContainer.innerHTML = "";

    // Always show all registered users, sorted by score
    this.leaderboard.sort((a, b) => b.score - a.score);

    this.leaderboard.forEach((user, index) => {
      const item = document.createElement("div");
      item.className = "leaderboard-item";

      const rank = index + 1;
      const rankIcon =
        rank === 1 ? "🥇" : rank === 2 ? "🥈" : rank === 3 ? "🥉" : `#${rank}`;

      item.innerHTML = `
                <div>
                    <strong>${rankIcon} ${user.username}</strong>
                    <div style="font-size: 12px; color: rgba(255,255,255,0.7);">
                        Flags: ${
                          user.flags ? user.flags.length : 0
                        } | Last: ${this.formatTime(user.lastActivity)}
                    </div>
                </div>
                <div style="font-size: 1.2rem; font-weight: bold; color: #ffd700;">
                    ${user.score || 0} pts
                </div>
            `;

      leaderboardContainer.appendChild(item);
    });
  }

  formatTime(date) {
    if (!date) return "Never";

    // Handle Firebase timestamp
    const timestamp = date.val ? date.val() : date;
    const dateObj = new Date(timestamp);
    const now = new Date();
    const diff = now - dateObj;
    const minutes = Math.floor(diff / 60000);

    if (minutes < 1) return "Just now";
    if (minutes < 60) return `${minutes}m ago`;
    return `${Math.floor(minutes / 60)}h ago`;
  }

  toggleWiresharkCapture() {
    const button = document.getElementById("startCapture");
    const status = document.getElementById("networkStatus");
    const packetData = document.getElementById("packetData");

    if (!this.isConnected) {
      this.isConnected = true;
      button.textContent = "Stop Wireshark Capture";
      status.textContent = "Connected";
      status.classList.add("connected");

      this.showNotification(
        "Wireshark capture started. Look for the hidden network traffic!",
        "success"
      );
      this.simulateRealPacketCapture(packetData);
    } else {
      this.isConnected = false;
      button.textContent = "Start Wireshark Capture";
      status.textContent = "Disconnected";
      status.classList.remove("connected");

      this.showNotification("Wireshark capture stopped.", "error");
      packetData.innerHTML =
        "<p>Start Wireshark to begin packet analysis...</p>";
    }
  }

  simulateRealPacketCapture(packetData) {
    const packetTypes = [
      "HTTP GET /api/flag HTTP/1.1",
      "DNS Query: suspicious.example.com",
      "FTP USER admin",
      "ICMP Echo Request (Ping)",
      "ARP Request: Who has 192.168.1.100?",
      "TCP SYN to port 80",
    ];

    let packetCount = 0;
    const interval = setInterval(() => {
      if (!this.isConnected) {
        clearInterval(interval);
        return;
      }

      packetCount++;
      const packetType =
        packetTypes[Math.floor(Math.random() * packetTypes.length)];
      const timestamp = new Date().toLocaleTimeString();
      const sourceIP = `192.168.1.${Math.floor(Math.random() * 255)}`;
      const destIP = `10.0.0.${Math.floor(Math.random() * 255)}`;

      const packetInfo = `
[${timestamp}] Packet #${packetCount}
Source: ${sourceIP} → Destination: ${destIP}
Type: ${packetType}
Length: ${Math.floor(Math.random() * 1000) + 100} bytes
---
            `;

      packetData.innerHTML += packetInfo;
      packetData.scrollTop = packetData.scrollHeight;

      // Occasionally show hints about real traffic
      if (Math.random() < 0.05) {
        this.showNotification(
          "🔍 Look for unusual packet patterns or encoded data!",
          "success"
        );
      }
    }, 3000);
  }

  simulateOtherUserActivity() {
    // No-op: Remove all simulated/bot activity
  }

  closeModal() {
    document.getElementById("challengeModal").style.display = "none";
  }

  showNotification(message, type = "info") {
    const notifications = document.getElementById("notifications");
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;

    notifications.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  broadcastChallengeUpdate(challengeId, state) {
    // In a real implementation, this would send updates to other users via WebSocket
    console.log(`Challenge ${challengeId} updated:`, state);
  }

  startRealTimeUpdates() {
    // Simulate real-time updates every 10 seconds
    setInterval(() => {
      if (this.currentUser) {
        this.simulateOtherUserActivity();
      }
    }, 10000);
  }
}

// Initialize the CTF system when the page loads
let ctfSystem;
document.addEventListener("DOMContentLoaded", () => {
  ctfSystem = new CTFSystem();
});
