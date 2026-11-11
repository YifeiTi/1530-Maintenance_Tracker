import './globals.css';

export const metadata = {
  title: 'Maintenance Tracker',
  description: 'Shared maintenance reports for tenants and landlords.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
