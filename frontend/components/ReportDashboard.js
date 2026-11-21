'use client';

import { useRef, useState } from 'react';
import { readResponse, statusLabel, submissionDate, uuidPattern } from '../lib/reports.mjs';

export default function ReportDashboard() {
  const [unitId, setUnitId] = useState('');
  const [tenantId, setTenantId] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [reports, setReports] = useState(null);
  const [selected, setSelected] = useState(null);
  const [listError, setListError] = useState('');
  const [detailError, setDetailError] = useState('');
  const [submitError, setSubmitError] = useState('');
  const [notice, setNotice] = useState('');
  const [loading, setLoading] = useState(false);
  const [opening, setOpening] = useState(false);
  const [saving, setSaving] = useState(false);
  const listRequest = useRef(0);
  const detailRequest = useRef(0);

  function changeUnit(value) {
    listRequest.current++;
    detailRequest.current++;
    setUnitId(value);
    setReports(null);
    setSelected(null);
    setNotice('');
    setListError('');
    setDetailError('');
    setLoading(false);
    setOpening(false);
  }

  async function loadReports(unit) {
    const request = ++listRequest.current;
    setLoading(true);
    setListError('');
    try {
      const data = await fetch(`/api/reports?unit_id=${encodeURIComponent(unit)}`, { cache: 'no-store' }).then(readResponse);
      if (request === listRequest.current) setReports(data);
    } catch (error) {
      if (request === listRequest.current) {
        setReports(null);
        setListError(error.message);
      }
    } finally {
      if (request === listRequest.current) setLoading(false);
    }
  }

  function showReports(event) {
    event.preventDefault();
    if (!uuidPattern.test(unitId.trim())) {
      setListError('Enter a valid unit UUID.');
      return;
    }
    setSelected(null);
    setDetailError('');
    detailRequest.current++;
    setOpening(false);
    loadReports(unitId.trim());
  }

  async function submitReport(event) {
    event.preventDefault();
    setSubmitError('');
    setNotice('');
    if (!uuidPattern.test(unitId.trim()) || !uuidPattern.test(tenantId.trim())) {
      setSubmitError('Enter valid unit and tenant UUIDs before submitting.');
      return;
    }
    if (!title.trim() || !description.trim()) {
      setSubmitError('A title and description are required.');
      return;
    }
    setSaving(true);
    try {
      const report = await fetch('/api/reports', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title.trim(), description: description.trim(), unit_id: unitId.trim(), tenant_id: tenantId.trim() }),
      }).then(readResponse);
      detailRequest.current++;
      setSelected(report);
      setDetailError('');
      setOpening(false);
      setTitle('');
      setDescription('');
      setNotice('Report submitted. The active list is being refreshed.');
      await loadReports(unitId.trim());
    } catch (error) {
      setSubmitError(error.message);
    } finally {
      setSaving(false);
    }
  }

  async function openReport(id) {
    const request = ++detailRequest.current;
    setOpening(true);
    setSelected(null);
    setDetailError('');
    try {
      const report = await fetch(`/api/reports/${encodeURIComponent(id)}`, { cache: 'no-store' }).then(readResponse);
      if (request === detailRequest.current) setSelected(report);
    } catch (error) {
      if (request === detailRequest.current) setDetailError(error.message);
    } finally {
      if (request === detailRequest.current) setOpening(false);
    }
  }

  return (
    <div className="report-dashboard">
      <section className="report-panel" aria-labelledby="unit-heading">
        <h2 id="unit-heading">Choose a test unit</h2>
        <p>Login is not implemented yet. Use existing unit and tenant UUIDs from the team’s test database. These fields do not verify identity or grant secure access.</p>
        <form onSubmit={showReports}>
          <div className="identity-fields">
            <label htmlFor="unit-id">Unit UUID
              <input id="unit-id" value={unitId} onChange={(e) => changeUnit(e.target.value)} disabled={saving} required autoComplete="off" />
            </label>
            <label htmlFor="tenant-id">Tenant UUID <span className="field-hint">Required to submit a report</span>
              <input id="tenant-id" value={tenantId} onChange={(e) => setTenantId(e.target.value)} disabled={saving} autoComplete="off" />
            </label>
          </div>
          <button type="submit" disabled={loading || saving}>{loading ? 'Loading reports…' : 'Load active reports'}</button>
        </form>
      </section>

      <div className="report-columns">
        <section className="report-panel" aria-labelledby="submit-heading">
          <h2 id="submit-heading">Submit a maintenance report</h2>
          <form onSubmit={submitReport}>
            <label htmlFor="report-title">Title
              <input id="report-title" value={title} onChange={(e) => setTitle(e.target.value)} disabled={saving} required />
            </label>
            <label htmlFor="report-description">Description
              <textarea id="report-description" rows="5" value={description} onChange={(e) => setDescription(e.target.value)} disabled={saving} required />
            </label>
            <button type="submit" disabled={saving}>{saving ? 'Submitting…' : 'Submit report'}</button>
          </form>
          {submitError && <p role="alert" className="error-text">{submitError}</p>}
          {notice && <p role="status" className="success-text">{notice}</p>}
        </section>

        <section className="report-panel" aria-labelledby="active-heading">
          <h2 id="active-heading">Active reports</h2>
          {loading && <p role="status">Loading reports…</p>}
          {listError && <p role="alert" className="error-text">{listError}</p>}
          {!loading && !listError && reports === null && <p>Choose a unit and load its reports.</p>}
          {!loading && reports?.length === 0 && <p>No active reports for this unit.</p>}
          {!loading && reports?.length > 0 && <ul className="report-list">
            {reports.map((report) => <li key={report.id}>
              <button className="report-link" type="button" onClick={() => openReport(report.id)}>{report.title || report.description}</button>
              <p><span className="status-label">{statusLabel(report.status)}</span> · {submissionDate(report)}</p>
            </li>)}
          </ul>}
        </section>
      </div>

      <section className="report-panel" aria-labelledby="details-heading" aria-busy={opening}>
        <h2 id="details-heading">Report details</h2>
        {opening && <p role="status">Loading report details…</p>}
        {detailError && <p role="alert" className="error-text">{detailError}</p>}
        {!opening && !detailError && !selected && <p>Open a report from the active list to see its current status and planned fix.</p>}
        {selected && <div>
          <h3>{selected.title || 'Maintenance report'}</h3>
          <p className="report-description">{selected.description}</p>
          <dl>
            <dt>Status</dt><dd>{statusLabel(selected.status)}</dd>
            <dt>Submitted</dt><dd>{submissionDate(selected)}</dd>
            <dt>Planned fix</dt><dd>{selected.planned_fix_note || 'No planned fix has been added yet.'}</dd>
          </dl>
        </div>}
      </section>
    </div>
  );
}
