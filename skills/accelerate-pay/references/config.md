# Accelerate Pay Configuration

## User Profile
- **Name:** (your first and last name)
- **Phone:** (your phone number for OTP)
- **Email:** (your email address)

## Preferred Card
- **Card:** (description, e.g., "Capital One ending in 1234")
- **Payment Source ID:** (from `node cli.js cards`, e.g., `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

## CLI Location
- **Path:** `<repo>/accelerate`
- **Commands:** `node cli.js <command>`

## Session Storage
- **File:** `~/.agentshop/accelerate-session.json`

## Setup Steps
1. Run `cd <repo>/accelerate && npm install`
2. Run `node cli.js auth-start --phone <PHONE> --first-name <FIRST> --last-name <LAST> --email <EMAIL>`
3. Enter OTP: `node cli.js auth-verify --phone <PHONE> --otp <CODE>`
4. List cards: `node cli.js cards`
5. Copy the preferred `paymentSourceId` into this file
