let latest = {};
const fmt = v => typeof v === 'number' ? v.toFixed(1) : String(v).toUpperCase();
async function post(id,value){await fetch('/api/simulator/'+id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({value})});await refresh();}
async function refresh(){
  const [status,tags,alarms] = await Promise.all([fetch('/api/status').then(r=>r.json()),fetch('/api/tags').then(r=>r.json()),fetch('/api/alarms').then(r=>r.json())]);
  document.getElementById('driver').textContent=status.driver;
  document.getElementById('alarm-count').textContent=status.active_alarms;
  latest=Object.fromEntries(tags.map(t=>[t.tag_id,t]));
  const cardIds=['tank_level','line_pressure','process_temp','flow_rate'];
  document.getElementById('cards').innerHTML=cardIds.map(id=>{const t=latest[id];return '<article class="card"><span class="quality">'+t.quality+'</span><div class="label">'+t.definition.name+'</div><div class="value">'+fmt(t.value)+'</div><div class="unit">'+t.definition.unit+'</div></article>';}).join('');
  document.getElementById('tank-fill').style.height=Math.max(3,Math.min(97,latest.tank_level.value))+'%';
  document.getElementById('pump').classList.toggle('fault',latest.pump_01_fault.value||latest.emergency_stop.value);
  const active=alarms.filter(a=>a.active);
  document.getElementById('alarms').innerHTML=active.length?active.map(a=>'<div class="alarm active"><span class="lamp"></span><div><strong>'+a.message+'</strong><small>'+a.tag_id+': '+a.value+'</small></div><span class="sev">'+a.severity+'</span></div>').join(''):'<div class="empty">No active alarms</div>';
}
document.getElementById('toggle-pump').onclick=()=>post('pump_01_run',!latest.pump_01_run.value);
document.getElementById('fault-pump').onclick=()=>post('pump_01_fault',!latest.pump_01_fault.value);
document.getElementById('estop').onclick=()=>post('emergency_stop',!latest.emergency_stop.value);
refresh(); setInterval(refresh,2000);
