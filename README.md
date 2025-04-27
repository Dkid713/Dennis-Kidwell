<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Cross-Sell / Vendor-Swap Tool</title>

<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="theme-color" content="#1769ff">

<style>
body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:20px;}
table{border-collapse:collapse;width:100%;margin-top:12px;}
th,td{border:1px solid #ccc;padding:4px 6px;font-size:13px;}
th{background:#eee;position:sticky;top:0;}
#gapChart{max-height:340px;margin-top:20px;}
</style>

<script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script type="module" src="affinity-scores.js"></script>
</head>

<body>
<h2>Cross-Sell / Vendor-Swap Tool</h2>
<input type="file" id="fileCsv" accept=".csv">
<small>(choose your Phocas CSV export)</small>

<div id="status" style="margin-top:10px;font-weight:bold;"></div>
<table id="tbl"></table>
<canvas id="gapChart"></canvas>

<script type="module">
import { score } from './affinity-scores.js';
const GOOD_TYPES=['PREM','STRA','TSTR'], MIN_GAP=1;
function pick(row,want){want=want.map(x=>x.toLowerCase().trim());
for(const k of Object.keys(row)){if(want.includes(k.toLowerCase().trim()))return k;}return null;}

document.getElementById('fileCsv').addEventListener('change',e=>{
 const f=e.target.files[0];if(!f)return;
 document.getElementById('status').textContent='Parsing…';
 Papa.parse(f,{header:true,skipEmptyLines:true,complete:r=>build(r.data)});
});

function build(rows){
 if(!rows.length){document.getElementById('status').textContent='CSV empty';return;}
 const map={cust:pick(rows[0],['National Account Code']),
            cat: pick(rows[0],['Product Category Product Category Description']),
            typ: pick(rows[0],['Vendor Vendor Type']),
            val: pick(rows[0],['Sales','Total Sales'])};
 if(Object.values(map).includes(null)){document.getElementById('status').textContent='Missing column';return;}

 const data={};
 rows.forEach(r=>{
   const c=(r[map.cust]||'').trim(),cat=(r[map.cat]||'').trim(),
         t=(r[map.typ]||'').trim(),v=+(String(r[map.val]).replace(/[^0-9.\-]/g,''))||0;
   if(!c||!cat||!v) return;
   data[c]??={}; data[c][cat]??={g:0,b:0};
   (GOOD_TYPES.includes(t)?data[c][cat].g:data[c][cat].b)+=v;
 });

 const gaps=[];
 for(const [cust,cCats] of Object.entries(data)){
   let anchor=null,max=0;
   for(const [cat,val] of Object.entries(cCats)){const tot=val.g+val.b;if(tot>max){max=tot;anchor=cat;}}
   for(const [tgt,pct] of Object.entries(score[anchor]||{})){
     const expect=max*pct/100, g=cCats[tgt]?.g||0, b=cCats[tgt]?.b||0, gap=Math.max(0,expect-g);
     if(gap<MIN_GAP&&b<MIN_GAP)continue;
     gaps.push({c:cust,a:anchor,t:tgt,e:Math.round(expect),b$:Math.round(b),
                bp:((b/(g+b)||0)*100).toFixed(0)+'%',g$:Math.round(gap),
                ac:b>0?'Replace vendor':'Upsell preferred'});
   }
 }

 gaps.sort((x,y)=>y.g$-x.g$);
 const tbl=document.getElementById('tbl');tbl.innerHTML=
   '<thead><tr><th>Customer</th><th>Anchor</th><th>Category</th><th>Expected $</th>'+
   '<th>Bad $</th><th>Bad %</th><th>Gap $</th><th>Action</th></tr></thead><tbody>'+
   gaps.map(g=>`<tr><td>${g.c}</td><td>${g.a}</td><td>${g.t}</td><td>${g.e}</td><td>${g.b$}</td>`+
   `<td>${g.bp}</td><td>${g.g$}</td><td>${g.ac}</td></tr>`).join('')+'</tbody>';

 document.getElementById('status').textContent=gaps.length+' opportunities found';

 const ctx=document.getElementById('gapChart').getContext('2d');
 if(window.gapChart) window.gapChart.destroy();
 window.gapChart=new Chart(ctx,{type:'bar',
   data:{labels:gaps.slice(0,15).map(x=>x.c+' ▸ '+x.t),
         datasets:[{label:'Gap $',data:gaps.slice(0,15).map(x=>x.g$)}]},
   options:{plugins:{legend:{display:false}},
            scales:{y:{beginAtZero:true,ticks:{callback:v=>'$'+v.toLocaleString()}}}}});
}

if('serviceWorker' in navigator){navigator.serviceWorker.register('service-worker.js');}
</script>
</body>
</html>
