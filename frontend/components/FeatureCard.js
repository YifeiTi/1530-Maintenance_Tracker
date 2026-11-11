export default function FeatureCard({ title, children }) {
  return (
    <article className="feature-card">
      <h3>{title}</h3>
      <p>{children}</p>
    </article>
  );
}
