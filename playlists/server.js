// server.js
import express from 'express';
import cors from 'cors';
import { Storage } from '@google-cloud/storage';

const app = express();
app.use(express.json({ limit: '2mb' }));

// Restrict CORS to your submission origin in production
const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || '*';
app.use(cors({ origin: ALLOWED_ORIGIN }));

const BUCKET = process.env.BUCKET;
if (!BUCKET) throw new Error('Missing BUCKET env var');
const storage = new Storage();
const bucket = storage.bucket(BUCKET);

// Simple MIME allow‑lists
const AUDIO_MIME = new Set(['audio/mpeg', 'audio/wav', 'audio/x-wav']);
const IMAGE_MIME = new Set(['image/jpeg', 'image/png']);

function sanitizeName(name = '') {
  return name.toLowerCase().replace(/[^a-z0-9._-]+/g, '-').replace(/^-+|-+$/g, '');
}

app.post('/uploadUrl', async (req, res) => {
  try {
    const { kind, filename, contentType } = req.body || {};
    if (!kind || !filename || !contentType) {
      return res.status(400).json({ error: 'missing fields' });
    }
    if (kind === 'audio' && !AUDIO_MIME.has(contentType)) {
      return res.status(400).json({ error: 'unsupported audio type' });
    }
    if (kind === 'image' && !IMAGE_MIME.has(contentType)) {
      return res.status(400).json({ error: 'unsupported image type' });
    }

    const ts = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    const safe = sanitizeName(filename);
    const prefix = kind === 'audio' ? 'uploads/audio' : 'uploads/images';
    const objectName = `${prefix}/${ts}/${Date.now()}-${safe}`;

    const file = bucket.file(objectName);
    const expires = Date.now() + 10 * 60 * 1000; // 10 minutes

    const [uploadUrl] = await file.getSignedUrl({
      version: 'v4',
      action: 'write',
      expires,
      contentType,
    });

    // Public URL assumes bucket allows public read (see setup below)
    const publicUrl = `https://storage.googleapis.com/${BUCKET}/${objectName}`;

    res.json({ uploadUrl, publicUrl, objectName });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'server_error' });
  }
});

app.get('/healthz', (_req, res) => res.send('ok'));

const port = process.env.PORT || 8080;
app.listen(port, () => console.log('upload service listening on ' + port));