export default function Dashboard() {
  const cards = [
    ['Open Issues', '165, 166, 167'],
    ['Build Queue', '3 active tasks'],
    ['Pull Requests', '0 open'],
    ['Agent Reports', 'Bootstrap only'],
    ['Themis Gate', 'Safe Mode Enabled']
  ];

  return (
    <main style={{padding:'32px',fontFamily:'sans-serif'}}>
      <h1>Daedalus Workshop</h1>
      <p>Standalone Mnemosyne Factory.</p>
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))',gap:'16px'}}>
        {cards.map(([title,value]) => (
          <section key={title} style={{border:'1px solid #333',padding:'16px',borderRadius:'12px'}}>
            <h3>{title}</h3>
            <p>{value}</p>
          </section>
        ))}
      </div>
    </main>
  );
}
