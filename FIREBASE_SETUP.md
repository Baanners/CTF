# Firebase Setup for Real-Time CTF

## 🚀 Your CTF is now Real-Time!

The CTF website has been upgraded to use **Firebase Realtime Database** for true real-time synchronization across all users.

## ✅ What's Now Working

### **Real-Time Features:**

- **Live Leaderboard**: All users see score updates instantly
- **Challenge Locking**: When one user starts a challenge, others see it as occupied immediately
- **Flag Capture**: When someone captures a flag, all users see the update in real-time
- **User Management**: All registered users appear on the leaderboard instantly

### **How It Works:**

1. **User joins** → Added to Firebase in real-time
2. **User starts challenge** → Challenge locked in Firebase, all users see it
3. **User captures flag** → Score updated in Firebase, leaderboard updates for everyone
4. **All actions sync** → Every user's browser updates automatically

## 🔧 Firebase Configuration

The Firebase config is already set up in `script.js`:

```javascript
this.firebaseConfig = {
  apiKey: "AIzaSyCrlgwWQ5QFib3fhdSTBgOMHJqAJVl4fLM",
  authDomain: "wireshark-f1fe7.firebaseapp.com",
  databaseURL: "https://wireshark-f1fe7-default-rtdb.firebaseio.com",
  projectId: "wireshark-f1fe7",
  storageBucket: "wireshark-f1fe7.firebasestorage.app",
  messagingSenderId: "651462050730",
  appId: "1:651462050730:web:4b8e1efff8a9b5a48da1d3",
};
```

## 📊 Firebase Database Structure

Your Firebase Realtime Database will have this structure:

```
wireshark-f1fe7-default-rtdb/
├── users/
│   ├── username1/
│   │   ├── username: "username1"
│   │   ├── joinedAt: timestamp
│   │   └── lastActivity: timestamp
│   └── username2/
│       └── ...
├── leaderboard/
│   ├── username1/
│   │   ├── username: "username1"
│   │   ├── score: 150
│   │   ├── flags: [100, 50]
│   │   └── lastActivity: timestamp
│   └── username2/
│       └── ...
└── challenges/
    ├── 1/
    │   ├── status: "completed"
    │   ├── completedBy: "username1"
    │   └── completedAt: timestamp
    ├── 2/
    │   ├── status: "occupied"
    │   ├── occupiedBy: "username2"
    │   └── startTime: timestamp
    └── ...
```

## 🎯 How to Test Real-Time Features

### **Test with Multiple Users:**

1. **Deploy to GitHub Pages** (as before)
2. **Open the website in multiple browser tabs/windows**
3. **Join with different usernames** in each tab
4. **Start a challenge** in one tab - watch it lock in the other tabs
5. **Capture a flag** in one tab - watch the leaderboard update in all tabs

### **Expected Behavior:**

- ✅ **User joins** → Appears on leaderboard in all tabs
- ✅ **Challenge locked** → Shows as occupied in all tabs
- ✅ **Flag captured** → Score updates in all tabs instantly
- ✅ **Real-time sync** → No page refresh needed

## 🔒 Security Notes

- **Firebase Rules**: The database is currently open for demo purposes
- **Production**: For production use, set up proper Firebase security rules
- **Authentication**: Consider adding user authentication for more security

## 🐛 Troubleshooting

### **If real-time updates don't work:**

1. Check browser console for Firebase errors
2. Verify Firebase config is correct
3. Check internet connection (Firebase needs internet)
4. Try refreshing the page

### **If users don't appear on leaderboard:**

1. Check Firebase console for database entries
2. Verify Firebase listeners are working
3. Check browser console for errors

## 🎉 Benefits of Real-Time CTF

- **True Competition**: Users can see others working in real-time
- **Live Leaderboard**: Instant score updates
- **Challenge Locking**: Prevents conflicts between users
- **Better UX**: No page refreshes needed
- **Scalable**: Works with any number of users

---

**Your CTF is now ready for real-time, multi-user competitions! 🚀**
