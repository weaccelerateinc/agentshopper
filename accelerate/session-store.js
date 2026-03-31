import { mkdir, readFile, rm, writeFile } from 'fs/promises';
import { getSessionDirectory, getSessionFilePath } from './config.js';

export async function loadSession() {
  try {
    const raw = await readFile(getSessionFilePath(), 'utf8');
    return JSON.parse(raw);
  } catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  }
}

export async function saveSession(session) {
  await mkdir(getSessionDirectory(), { recursive: true });
  await writeFile(getSessionFilePath(), JSON.stringify(session, null, 2));
}

export async function clearSession() {
  await rm(getSessionFilePath(), { force: true });
}
