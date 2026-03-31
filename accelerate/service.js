import crypto from 'crypto';
import { DEFAULT_MERCHANT_ID, getSessionFilePath } from './config.js';
import {
  AccelerateApiError,
  createPanProxyUrl,
  executePanProxy,
  exchangeCustomToken,
  getCardLockStatus,
  getOnboardingStep,
  getUserDetails,
  getWalletCards,
  sendCode,
  startOnboarding,
  submitVgsInbound,
  verifyOnboarding,
  verifyCode,
} from './client.js';
import { clearSession, loadSession, saveSession } from './session-store.js';

function nowMs() {
  return Date.now();
}

function expiresAtFromSeconds(seconds) {
  return nowMs() + Number(seconds || 0) * 1000;
}

function maskCardNumber(number) {
  if (!number) return null;
  return String(number).slice(-4);
}

function normalizeExpiry(month, year) {
  if (!month || !year) return '';
  return `${String(month).padStart(2, '0')}/${String(year).slice(-2)}`;
}

function buildSessionRecord({ phoneNumber, fingerprint, exchangeResponse, customToken }) {
  return {
    phoneNumber,
    fingerprint,
    idToken: exchangeResponse.idToken,
    refreshToken: exchangeResponse.refreshToken,
    expiresAt: expiresAtFromSeconds(exchangeResponse.expiresIn),
    customTokenIssuedAt: nowMs(),
    customToken,
  };
}

function buildPendingOnboarding({
  phoneNumber,
  fingerprint,
  entityId,
  verificationId,
  firstName,
  lastName,
  email,
  merchantId,
}) {
  return {
    phoneNumber,
    fingerprint,
    pendingOnboarding: {
      entityId,
      verificationId,
      firstName: firstName || null,
      lastName: lastName || null,
      email: email || null,
      merchantId: merchantId || null,
      startedAt: nowMs(),
    },
  };
}

function assertVgsSatisfied(lockStatus, verificationPayload) {
  if (!lockStatus.canVerify) {
    throw new Error(`Card ${lockStatus.paymentSourceId} cannot be verified for this flow`);
  }
  if (lockStatus.isNumberRequired && !verificationPayload?.['card-number']) {
    throw new Error('Accelerate requires full card number verification before materialization');
  }
  if (lockStatus.isCvvRequired && !verificationPayload?.cvv) {
    throw new Error('Accelerate requires CVV verification before materialization');
  }
  if (lockStatus.isExpiryRequired && !verificationPayload?.['exp-date']) {
    throw new Error('Accelerate requires expiry verification before materialization');
  }
}

async function getUsableSession() {
  const session = await loadSession();
  if (!session) return null;
  if (!session.idToken || !session.expiresAt || session.expiresAt <= nowMs() + 60_000) {
    return null;
  }
  return session;
}

export async function getSessionStatus() {
  const persisted = await loadSession();
  const active = await getUsableSession();
  const hasPendingOnboarding = !!persisted?.pendingOnboarding?.verificationId;
  return {
    has_session: !!persisted,
    is_authenticated: !!active,
    phone_number: active?.phoneNumber || persisted?.phoneNumber || null,
    expires_at: active?.expiresAt || persisted?.expiresAt || null,
    requires_reauth: !!persisted && !active && !hasPendingOnboarding,
    awaiting_verification: hasPendingOnboarding && !active,
    pending_onboarding: persisted?.pendingOnboarding || null,
    session_file: getSessionFilePath(),
  };
}

export async function startAuth({
  phoneNumber,
  firstName,
  lastName,
  email,
  merchantId = DEFAULT_MERCHANT_ID,
} = {}) {
  if (!phoneNumber) {
    throw new Error('phoneNumber is required');
  }

  const fingerprint = crypto.randomUUID().toLowerCase();
  const step = await getOnboardingStep(phoneNumber);

  try {
    const started = await startOnboarding({
      firstName,
      lastName,
      phoneNumber,
      email,
      merchantId,
    });
    await saveSession(buildPendingOnboarding({
      phoneNumber,
      fingerprint,
      entityId: started.entityId,
      verificationId: started.verificationId,
      firstName,
      lastName,
      email,
      merchantId,
    }));

    return {
      phone_number: phoneNumber,
      first_name: firstName || null,
      last_name: lastName || null,
      email: email || null,
      merchant_id: merchantId || null,
      onboarding_state: step.state,
      otp_sent: true,
      auth_state: 'otp_required',
      fingerprint,
      entity_id: started.entityId,
      verification_id: started.verificationId,
      auth_flow: 'onboarding_start',
    };
  } catch (error) {
    const send = await sendCode({ phoneNumber, fingerPrint: fingerprint });
    await saveSession({ phoneNumber, fingerprint, pendingOnboarding: null });

    return {
      phone_number: phoneNumber,
      first_name: firstName || null,
      last_name: lastName || null,
      email: email || null,
      merchant_id: merchantId || null,
      onboarding_state: step.state,
      otp_sent: send?.status === 'Ok',
      auth_state: 'otp_required',
      fingerprint,
      auth_flow: 'send_code_fallback',
      fallback_reason: error.message,
    };
  }
}

export async function verifyAuth(phoneNumber, otpCode, merchantId = DEFAULT_MERCHANT_ID) {
  const persisted = await loadSession();
  const fingerprint = persisted?.phoneNumber === phoneNumber && persisted?.fingerprint
    ? persisted.fingerprint
    : crypto.randomUUID().toLowerCase();
  const pending = persisted?.phoneNumber === phoneNumber ? persisted?.pendingOnboarding : null;

  let customToken;
  let authFlow = 'verify_code';
  let fieldsNeeded = [];

  if (pending?.entityId && pending?.verificationId) {
    const verified = await verifyOnboarding({
      entityId: pending.entityId,
      verificationId: pending.verificationId,
      verificationCode: otpCode,
      merchantId: merchantId || pending.merchantId || undefined,
    });
    customToken = verified?.authToken || null;
    fieldsNeeded = verified?.fieldsNeeded || [];
    authFlow = 'onboarding_verify';
  } else {
    const verified = await verifyCode({
      phoneNumber,
      code: otpCode,
      fingerprint,
      merchantId,
    });
    customToken = verified?.customToken || null;
    fieldsNeeded = [];
  }

  if (!customToken) {
    throw new Error(
      fieldsNeeded.length
        ? `Accelerate verification succeeded but still needs fields: ${fieldsNeeded.join(', ')}`
        : 'Accelerate verification did not return a custom token'
    );
  }

  const exchanged = await exchangeCustomToken(customToken);
  const session = buildSessionRecord({
    phoneNumber,
    fingerprint,
    exchangeResponse: exchanged,
    customToken,
  });
  await saveSession(session);

  return {
    phone_number: phoneNumber,
    is_authenticated: true,
    expires_at: session.expiresAt,
    is_new_user: !!exchanged.isNewUser,
    auth_flow: authFlow,
    fields_needed: fieldsNeeded,
  };
}

export async function listWalletCards({ merchantId = DEFAULT_MERCHANT_ID } = {}) {
  const session = await getUsableSession();
  if (!session) {
    throw new Error('No valid Accelerate session. Run accelerate_auth_start and accelerate_auth_verify first.');
  }

  try {
    const [user, wallet] = await Promise.all([
      getUserDetails(session.idToken),
      getWalletCards(session.idToken, merchantId),
    ]);

    return {
      user,
      wallet,
    };
  } catch (error) {
    if (error instanceof AccelerateApiError && error.status === 401) {
      await clearSession();
      throw new Error('Accelerate session expired. Re-authenticate and retry.');
    }
    throw error;
  }
}

export async function materializePayment({
  paymentSourceId,
  amountCents,
  merchantId = DEFAULT_MERCHANT_ID,
  verificationPayload,
} = {}) {
  if (!paymentSourceId) {
    throw new Error('paymentSourceId is required');
  }
  if (!Number.isInteger(amountCents) || amountCents <= 0) {
    throw new Error('amountCents must be a positive integer');
  }

  const session = await getUsableSession();
  if (!session) {
    throw new Error('No valid Accelerate session. Run accelerate_auth_start and accelerate_auth_verify first.');
  }

  try {
    const lockStatus = await getCardLockStatus(session.idToken, { paymentSourceId, merchantId });

    if (
      lockStatus.isNumberRequired ||
      lockStatus.isCvvRequired ||
      lockStatus.isExpiryRequired ||
      lockStatus.isBillingZipRequired
    ) {
      assertVgsSatisfied(lockStatus, verificationPayload);
      await submitVgsInbound(session.idToken, {
        paymentSourceId,
        verificationSessionId: lockStatus.preAuthId,
        payload: verificationPayload,
      });
    }

    const { proxyUrl } = await createPanProxyUrl(session.idToken, {
      paymentSourceId,
      amount: amountCents,
    });
    const materialized = await executePanProxy(session.idToken, proxyUrl);

    return {
      payment_source_id: paymentSourceId,
      amount_cents: amountCents,
      amount_usd: materialized.amountUSD || null,
      lock_status: lockStatus,
      payment: {
        cardNumber: materialized.number,
        expiry: normalizeExpiry(materialized.expirationMonth, materialized.expirationYear),
        cvv: materialized.cvv,
        source: 'accelerate',
        last4: materialized.last4 || maskCardNumber(materialized.number),
        network: materialized.details?.cardIssuer || null,
        expirationMonth: materialized.expirationMonth || null,
        expirationYear: materialized.expirationYear || null,
      },
    };
  } catch (error) {
    if (error instanceof AccelerateApiError && error.status === 401) {
      await clearSession();
      throw new Error('Accelerate session expired. Re-authenticate and retry.');
    }
    throw error;
  }
}
