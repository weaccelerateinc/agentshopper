import { homedir } from 'os';
import { dirname, join, resolve } from 'path';

export const API_BASE_URL = process.env.ACCELERATE_API_BASE_URL || 'https://sbx.api.weaccelerate.com';
export const DEFAULT_MERCHANT_ID = process.env.ACCELERATE_DEFAULT_MERCHANT_ID || null;

function defaultSessionPath() {
  return join(homedir(), '.agentshop', 'accelerate-session.json');
}

export function getSessionFilePath() {
  const configured = process.env.AGENTSHOP_ACCELERATE_SESSION_FILE || defaultSessionPath();
  return resolve(configured);
}

export function getSessionDirectory() {
  return dirname(getSessionFilePath());
}
