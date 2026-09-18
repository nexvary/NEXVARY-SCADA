const I18N={
en:{subtitle:"Industrial Monitoring & Control Platform",overview:"Overview",hmi:"HMI",devices:"Devices",alarms:"Alarms",historian:"Historian",audit:"Audit",settings:"Settings",about:"About",nuclearScope:"Nuclear profile",nonSafety:"Non-safety monitoring only",overviewTitle:"Operations Overview",overviewText:"Unified live view across configured devices and the built-in process simulator.",activeAlarms:"ACTIVE ALARMS",processMimic:"PROCESS MIMIC",startStop:"START / STOP PUMP",toggleFault:"TOGGLE FAULT",alarmConsole:"ALARM CONSOLE",hmiText:"Live tag workspace with quality, units and device source.",devicesText:"Configured drivers, health and write policy.",alarmsText:"Active and cleared events with operator acknowledgement.",historianText:"Select a numeric tag to inspect recent recorded samples.",auditText:"Operator writes, denied actions and alarm acknowledgements.",operator:"Operator",role:"Role",writeSafety:"Write safety:",writeSafetyText:"Real-device writes remain blocked by the server kill-switch even when this screen selects an operator role.",nuclearNotice:"Nuclear support is restricted to non-safety monitoring, simulation, training, historian, maintenance and auxiliary systems."},
ar:{subtitle:"منصة المراقبة والتحكم الصناعي",overview:"نظرة عامة",hmi:"واجهة التشغيل",devices:"الأجهزة",alarms:"الإنذارات",historian:"السجل الزمني",audit:"سجل العمليات",settings:"الإعدادات",about:"عنا",nuclearScope:"ملف الطاقة النووية",nonSafety:"مراقبة غير مصنفة للسلامة فقط",overviewTitle:"نظرة عامة على التشغيل",overviewText:"عرض حي موحد للأجهزة المهيأة ومحاكي العمليات المدمج.",activeAlarms:"إنذارات نشطة",processMimic:"مخطط العملية",startStop:"تشغيل / إيقاف المضخة",toggleFault:"تبديل حالة العطل",alarmConsole:"لوحة الإنذارات",hmiText:"عرض حي للوسوم والقيم والجودة والوحدة ومصدر الجهاز.",devicesText:"التعريفات وحالة الاتصال وسياسة الكتابة لكل جهاز.",alarmsText:"الإنذارات النشطة والمنتهية مع تأكيد المشغل.",historianText:"اختر قيمة رقمية لعرض العينات المسجلة حديثاً.",auditText:"عمليات الكتابة والرفض وتأكيد الإنذارات.",operator:"المشغل",role:"الصلاحية",writeSafety:"أمان الكتابة:",writeSafetyText:"الكتابة إلى الأجهزة الحقيقية تظل محجوبة بقفل الخادم حتى مع اختيار صلاحية مشغل هنا.",nuclearNotice:"دعم القطاع النووي مقصور على المراقبة غير الحرجة والمحاكاة والتدريب والسجل والصيانة والأنظمة المساندة."},
tr:{overview:"Genel Bakış",hmi:"HMI",devices:"Cihazlar",alarms:"Alarmlar",historian:"Geçmiş",audit:"Denetim",settings:"Ayarlar",about:"Hakkında"},
es:{overview:"Resumen",hmi:"HMI",devices:"Dispositivos",alarms:"Alarmas",historian:"Histórico",audit:"Auditoría",settings:"Ajustes",about:"Acerca de"},
de:{overview:"Übersicht",hmi:"HMI",devices:"Geräte",alarms:"Alarme",historian:"Historian",audit:"Audit",settings:"Einstellungen",about:"Info"},
it:{overview:"Panoramica",hmi:"HMI",devices:"Dispositivi",alarms:"Allarmi",historian:"Storico",audit:"Audit",settings:"Impostazioni",about:"Informazioni"},
fr:{overview:"Vue générale",hmi:"IHM",devices:"Appareils",alarms:"Alarmes",historian:"Historique",audit:"Audit",settings:"Paramètres",about:"À propos"},
ur:{overview:"جائزہ",hmi:"HMI",devices:"آلات",alarms:"الارم",historian:"تاریخ",audit:"آڈٹ",settings:"ترتیبات",about:"تعارف"},
fa:{overview:"نمای کلی",hmi:"HMI",devices:"دستگاه‌ها",alarms:"هشدارها",historian:"تاریخچه",audit:"ممیزی",settings:"تنظیمات",about:"درباره"},
ru:{overview:"Обзор",hmi:"HMI",devices:"Устройства",alarms:"Тревоги",historian:"Архив",audit:"Аудит",settings:"Настройки",about:"О системе"}
};
let latest={},alarms=[],definitions=[],devices=[];
const $=id=>document.getElementById(id);
const escapeHtml=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const operatorHeaders=()=>({"Content-Type":"application/json","X-Operator":$("operator").value||"local-operator","X-Role":$("role").value||"viewer"});
const fmt=v=>typeof v==="number"?(Math.abs(v)>=100?v.toFixed(0):v.toFixed(1)):String(v).toUpperCase();

function setLocale(locale){
  localStorage.setItem("nexvary-scada-locale",locale);
  const rtl=["ar","ur","fa"].includes(locale);
  document.documentElement.lang=locale;document.documentElement.dir=rtl?"rtl":"ltr";
  const dict={...I18N.en,...(I18N[locale]||{})};
  document.querySelectorAll("[data-i18n]").forEach(el=>{const key=el.dataset.i18n;if(dict[key])el.textContent=dict[key]});
}
function navigate(page){
  document.querySelectorAll(".page").forEach(x=>x.classList.toggle("active",x.id==="page-"+page));
  document.querySelectorAll(".nav").forEach(x=>x.classList.toggle("active",x.dataset.page===page));
  history.replaceState(null,"","#"+page);
  if(page==="historian")loadTrend();
  if(page==="audit")loadAudit();
}
async function api(url,options){
  const response=await fetch(url,options);
  if(!response.ok){let detail="Request failed";try{detail=(await response.json()).detail||detail}catch{}throw new Error(detail)}
  return response.json();
}
async function writeTag(id,value){
  try{await api("/api/write/"+encodeURIComponent(id),{method:"POST",headers:operatorHeaders(),body:JSON.stringify({value})});await refresh()}
  catch(error){alert(error.message)}
}
async function ackAlarm(id){
  try{await api("/api/alarms/"+encodeURIComponent(id)+"/ack",{method:"POST",headers:operatorHeaders()});await refresh();await loadAudit()}
  catch(error){alert(error.message)}
}
function renderCards(){
  const preferred=["tank_level","line_pressure","process_temp","flow_rate"].filter(id=>latest[id]);
  const ids=preferred.length?preferred:Object.keys(latest).filter(id=>typeof latest[id].value==="number").slice(0,4);
  $("cards").innerHTML=ids.map(id=>{const t=latest[id];return '<article class="card"><span class="quality '+t.quality+'">'+escapeHtml(t.quality)+'</span><div class="label">'+escapeHtml(t.definition.name)+'</div><div class="value">'+escapeHtml(fmt(t.value))+'</div><div class="unit">'+escapeHtml(t.definition.unit)+'</div></article>'}).join("")||'<div class="empty">No numeric tags</div>';
}
function renderOverview(){
  const tank=latest.tank_level;if(tank)$("tank-fill").style.height=Math.max(3,Math.min(97,Number(tank.value)||0))+"%";
  const fault=latest.pump_01_fault?.value||latest.emergency_stop?.value;$("pump").classList.toggle("fault",Boolean(fault));
  const active=alarms.filter(a=>a.active);$("alarm-count").textContent=active.length;
  $("overview-alarms").innerHTML=active.length?active.slice(0,7).map(a=>'<div class="alarm active"><span class="lamp"></span><div><strong>'+escapeHtml(a.message)+'</strong><small>'+escapeHtml(a.tag_id)+': '+escapeHtml(a.value)+'</small></div><span class="sev">'+escapeHtml(a.severity)+'</span></div>').join(""):'<div class="empty">No active alarms</div>';
}
function renderTags(){
  const rows=Object.values(latest).map(t=>'<tr><td>'+escapeHtml(t.definition.name)+'</td><td><b>'+escapeHtml(fmt(t.value))+'</b></td><td>'+escapeHtml(t.definition.unit)+'</td><td><span class="badge '+(t.quality==="GOOD"?"ok":"bad")+'">'+escapeHtml(t.quality)+'</span></td><td>'+escapeHtml(t.device_id)+'</td><td>'+escapeHtml(t.definition.source)+'</td></tr>').join("");
  $("tag-table").innerHTML='<table class="data-table"><thead><tr><th>TAG</th><th>VALUE</th><th>UNIT</th><th>QUALITY</th><th>DEVICE</th><th>SOURCE</th></tr></thead><tbody>'+rows+'</tbody></table>';
}
function renderDevices(){
  $("device-grid").innerHTML=devices.map(d=>'<article class="device-card"><span class="badge '+(d.health.connected?"ok":"bad")+'">'+(d.health.connected?"ONLINE":"OFFLINE")+'</span><h3>'+escapeHtml(d.name)+'</h3><p>'+escapeHtml(d.description)+'</p><div class="device-meta"><div><span>DRIVER</span><b>'+escapeHtml(d.driver)+'</b></div><div><span>TAGS</span><b>'+d.tag_count+'</b></div><div><span>WRITES</span><b>'+ (d.writes_enabled?"DEVICE ENABLED":"BLOCKED")+'</b></div><div><span>HEALTH</span><b>'+escapeHtml(d.health.detail)+'</b></div></div></article>').join("");
}
function renderAlarms(){
  const rows=alarms.map(a=>'<tr><td><span class="badge '+(a.active?"bad":"ok")+'">'+(a.active?"ACTIVE":"CLEARED")+'</span></td><td>'+escapeHtml(a.severity)+'</td><td>'+escapeHtml(a.message)+'</td><td>'+escapeHtml(a.value)+'</td><td>'+escapeHtml(a.acknowledged_by||"—")+'</td><td><button class="ack" '+(a.acknowledged?"disabled":"")+' onclick="ackAlarm(\''+escapeHtml(a.rule_id)+'\')">'+(a.acknowledged?"ACKED":"ACK")+'</button></td></tr>').join("");
  $("alarm-table").innerHTML='<table class="data-table"><thead><tr><th>STATE</th><th>SEVERITY</th><th>MESSAGE</th><th>VALUE</th><th>ACK BY</th><th>ACTION</th></tr></thead><tbody>'+rows+'</tbody></table>';
}
function populateTrendTags(){
  const current=$("trend-tag").value;
  const numeric=Object.values(latest).filter(t=>typeof t.value==="number");
  $("trend-tag").innerHTML=numeric.map(t=>'<option value="'+escapeHtml(t.tag_id)+'">'+escapeHtml(t.definition.name)+'</option>').join("");
  if(numeric.some(t=>t.tag_id===current))$("trend-tag").value=current;
}
async function loadTrend(){
  const tag=$("trend-tag").value;if(!tag)return;
  const rows=await api("/api/history/"+encodeURIComponent(tag)+"?minutes="+$("trend-window").value+"&limit=500");
  const numeric=rows.filter(r=>typeof r.value==="number");
  $("trend-empty").textContent=numeric.length<2?"Waiting for more samples…":"";
  drawTrend(numeric);
}
function drawTrend(rows){
  const canvas=$("trend-canvas"),ctx=canvas.getContext("2d"),w=canvas.width,h=canvas.height;ctx.clearRect(0,0,w,h);
  ctx.strokeStyle="#27303a";ctx.lineWidth=1;for(let i=1;i<5;i++){const y=i*h/5;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke()}
  if(rows.length<2)return;
  const vals=rows.map(r=>Number(r.value)),min=Math.min(...vals),max=Math.max(...vals),span=max-min||1;
  ctx.strokeStyle="#d4af37";ctx.lineWidth=3;ctx.beginPath();rows.forEach((r,i)=>{const x=i*(w/(rows.length-1)),y=h-24-((Number(r.value)-min)/span)*(h-48);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke();
  ctx.fillStyle="#9aa5b1";ctx.font="18px Segoe UI";ctx.fillText("max "+max.toFixed(2),14,24);ctx.fillText("min "+min.toFixed(2),14,h-8);
}
async function loadAudit(){
  const rows=await api("/api/audit?limit=200");
  const html=rows.map(r=>'<tr><td>'+escapeHtml(r.timestamp.replace("T"," ").slice(0,19))+'</td><td>'+escapeHtml(r.operator)+'</td><td>'+escapeHtml(r.role)+'</td><td>'+escapeHtml(r.action)+'</td><td>'+escapeHtml(r.target)+'</td><td><span class="badge '+(r.success?"ok":"bad")+'">'+(r.success?"OK":"DENIED")+'</span></td></tr>').join("");
  $("audit-table").innerHTML='<table class="data-table"><thead><tr><th>TIME</th><th>OPERATOR</th><th>ROLE</th><th>ACTION</th><th>TARGET</th><th>RESULT</th></tr></thead><tbody>'+html+'</tbody></table>';
}
async function refresh(){
  try{
    const [status,tags,a,d]=await Promise.all([api("/api/status"),api("/api/tags"),api("/api/alarms"),api("/api/devices")]);
    $("runtime-status").textContent="ONLINE · "+status.device_count+" DEV";
    latest=Object.fromEntries(tags.map(t=>[t.tag_id,t]));alarms=a;devices=d;
    renderCards();renderOverview();renderTags();renderDevices();renderAlarms();populateTrendTags();
  }catch(error){$("runtime-status").textContent="DEGRADED";console.error(error)}
}
document.querySelectorAll(".nav").forEach(btn=>btn.onclick=()=>navigate(btn.dataset.page));
$("locale").value=localStorage.getItem("nexvary-scada-locale")||"en";$("locale").onchange=e=>setLocale(e.target.value);setLocale($("locale").value);
$("operator").value=localStorage.getItem("nexvary-operator")||"local-operator";$("role").value=localStorage.getItem("nexvary-role")||"viewer";
$("operator").onchange=e=>localStorage.setItem("nexvary-operator",e.target.value);$("role").onchange=e=>localStorage.setItem("nexvary-role",e.target.value);
$("toggle-pump").onclick=()=>writeTag("pump_01_run",!latest.pump_01_run?.value);
$("fault-pump").onclick=()=>writeTag("pump_01_fault",!latest.pump_01_fault?.value);
$("estop").onclick=()=>writeTag("emergency_stop",!latest.emergency_stop?.value);
$("trend-tag").onchange=loadTrend;$("trend-window").onchange=loadTrend;
navigate((location.hash||"#overview").slice(1));refresh();setInterval(refresh,2500);
