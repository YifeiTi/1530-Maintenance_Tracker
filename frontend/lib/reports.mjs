export function statusLabel(status) {
  return { open: 'Submitted', in_progress: 'In progress', resolved: 'Resolved' }[status] || status || 'Unknown';
}

export function submissionDate(report) {
  const value = report.submitted_at || report.created_at;
  if (!value || Number.isNaN(new Date(value).getTime())) return 'Not available';
  return new Date(value).toLocaleString();
}

export async function readResponse(response) {
  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error('The server returned an unreadable response. Please try again.');
  }
  if (!response.ok) {
    if (typeof data.detail === 'string') throw new Error(data.detail);
    if (Array.isArray(data.detail)) {
      throw new Error(data.detail.map((item) => item.msg).join('; '));
    }
    throw new Error('The request failed. Please try again.');
  }
  return data;
}

export const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
