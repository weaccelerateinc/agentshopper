import { API_BASE_URL } from './config.js';

export class AccelerateApiError extends Error {
  constructor(message, { status = 0, body = null } = {}) {
    super(message);
    this.name = 'AccelerateApiError';
    this.status = status;
    this.body = body;
  }
}

async function parseResponse(response) {
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function request(path, { method = 'GET', headers = {}, body } = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body == null ? undefined : JSON.stringify(body),
  });
  const parsed = await parseResponse(response);
  if (!response.ok) {
    throw new AccelerateApiError(`Accelerate API request failed: ${method} ${path}`, {
      status: response.status,
      body: parsed,
    });
  }
  return parsed;
}

export async function getOnboardingStep(phoneNumber) {
  return request(`/agents/onboarding/step/${encodeURIComponent(phoneNumber)}`);
}

export async function sendCode({ phoneNumber, fingerPrint }) {
  return request('/agents/onboarding/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: { phoneNumber, fingerPrint },
  });
}

export async function startOnboarding({ firstName, lastName, phoneNumber, email, merchantId }) {
  return request('/agents/onboarding/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: {
      ...(firstName ? { firstName } : {}),
      ...(lastName ? { lastName } : {}),
      phoneNumber,
      ...(email ? { email } : {}),
      ...(merchantId ? { merchantId } : {}),
    },
  });
}

export async function verifyCode({ phoneNumber, code, fingerprint, merchantId }) {
  return request('/agents/onboarding/verify-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: {
      phoneNumber,
      code,
      fingerprint,
      ...(merchantId ? { merchantId } : {}),
    },
  });
}

export async function verifyOnboarding({ entityId, verificationId, verificationCode, merchantId }) {
  return request('/agents/onboarding/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: {
      entityId,
      verificationId,
      ...(verificationCode ? { verificationCode } : {}),
      ...(merchantId ? { merchantId } : {}),
    },
  });
}

export async function getFirebasePublicConfig() {
  return request('/agents/contracts/firebase-public-config');
}

export async function exchangeCustomToken(customToken) {
  const config = await getFirebasePublicConfig();
  const response = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=${encodeURIComponent(config.apiKey)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      token: customToken,
      returnSecureToken: true,
    }),
  });
  const parsed = await parseResponse(response);
  if (!response.ok) {
    throw new AccelerateApiError('Firebase token exchange failed', {
      status: response.status,
      body: parsed,
    });
  }
  return parsed;
}

export async function getUserDetails(idToken) {
  return request('/agents/users/me', {
    headers: { Authorization: `Bearer ${idToken}` },
  });
}

export async function getWalletCards(idToken, merchantId) {
  const headers = { Authorization: `Bearer ${idToken}` };
  if (merchantId) headers.merchantId = merchantId;
  return request('/agents/wallet/cards', { headers });
}

export async function getCardLockStatus(idToken, { paymentSourceId, merchantId }) {
  return request('/agents/wallet/get-card-lock-status', {
    method: 'POST',
    headers: { Authorization: `Bearer ${idToken}`, 'Content-Type': 'application/json' },
    body: {
      paymentSourceId,
      ...(merchantId ? { merchantId } : {}),
    },
  });
}

export async function submitVgsInbound(idToken, { paymentSourceId, verificationSessionId, payload }) {
  return request('/agents/wallet/vgs-inbound', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${idToken}`,
      'Content-Type': 'application/json',
      paymentSourceId,
      ...(verificationSessionId ? { verificationSessionId } : {}),
    },
    body: payload,
  });
}

export async function createPanProxyUrl(idToken, { paymentSourceId, amount }) {
  return request('/agents/credentials/pan', {
    method: 'POST',
    headers: { Authorization: `Bearer ${idToken}`, 'Content-Type': 'application/json' },
    body: { paymentSourceId, amount },
  });
}

export async function executePanProxy(idToken, proxyUrl) {
  const response = await fetch(proxyUrl, {
    headers: {
      Authorization: `Bearer ${idToken}`,
      'ngrok-skip-browser-warning': '1',
    },
  });
  const parsed = await parseResponse(response);
  if (!response.ok) {
    throw new AccelerateApiError('PAN proxy call failed', {
      status: response.status,
      body: parsed,
    });
  }
  return parsed;
}
