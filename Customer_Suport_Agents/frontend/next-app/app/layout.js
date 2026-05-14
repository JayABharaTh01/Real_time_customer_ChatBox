import './globals.css';

export const metadata = {
  title: 'Customer Support Agent - Next.js',
  description: 'Multi-agent customer support app connected to backend API'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}