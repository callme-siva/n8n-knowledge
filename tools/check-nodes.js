// Deep check: every node type, typeVersion, parameter and option exists in a real n8n install.
// Usage (see docs/testing.md): npm i n8n && node tools/check-nodes.js workflows/*/workflow.json
const fs=require('fs'),path=require('path');
const pkgs={'n8n-nodes-base':'n8n-nodes-base','@n8n/n8n-nodes-langchain':'@n8n/n8n-nodes-langchain'};
const reg={};
for(const [prefix,p] of Object.entries(pkgs)){
  const pkgJson=require.resolve(p+'/package.json',{paths:[process.cwd()]});
  const dir=path.dirname(pkgJson);
  const pj=require(pkgJson);
  for(const f of pj.n8n.nodes){
    try{const m=require(path.join(dir,f));for(const C of Object.values(m)){if(typeof C!=='function')continue;let inst;try{inst=new C()}catch{continue}
      const descs=[];
      if(inst.nodeVersions){for(const [v,n] of Object.entries(inst.nodeVersions))descs.push([v,n.description]);}
      else if(inst.description){const vs=[].concat(inst.description.version);vs.forEach(v=>descs.push([v,inst.description]));}
      for(const [v,d] of descs){const name=prefix+'.'+(d.name||inst.description?.name);(reg[name]=reg[name]||{})[String(Number(v))]=d;}
    }}catch(e){}
  }
}
let bad=0;
for(const f of process.argv.slice(2)){
  const wf=JSON.parse(fs.readFileSync(f));const errs=[];
  for(const n of wf.nodes){
    const t=reg[n.type];
    if(!t){errs.push(`unknown type ${n.type}`);continue;}
    const d=t[String(n.typeVersion)];
    if(!d){errs.push(`${n.name}: version ${n.typeVersion} not in [${Object.keys(t)}]`);continue;}
    const props=new Set(d.properties.map(p=>p.name));
    for(const [k,v] of Object.entries(n.parameters)){
      const optDefs=d.properties.filter(p=>p.name===k&&p.type==='options');
      if(optDefs.length&&typeof v==='string'&&!v.startsWith('=')){const allowed=new Set(optDefs.flatMap(p=>(p.options||[]).map(o=>o.value)));
        if(allowed.size&&!allowed.has(v))errs.push(`${n.name}: '${k}' = '${v}' not in [${[...allowed].slice(0,12).join(', ')}]`);}
    }
    for(const k of Object.keys(n.parameters)){ if(!props.has(k)&&k!=='pollTimes'){errs.push(`${n.name}: unknown param '${k}'`);continue;}
      const defs=d.properties.filter(p=>p.name===k&&p.type==='collection');
      const v=n.parameters[k];
      if(defs.length&&v&&typeof v==='object'){const kids=new Set(defs.flatMap(p=>(p.options||[]).map(o=>o.name)));
        for(const kk of Object.keys(v)) if(!kids.has(kk)) errs.push(`${n.name}: unknown option '${k}.${kk}'`);}
    }
  }
  console.log((errs.length?'✗ ':'✓ ')+path.basename(f)+errs.map(e=>'\n   - '+e).join(''));bad+=errs.length;
}
console.log(bad+' issues');
