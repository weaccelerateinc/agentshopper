#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { getSessionStatus, listWalletCards, materializePayment, startAuth, verifyAuth } from './service.js';

const server = new Server(
  {
    name: 'accelerate-mcp',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

function toTextResult(payload) {
  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(payload, null, 2),
      },
    ],
  };
}

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'accelerate_auth_start',
      description: 'Start Accelerate onboarding/authentication using buyer identity fields and return verification identifiers for OTP completion.',
      inputSchema: {
        type: 'object',
        properties: {
          phone_number: {
            type: 'string',
            description: 'Phone number entered by the user.',
          },
          first_name: {
            type: 'string',
            description: 'Buyer first name.',
          },
          last_name: {
            type: 'string',
            description: 'Buyer last name.',
          },
          email: {
            type: 'string',
            description: 'Buyer email address.',
          },
          merchant_id: {
            type: 'string',
            description: 'Optional Accelerate merchant id.',
          },
        },
        required: ['phone_number'],
      },
    },
    {
      name: 'accelerate_auth_verify',
      description: 'Verify an OTP and persist a reusable Accelerate session locally.',
      inputSchema: {
        type: 'object',
        properties: {
          phone_number: { type: 'string' },
          otp_code: { type: 'string' },
          merchant_id: { type: 'string' },
        },
        required: ['phone_number', 'otp_code'],
      },
    },
    {
      name: 'accelerate_wallet_list_cards',
      description: 'List wallet cards and offers for the authenticated Accelerate user.',
      inputSchema: {
        type: 'object',
        properties: {
          merchant_id: { type: 'string' },
        },
      },
    },
    {
      name: 'accelerate_payment_materialize',
      description: 'Materialize PAN, expiry, and CVV for a selected wallet card for immediate use in checkout.',
      inputSchema: {
        type: 'object',
        properties: {
          payment_source_id: { type: 'string' },
          amount_cents: { type: 'integer' },
          merchant_id: { type: 'string' },
          verification_payload: {
            type: 'object',
            properties: {
              'card-number': { type: 'string' },
              cvv: { type: 'string' },
              'exp-date': { type: 'string' },
            },
          },
        },
        required: ['payment_source_id', 'amount_cents'],
      },
    },
    {
      name: 'accelerate_session_status',
      description: 'Report whether a reusable Accelerate session already exists.',
      inputSchema: {
        type: 'object',
        properties: {},
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;

  switch (name) {
    case 'accelerate_auth_start':
      return toTextResult(await startAuth({
        phoneNumber: args.phone_number,
        firstName: args.first_name,
        lastName: args.last_name,
        email: args.email,
        merchantId: args.merchant_id,
      }));
    case 'accelerate_auth_verify':
      return toTextResult(await verifyAuth(args.phone_number, args.otp_code, args.merchant_id));
    case 'accelerate_wallet_list_cards':
      return toTextResult(await listWalletCards({ merchantId: args.merchant_id }));
    case 'accelerate_payment_materialize':
      return toTextResult(await materializePayment({
        paymentSourceId: args.payment_source_id,
        amountCents: args.amount_cents,
        merchantId: args.merchant_id,
        verificationPayload: args.verification_payload,
      }));
    case 'accelerate_session_status':
      return toTextResult(await getSessionStatus());
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
