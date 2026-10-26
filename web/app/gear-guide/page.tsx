'use client';
import {useState} from 'react';
const API=process.env.NEXT_PUBLIC_GATEWAY_URL || 'http://127.0.0.1:8000';
type Recommendation={sku:string;name:string;brand:string;price_usd:number;available_to_promise:number;reason:string};
export default function GearGuide(){
  const [message,setMessage]=useState('Waterproof safety toe work boots for under $160');
  const [store_id,setStore]=useState('BBW-004');const [max_price_usd,setBudget]=useState(160);
  const [answer,setAnswer]=useState<{recommendations:Recommendation[];disclaimer?:string} | null>(null);
  const [error,setError]=useState(''); const [busy,setBusy]=useState(false);
  async function ask(e:React.FormEvent){e.preventDefault();setBusy(true);setError('');setAnswer(null);try {
    const res=await fetch(`${API}/api/assistant/recommend`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message,store_id,max_price_usd})});
    const json=await res.json();if(!res.ok)throw new Error(typeof json.detail==='string'?json.detail:'Request failed');setAnswer(json);
  }catch(err){setError(err instanceof Error?err.message:String(err))}finally{setBusy(false)}}
  return <main className="shell"><div className="eyebrow">STOREFRONT EXPERIENCE / PILOT</div><div className="hero"><div><h1>Find the right gear.</h1><p>Product advice tied to live inventory and your local store. Mock AI provider — no external API calls.</p></div><div className="labelbox"><small>WORK ITEM</small><b>BBWW-2460</b><span>Ground the AI results</span></div></div>
    <div className="grid"><section className="panel pad"><h2>Ask the gear advisor</h2><p className="sub">Tell us your trade, the job site conditions and the gear you need.</p><form onSubmit={ask}><label htmlFor="message">WHAT DO YOU NEED?</label><textarea id="message" rows={5} value={message} onChange={e=>setMessage(e.target.value)}/><div className="formrow"><div><label htmlFor="store">PICKUP LOCATION</label><select id="store" value={store_id} onChange={e=>setStore(e.target.value)}><option value="BBW-004">Rocklin</option><option value="BBW-001">Sacramento</option><option value="BBW-002">West Sacramento</option></select></div><div><label htmlFor="budget">BUDGET (USD)</label><input id="budget" type="number" min="1" value={max_price_usd} onChange={e=>setBudget(Number(e.target.value))}/></div></div><button disabled={busy||message.trim().length<3}>{busy?'Checking availability…':'Find my gear →'}</button></form></section>
    <aside className="panel pad"><h2>Recommended gear</h2>{error&&<div className="error">{error}</div>}{!answer&&!error&&<p className="sub">Ask a question to preview recommendations. Only products verified against the catalog and store availability should appear here.</p>}{answer?.recommendations.length===0&&<p>No verified inventory matches. Try another store or budget.</p>}{answer?.recommendations.map(r=><div className="gearitem" key={r.sku}><small>{r.sku}</small><h3>{r.brand} · {r.name}</h3><div className="row"><b>${r.price_usd.toFixed(2)}</b><span>{r.available_to_promise} available for pickup</span></div><p>{r.reason}</p></div>)}<div className="note"><b>Catalog-grounding requirement</b><p>LLM suggestions are candidates, not facts. Never invent a SKU, price or in-stock claim from a model response.</p></div></aside></div></main>;
}
