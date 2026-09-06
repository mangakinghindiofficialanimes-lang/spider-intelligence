import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Spider Intelligence",
  description:
    "An open-source, modular, local-first artificial intelligence platform."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
