# Firebase Setup Instructions

## Overview

The Adaptive Learning API now uses Firebase Firestore as its database. You'll need to set up a Firebase project and obtain service account credentials.

## Step-by-Step Setup

### 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select an existing project
3. Enter a project name (e.g., "adaptive-learning-api")
4. (Optional) Enable Google Analytics
5. Click "Create project"

### 2. Enable Firestore Database

1. In your Firebase project dashboard, click "Build" → "Firestore Database"
2. Click "Create database"
3. Choose a location for your database (select closest to your users)
4. Start in **production mode** or **test mode**:
   - **Production mode**: Secure by default, requires authentication rules
   - **Test mode**: Open for 30 days (good for development)
5. Click "Enable"

### 3. Generate Service Account Credentials

1. In Firebase Console, click the gear icon (⚙️) → "Project settings"
2. Navigate to the "Service accounts" tab
3. Click "Generate new private key"
4. A dialog will appear warning that the key should be kept confidential
5. Click "Generate key"
6. A JSON file will download automatically

### 4. Configure Your Application

#### Option A: Local Development

1. Rename the downloaded JSON file to `firebase-credentials.json`
2. Place it in the root directory of this project (same level as `app/` folder)
3. **Important**: This file is already in `.gitignore` to prevent accidental commits
4. The application will automatically use this file

#### Option B: Using Environment Variable

1. Copy the downloaded JSON file to a secure location
2. Update your `.env` file:
   ```bash
   FIREBASE_CREDENTIALS_PATH=/path/to/your/firebase-credentials.json
   ```

### 5. Verify Setup

Run the health check endpoint to verify Firebase connection:

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "Firebase Firestore"
}
```

## Seed Sample Data

Once Firebase is configured, populate the database with sample questions:

```bash
python seed_data.py
```

This will create 30 questions across Python, JavaScript, and Data Science subjects.

## Security Best Practices

### ⚠️ Important Security Notes

1. **Never commit credentials to Git**
   - The `firebase-credentials.json` is gitignored
   - Double-check before pushing code

2. **Firestore Security Rules**
   - Configure appropriate security rules in Firebase Console
   - Go to Firestore Database → Rules
   - Example rules for authenticated access:
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read, write: if request.auth != null;
       }
     }
   }
   ```

3. **Service Account Permissions**
   - The service account has admin access to Firestore
   - Rotate credentials periodically
   - Use separate credentials for development and production

4. **API Key Protection**
   - Change default `ADMIN_API_KEY` and `AI_API_KEY` in production
   - Store them as environment variables or secrets

## Troubleshooting

### Error: "Firebase credentials not found"
- Verify the `firebase-credentials.json` file exists in the root directory
- Check the `FIREBASE_CREDENTIALS_PATH` in your `.env` file
- Ensure the path is absolute or relative to the project root

### Error: "Permission denied"
- Check Firestore security rules in Firebase Console
- Verify the service account has proper permissions
- Ensure you're using the correct project ID

### Error: "Failed to initialize Firebase"
- Verify the JSON credentials file is valid
- Check if Firebase services are enabled for your project
- Ensure Firestore is enabled (not Realtime Database)

## Firebase Console Access

- **Firestore Data Viewer**: Firebase Console → Firestore Database
- **Usage Statistics**: Firebase Console → Usage and billing
- **Security Rules**: Firebase Console → Firestore Database → Rules
- **Indexes**: Firebase Console → Firestore Database → Indexes

## Cost Considerations

Firebase Firestore has a generous free tier:
- **Reads**: 50,000/day
- **Writes**: 20,000/day
- **Deletes**: 20,000/day
- **Storage**: 1 GB

Monitor usage in Firebase Console → Usage and billing

## Next Steps

1. ✅ Set up Firebase project
2. ✅ Download service account credentials
3. ✅ Configure application
4. ✅ Seed database with sample data
5. ✅ Test API endpoints
6. 📊 Set up Power BI integration (see API_DOCUMENTATION.md)

For Power BI dashboard integration, use the endpoint:
```
GET /api/powerbi/analytics
X-API-Key: your-admin-api-key
```

This provides comprehensive analytics data ready for Power BI visualization.
