import FeatureCard from '../components/FeatureCard';

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
          <h1 id="page-title">Keep everyone updated on the same issue.</h1>
          <p className="intro-text">
            A shared place for tenants and landlords to report problems,
            follow repairs, and keep track of what has been done.
          </p>
          <p className="setup-note">
            This is the Sprint 4 homepage. Account access, reports, and chat
            are planned and are not connected yet.
          </p>
        </section>

        <section aria-labelledby="features-title">
          <div className="section-heading">
            <h2 id="features-title">What you will be able to do</h2>
            <span className="planned-label">Planned features</span>
          </div>
          <div className="feature-grid">
            <FeatureCard title="Report an issue">
              Tenants will be able to submit a short description of a
              maintenance problem for their unit.
            </FeatureCard>
            <FeatureCard title="Follow the progress">
              Roommates will share an active report list and see whether an
              issue is Submitted, In progress, or Resolved.
            </FeatureCard>
            <FeatureCard title="Keep the conversation together">
              Each request will have its own chat, so messages about a repair
              stay with the report.
            </FeatureCard>
          </div>
        </section>

        <section className="roles" aria-labelledby="roles-title">
          <h2 id="roles-title">For tenants and landlords</h2>
          <p>
            Tenants will see reports for their unit. Landlords will review
            reports for their property, update statuses, and share planned fixes.
            Resolved reports and their history will remain available.
          </p>
        </section>
      </main>
      <footer>Maintenance Tracker · Sprint 4 frontend setup</footer>
    </>
  );
}
