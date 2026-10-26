'use client';
import {useEffect,useState} from 'react';
type Exception = {severity:string;store_id:string;store:string;lag_minutes:number;message:string};
type Inventory = {sku:string;product:string;on_hand:number;active_store_holds:number;web_commitments:number;available_to_promise:number;snapshot_at:string};
const API=process.env.NEXT_PUBLIC_GATEWAY_URL || 'http://127.0.0.1:8000';
export default function OpsPage(){
  const [exceptions,setExceptions]=useState<Exception[]>([]),[inventory,setInventory]=useState<Inventory[]>([]),[error,setError]=useState('');
  useEffect(()=>{Promise.all([
    fetch(`${API}/api/ops/pos-sync-exceptions`).then(r=>r.json()),
    fetch(`${API}/api/inventory/BBW-004?limit=80`).then(r=>r.json())
  ]).then(([ops,inv])=>{setExceptions(ops.exceptions || []);setInventory(inv.items || [])}).catch(()=>setError('Gateway unavailable. Start the API with make run.'))},[]);
  return <main className="shell"><div className="eyebrow">OPERATIONS / NORTHERN CALIFORNIA</div>
   <div className="hero"><div><h1>Fulfillment workbench</h1><p>Inventory promise, sync health and store handoff. Fixture snapshot: Oct 26, 2026 · 08:30 PT</p></div><div className="labelbox"><small>RELEASE TRAIN</small><b>2026.10 / RC-2</b><span>BBWW-2418 under review</span></div></div>
   {error && <div className="error">{error}</div>}
   <section className="metrics"><article><small>CONNECTED STORES</small><strong>10</strong><span>POS ↔ Gateway</span></article><article><small>SYNC EXCEPTIONS</small><strong>{exceptions.length}</strong><span>Stale import batches</span></article><article><small>ROCKLIN SKU COUNT</small><strong>{inventory.length}</strong><span>Availability projection</span></article><article><small>OPEN INCIDENT</small><strong>2418</strong><span>Online promise mismatch</span></article></section>
   <div className="grid"><section className="panel"><div className="sectionhead"><h2>Rocklin • Available to Promise</h2><span>BBW-004</span></div><p className="sub">Combines POS on-hand, in-store holds and web orders. Rows below expose the known incident.</p><div className="tablewrap"><table><thead><tr><th>SKU / PRODUCT</th><th>PHYSICAL</th><th>STORE HOLDS</th><th>WEB</th><th>ATP</th></tr></thead><tbody>{inventory.slice(0,16).map(i=><tr key={i.sku}><td><b>{i.sku}</b><span>{i.product}</span></td><td>{i.on_hand}</td><td>{i.active_store_holds}</td><td>{i.web_commitments}</td><td><strong>{i.available_to_promise}</strong></td></tr>)}</tbody></table></div></section>
   <aside className="panel"><div className="sectionhead"><h2>Integration monitor</h2><span>LAST RUN 08:30</span></div><div className="feed"><div className="ok">● 09 retail locations reporting on time</div>{exceptions.map(x=><div className="incident" key={x.store_id}><div className="severity">{x.severity.toUpperCase()} · {x.store_id}</div><b>{x.store} POS snapshot late</b><p>{x.message}</p><small>Route to: Retail Systems / Integration</small></div>)}<div className="note"><strong>Handoff note</strong><p>Product availability drives marketplace feeds and the Gear Advisor. Incorrect ATP can oversell an item that's already committed to pickup.</p></div></div></aside></div>
  </main>
}
