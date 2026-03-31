#!/usr/bin/env node

import { getSessionStatus, listWalletCards, materializePayment, startAuth, verifyAuth } from './service.js';

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const args = { _: command ? [command] : [] };
  for (let index = 0; index < rest.length; index += 1) {
    const current = rest[index];
    if (!current.startsWith('--')) continue;
    const key = current.slice(2).replace(/-/g, '_');
    const next = rest[index + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    index += 1;
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  let result;
  switch (command) {
    case 'auth-start':
      result = await startAuth({
        phoneNumber: args.phone,
        firstName: args.first_name,
        lastName: args.last_name,
        email: args.email,
        merchantId: args.merchant_id,
      });
      break;
    case 'auth-verify':
      result = await verifyAuth(args.phone, args.otp, args.merchant_id);
      break;
    case 'cards':
      result = await listWalletCards({ merchantId: args.merchant_id });
      break;
    case 'payment-materialize':
      result = await materializePayment({
        paymentSourceId: args.payment_source_id,
        amountCents: Number(args.amount_cents),
        merchantId: args.merchant_id,
        verificationPayload: {
          ...(args.card_number ? { 'card-number': args.card_number } : {}),
          ...(args.cvv ? { cvv: args.cvv } : {}),
          ...(args.exp_date ? { 'exp-date': args.exp_date } : {}),
        },
      });
      break;
    case 'session-status':
      result = await getSessionStatus();
      break;
    default:
      throw new Error('Unknown command. Use auth-start, auth-verify, cards, payment-materialize, or session-status.');
  }

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
});
