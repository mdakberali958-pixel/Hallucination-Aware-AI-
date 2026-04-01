import React, {useState} from 'react'

export default function App(){
  const [q,setQ]=useState('')
  const [mode,setMode]=useState('standard')
  const [resp,setResp]=useState(null)

  const ask=async()=>{
    const r=await fetch('http://localhost:8000/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q,mode})})
    setResp(await r.json())
  }

  return (
    <div className="p-6 grid grid-cols-3 gap-4">
      <div className="col-span-2">
        <input className="w-full p-3 bg-slate-800 rounded" value={q} onChange={e=>setQ(e.target.value)} placeholder="Ask..."/>
        <div className="mt-2 flex gap-2">
          <select className="bg-slate-800 p-2" value={mode} onChange={e=>setMode(e.target.value)}>
            <option value="standard">Standard</option>
            <option value="rag">RAG</option>
          </select>
          <button className="bg-indigo-600 px-4 py-2 rounded" onClick={ask}>Ask</button>
        </div>
        {resp && <div className="mt-4 bg-slate-800 p-4 rounded">
          <p>{resp.answer}</p>
          <div className="mt-2 text-green-400">Risk: {resp.analysis.risk_score}%</div>
        </div>}
      </div>

      <div className="bg-slate-800 p-4 rounded">
        <h2 className="text-xl">Reliability</h2>
        {resp && <>
          <div className="text-3xl text-green-400">{resp.analysis.confidence}%</div>
          <div className="mt-2">
            <p>Document: {resp.analysis.metrics.document_support}%</p>
            <p>Consistency: {resp.analysis.metrics.semantic_consistency}%</p>
            <p>Claims: {resp.analysis.metrics.fact_claim_verification}%</p>
          </div>
        </>}
      </div>
    </div>
  )
}
