import './globals.css';
import Link from 'next/link';
import type { Metadata } from 'next';
export const metadata: Metadata = {title:'BBWW | Commerce Operations',description:'Prototype retail operations workbench'};
export default function RootLayout({children}:{children:React.ReactNode}) {
  return <html lang="en"><body><header className="topbar"><div className="mark">BB<span>WW</span></div><div className="brand"><strong>BAREBONES WORKWEAR</strong><small>COMMERCE SYSTEMS / INTERNAL PREVIEW</small></div><nav><Link href="/">Ops Overview</Link><Link href="/gear-guide">Gear Advisor</Link></nav><div className="pill">● SANDBOX</div></header>{children}<footer>BBWW Engineering · Commerce Gateway v0.8.2 · Simulated operational data · Not a production system</footer></body></html>;
}
