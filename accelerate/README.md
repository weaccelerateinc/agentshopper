# Accelerate MCP

Standalone MCP server and CLI for Accelerate wallet authentication and payment materialization.

## Install

```bash
cd accelerate
npm install
```

## MCP Server

```bash
node index.js
```

Tools:
- `accelerate_auth_start`
- `accelerate_auth_verify`
- `accelerate_wallet_list_cards`
- `accelerate_payment_materialize`
- `accelerate_session_status`

## CLI

```bash
node cli.js session-status
node cli.js auth-start --phone 6263211250 --first-name Gary --last-name Chao --email gharychao@gmail.com
node cli.js auth-verify --phone 6263211250 --otp 123456
node cli.js cards
node cli.js payment-materialize --payment-source-id 4b5f0ee0-fa5c-4c6e-8272-d5d48524b576 --amount-cents 10799
```

## Session Storage

By default, the reusable auth session is stored outside the repo at:

```bash
~/.agentshop/accelerate-session.json
```

Override with:

```bash
AGENTSHOP_ACCELERATE_SESSION_FILE=/custom/path/session.json
```
