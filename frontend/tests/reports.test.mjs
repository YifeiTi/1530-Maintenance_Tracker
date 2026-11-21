import test from 'node:test';
import assert from 'node:assert/strict';
import { statusLabel, submissionDate, readResponse } from '../lib/reports.mjs';

test('database status values use the story labels without changing API values', () => {
  assert.equal(statusLabel('open'), 'Submitted');
  assert.equal(statusLabel('in_progress'), 'In progress');
  assert.equal(statusLabel('resolved'), 'Resolved');
});

test('submission time works with list/detail timestamps and missing values', () => {
  const date = '2026-11-20T15:00:00Z';
  assert.equal(submissionDate({ submitted_at: date }), submissionDate({ created_at: date }));
  assert.equal(submissionDate({}), 'Not available');
});

test('backend validation messages and missing reports reach the user', async () => {
  await assert.rejects(readResponse(new Response(JSON.stringify({ detail: 'Description is required' }), { status: 400 })), /Description is required/);
  await assert.rejects(readResponse(new Response(JSON.stringify({ detail: 'Report not found' }), { status: 404 })), /Report not found/);
  await assert.rejects(readResponse(new Response('Bad gateway', { status: 502 })), /unreadable response/);
});
