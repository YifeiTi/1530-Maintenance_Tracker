import ReportDashboard from '../components/ReportDashboard';

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#main">Skip to content</a>
      <header className="site-header">
        <a className="brand" href="/">Maintenance Tracker</a>
        <span className="team-name">Team Penguins</span>
      </header>
      <main id="main">
        <section className="intro" aria-labelledby="page-title">
          <p className="eyebrow">Apartment maintenance in one place</p>
          <h1 id="page-title">Report a problem. Follow the repair.</h1>
          <p className="intro-text">Submit a maintenance issue and see its status, submission date, and planned fix.</p>
        </section>
        <ReportDashboard />
      </main>
      <footer>Maintenance Tracker · Sprint 5 report screens</footer>
    </>
  );
}
