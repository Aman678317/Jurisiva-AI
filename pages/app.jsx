import React from 'react';
import Head from 'next/head';

export default function AppPage() {
  return (
    <>
      <Head>
        <title>Jurisiva AI — Workspace</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>
      <iframe
        src="/apps/web/index.html"
        style={{
          width: '100vw',
          height: '100vh',
          border: 'none',
          margin: 0,
          padding: 0,
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
        }}
      />
    </>
  );
}
