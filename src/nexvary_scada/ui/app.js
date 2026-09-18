const I18N={
en:{subtitle:"Industrial Monitoring & Control Platform",overview:"Overview",hmi:"HMI",devices:"Devices",alarms:"Alarms",historian:"Historian",audit:"Audit",settings:"Settings",aboutUs:"About Us",systemInfo:"About System",nuclearScope:"Nuclear profile",nonSafety:"Non-safety monitoring only",overviewTitle:"Operations Overview",overviewText:"Unified live view across configured devices and the built-in process simulator.",activeAlarms:"ACTIVE ALARMS",processMimic:"PROCESS MIMIC",startStop:"START / STOP PUMP",toggleFault:"TOGGLE FAULT",alarmConsole:"ALARM CONSOLE",hmiText:"Live tag workspace with quality, units and device source.",devicesText:"Configured drivers, health and write policy.",alarmsText:"Active and cleared events with operator acknowledgement.",historianText:"Select a numeric tag to inspect recent recorded samples.",auditText:"Operator writes, denied actions and alarm acknowledgements.",operator:"Operator",role:"Role",writeSafety:"Write safety:",writeSafetyText:"Real-device writes remain blocked by the server kill-switch even when this screen selects an operator role.",aboutUsText:"Official NEXVARY channels and contact points.",companyText:"Technology solutions focused on secure, reliable and professionally engineered systems.",systemIntro:"NEXVARY SCADA is an industrial monitoring and control platform designed to unify devices, live process data, alarms, history and operator actions in one interface.",systemMission:"One operations layer for industrial visibility",systemMissionText:"The platform connects to industrial equipment through protocol drivers, converts raw points into structured tags, records history, evaluates alarms and presents operators with a secure HMI.",featureConnectivity:"Industrial Connectivity",featureConnectivityText:"Modbus TCP and Modbus RTU/RS-485 with device and tag mapping.",featureHmi:"HMI & Live Operations",featureHmiText:"Live process mimic, quality states, values, sources and responsive operator views.",featureAlarms:"Alarm Management",featureAlarmsText:"Priority alarms, active/cleared states and operator acknowledgement.",featureHistorian:"Historian & Trends",featureHistorianText:"Recorded process samples, time windows and visual trend inspection.",featureAudit:"Audit & Accountability",featureAuditText:"Records operator writes, denied actions and alarm acknowledgements.",featureSafety:"Write Safety",featureSafetyText:"Role gates, per-device permissions and an independent real-hardware write kill-switch.",featureSimulator:"Built-in Simulator",featureSimulatorText:"A deterministic demo process supports testing before connecting physical PLCs.",featureLanguages:"Multilingual HMI",featureLanguagesText:"Arabic RTL and multilingual navigation for international operator environments.",architecture:"System Architecture",nuclearBoundaryTitle:"Nuclear safety boundary",nuclearNotice:"Nuclear support is restricted to non-safety monitoring, simulation, training, historian, maintenance and auxiliary systems."},
ar:{subtitle:"منصة المراقبة والتحكم الصناعي",overview:"نظرة عامة",hmi:"واجهة التشغيل",devices:"الأجهزة",alarms:"الإنذارات",historian:"السجل الزمني",audit:"سجل العمليات",settings:"الإعدادات",aboutUs:"عنا",systemInfo:"حول النظام",nuclearScope:"ملف الطاقة النووية",nonSafety:"مراقبة غير مصنفة للسلامة فقط",overviewTitle:"نظرة عامة على التشغيل",overviewText:"عرض حي موحد للأجهزة المهيأة ومحاكي العمليات المدمج.",activeAlarms:"إنذارات نشطة",processMimic:"مخطط العملية",startStop:"تشغيل / إيقاف المضخة",toggleFault:"تبديل حالة العطل",alarmConsole:"لوحة الإنذارات",hmiText:"عرض حي للوسوم والقيم والجودة والوحدة ومصدر الجهاز.",devicesText:"التعريفات وحالة الاتصال وسياسة الكتابة لكل جهاز.",alarmsText:"الإنذارات النشطة والمنتهية مع تأكيد المشغل.",historianText:"اختر قيمة رقمية لعرض العينات المسجلة حديثاً.",auditText:"عمليات الكتابة والرفض وتأكيد الإنذارات.",operator:"المشغل",role:"الصلاحية",writeSafety:"أمان الكتابة:",writeSafetyText:"الكتابة إلى الأجهزة الحقيقية تظل محجوبة بقفل الخادم حتى مع اختيار صلاحية مشغل هنا.",aboutUsText:"قنوات NEXVARY الرسمية ووسائل الاتصال بالشركة.",companyText:"حلول تقنية تركز على الأنظمة الآمنة والموثوقة والمصممة هندسياً بصورة احترافية.",systemIntro:"NEXVARY SCADA منصة للمراقبة والتحكم الصناعي توحد الأجهزة وبيانات العمليات الحية والإنذارات والسجل الزمني وإجراءات المشغل داخل واجهة واحدة.",systemMission:"طبقة تشغيل موحدة للرؤية الصناعية",systemMissionText:"يتصل النظام بالمعدات الصناعية عبر مشغلات البروتوكولات، ويحول النقاط الخام إلى وسوم منظمة، ويسجل التاريخ ويقيّم الإنذارات ويعرضها للمشغل عبر HMI آمنة.",featureConnectivity:"الاتصال الصناعي",featureConnectivityText:"دعم Modbus TCP وModbus RTU/RS-485 مع ربط الأجهزة والوسوم.",featureHmi:"واجهة التشغيل والبيانات الحية",featureHmiText:"مخطط عمليات حي وحالات الجودة والقيم والمصادر وواجهات متجاوبة.",featureAlarms:"إدارة الإنذارات",featureAlarmsText:"أولويات وحالات نشطة ومنتهية مع تأكيد المشغل.",featureHistorian:"السجل الزمني والاتجاهات",featureHistorianText:"تسجيل عينات العمليات وعرض الفترات الزمنية والاتجاهات.",featureAudit:"التدقيق والمساءلة",featureAuditText:"تسجيل عمليات الكتابة والإجراءات المرفوضة وتأكيد الإنذارات.",featureSafety:"أمان الكتابة",featureSafetyText:"صلاحيات حسب الدور وإذن لكل جهاز وقفل مستقل للكتابة إلى المعدات الحقيقية.",featureSimulator:"المحاكي المدمج",featureSimulatorText:"محاكاة عملية صناعية تسمح باختبار النظام قبل ربط PLC فعلي.",featureLanguages:"واجهة متعددة اللغات",featureLanguagesText:"دعم العربية RTL والتنقل بعدة لغات لبيئات التشغيل الدولية.",architecture:"معمارية النظام",nuclearBoundaryTitle:"حدود السلامة النووية",nuclearNotice:"دعم القطاع النووي مقصور على المراقبة غير الحرجة والمحاكاة والتدريب والسجل والصيانة والأنظمة المساندة."},
tr:{overview:"Genel Bakış",hmi:"HMI",devices:"Cihazlar",alarms:"Alarmlar",historian:"Geçmiş",audit:"Denetim",settings:"Ayarlar",aboutUs:"Hakkımızda",systemInfo:"Sistem Hakkında"},
es:{overview:"Resumen",hmi:"HMI",devices:"Dispositivos",alarms:"Alarmas",historian:"Histórico",audit:"Auditoría",settings:"Ajustes",aboutUs:"Nosotros",systemInfo:"Sobre el sistema"},
de:{overview:"Übersicht",hmi:"HMI",devices:"Geräte",alarms:"Alarme",historian:"Historian",audit:"Audit",settings:"Einstellungen",aboutUs:"Über uns",systemInfo:"Über das System"},
it:{overview:"Panoramica",hmi:"HMI",devices:"Dispositivi",alarms:"Allarmi",historian:"Storico",audit:"Audit",settings:"Impostazioni",aboutUs:"Chi siamo",systemInfo:"Sul sistema"},
fr:{overview:"Vue générale",hmi:"IHM",devices:"Appareils",alarms:"Alarmes",historian:"Historique",audit:"Audit",settings:"Paramètres",aboutUs:"À propos de nous",systemInfo:"À propos du système"},
ur:{overview:"جائزہ",hmi:"HMI",devices:"آلات",alarms:"الارم",historian:"تاریخ",audit:"آڈٹ",settings:"ترتیبات",aboutUs:"ہمارے بارے میں",systemInfo:"نظام کے بارے میں"},
fa:{overview:"نمای کلی",hmi:"HMI",devices:"دستگاه‌ها",alarms:"هشدارها",historian:"تاریخچه",audit:"ممیزی",settings:"تنظیمات",aboutUs:"درباره ما",systemInfo:"درباره سیستم"},
ru:{overview:"Обзор",hmi:"HMI",devices:"Устройства",alarms:"Тревоги",historian:"Архив",audit:"Аудит",settings:"Настройки",aboutUs:"О нас",systemInfo:"О системе"}
};
let latest={},alarms=[],definitions=[],devices=[];
const $=id=>document.getElementById(id);
const escapeHtml=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const operatorHeaders=()=>({"Content-Type":"application/json","X-Operator":$("operator").value||"local-operator","X-Role":$("role").value||"viewer"});
const fmt=v=>typeof v==="number"?(Math.abs(v)>=100?v.toFixed(0):v.toFixed(1)):String(v).toUpperCase();
const icon=(name,cls="")=>'<svg class="'+cls+'" aria-hidden="true"><use href="#i-'+name+'"></use></svg>';
const metricIcon=id=>({tank_level:"database",line_pressure:"protocol",process_temp:"historian",flow_rate:"network"}[id]||"hmi");

function setLocale(locale){
  localStorage.setItem("nexvary-scada-locale",locale);
  const rtl=["ar","ur","fa"].includes(locale);
  document.documentElement.lang=locale;document.documentElement.dir=rtl?"rtl":"ltr";
  const dict={...I18N.en,...(I18N[locale]||{})};
  document.querySelectorAll("[data-i18n]").forEach(el=>{const key=el.dataset.i18n;if(dict[key])el.textContent=dict[key]});
}
function navigate(page){
  const target=$("page-"+page);
  if(!target)page="overview";
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
  $("cards").innerHTML=ids.map(id=>{const t=latest[id];return '<article class="card"><span class="quality '+t.quality+'">'+escapeHtml(t.quality)+'</span><div class="label metric-title">'+icon(metricIcon(id))+escapeHtml(t.definition.name)+'</div><div class="value">'+escapeHtml(fmt(t.value))+'</div><div class="unit">'+escapeHtml(t.definition.unit)+'</div></article>'}).join("")||'<div class="empty">No numeric tags</div>';
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
  $("device-grid").innerHTML=devices.map(d=>'<article class="device-card"><div class="device-head"><span class="device-glyph">'+icon("devices")+'</span><span class="badge '+(d.health.connected?"ok":"bad")+'">'+(d.health.connected?"ONLINE":"OFFLINE")+'</span></div><h3>'+escapeHtml(d.name)+'</h3><p>'+escapeHtml(d.description)+'</p><div class="device-meta"><div><span>DRIVER</span><b>'+escapeHtml(d.driver)+'</b></div><div><span>TAGS</span><b>'+d.tag_count+'</b></div><div><span>WRITES</span><b>'+ (d.writes_enabled?"DEVICE ENABLED":"BLOCKED")+'</b></div><div><span>HEALTH</span><b>'+escapeHtml(d.health.detail)+'</b></div></div></article>').join("");
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
  ctx.strokeStyle="#223245";ctx.lineWidth=1;for(let i=1;i<5;i++){const y=i*h/5;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke()}
  if(rows.length<2)return;
  const vals=rows.map(r=>Number(r.value)),min=Math.min(...vals),max=Math.max(...vals),span=max-min||1;
  const gradient=ctx.createLinearGradient(0,0,w,0);gradient.addColorStop(0,"#7d49ff");gradient.addColorStop(.35,"#24a8ff");gradient.addColorStop(.68,"#d6ad4d");gradient.addColorStop(1,"#31e78a");
  ctx.strokeStyle=gradient;ctx.lineWidth=3;ctx.beginPath();rows.forEach((r,i)=>{const x=i*(w/(rows.length-1)),y=h-24-((Number(r.value)-min)/span)*(h-48);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke();
  ctx.fillStyle="#a9b5c2";ctx.font="18px Segoe UI";ctx.fillText("max "+max.toFixed(2),14,24);ctx.fillText("min "+min.toFixed(2),14,h-8);
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
navigate((location.hash||"#executive").slice(1));refresh();setInterval(refresh,2500);

const executiveLabels={
  connected_sites:["CONNECTED SITES","sites"],
  monitored_assets:["MONITORED ASSETS","assets"],
  asset_health_percent:["ASSET HEALTH","%"],
  generation_mw:["DEMO GENERATION","MW"],
  critical_open_alarms:["CRITICAL ALARMS","open"],
  audit_coverage_percent:["AUDIT COVERAGE","%"]
};
const nuclearLabels={
  gross_generation_mw:["GROSS GENERATION","MW"],
  grid_frequency_hz:["GRID FREQUENCY","Hz"],
  auxiliary_load_mw:["AUXILIARY LOAD","MW"],
  cooling_water_inlet_c:["COOLING WATER INLET","°C"],
  systems_available:["SYSTEMS AVAILABLE",""],
  open_critical_alarms:["CRITICAL ALARMS","open"]
};

function renderKpis(targetId,values,labels){
  const target=$(targetId);if(!target)return;
  target.innerHTML=Object.entries(labels).map(([key,label])=>{
    const value=values[key]??"—";
    return '<article class="exec-kpi"><small>'+escapeHtml(label[0])+'</small><strong>'+escapeHtml(value)+'</strong><span>'+escapeHtml(label[1])+'</span></article>';
  }).join("");
}
function drawNuclearTrend(values){
  const canvas=$("nuclear-trend");if(!canvas||!values?.length)return;
  const ctx=canvas.getContext("2d"),w=canvas.width,h=canvas.height;
  ctx.clearRect(0,0,w,h);ctx.strokeStyle="#223245";ctx.lineWidth=1;
  for(let i=1;i<5;i++){const y=i*h/5;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke()}
  const min=Math.min(...values),max=Math.max(...values),span=max-min||1;
  const gradient=ctx.createLinearGradient(0,0,w,0);gradient.addColorStop(0,"#7d49ff");gradient.addColorStop(.5,"#24a8ff");gradient.addColorStop(1,"#d6ad4d");
  ctx.strokeStyle=gradient;ctx.lineWidth=3;ctx.beginPath();
  values.forEach((value,i)=>{const x=20+i*((w-40)/(values.length-1)),y=h-28-((value-min)/span)*(h-55);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});
  ctx.stroke();ctx.fillStyle="#a9b5c2";ctx.font="16px Segoe UI";ctx.fillText("max "+max.toFixed(1)+" MW",16,20);ctx.fillText("min "+min.toFixed(1)+" MW",16,h-8);
}
async function refreshPresentation(){
  try{
    const [executive,nuclear]=await Promise.all([api("/api/executive"),api("/api/nuclear")]);
    renderKpis("executive-kpis",executive.headline,executiveLabels);
    const sectors=$("executive-sectors");
    if(sectors)sectors.innerHTML=executive.sectors.map(s=>'<article class="sector-card '+escapeHtml(s.accent)+'"><b>'+escapeHtml(s.name)+'</b><small>'+escapeHtml(s.sites)+' connected demo site'+(s.sites===1?"":"s")+'</small><span>'+escapeHtml(s.status)+'</span></article>').join("");
    const capabilities=$("executive-capabilities");
    if(capabilities)capabilities.innerHTML=executive.capabilities.map(x=>'<div class="capability-item"><i></i><span>'+escapeHtml(x)+'</span></div>').join("");
    renderKpis("nuclear-headline",nuclear.headline,nuclearLabels);
    if($("nuclear-plant-name"))$("nuclear-plant-name").textContent=nuclear.plant;
    if($("nuclear-scope-notice"))$("nuclear-scope-notice").textContent=nuclear.scope_notice;
    const units=$("nuclear-units");
    if(units)units.innerHTML=nuclear.units.map(u=>'<article class="unit-card"><div class="unit-card-head"><b>UNIT '+u.unit+'</b><span>'+escapeHtml(u.status)+'</span></div><div class="unit-power">'+escapeHtml(u.generator_load_mw)+' <small>MW</small></div><div class="unit-meta"><div><small>TURBINE SPEED</small><b>'+escapeHtml(u.turbine_speed_rpm)+' RPM</b></div><div><small>AVAILABILITY</small><b>'+escapeHtml(u.availability_percent)+'%</b></div></div></article>').join("");
    const systems=$("nuclear-systems");
    if(systems)systems.innerHTML=nuclear.systems.map(s=>'<div class="nuclear-system"><i></i><div><b>'+escapeHtml(s.name)+'</b><small>'+escapeHtml(s.detail)+'</small></div><span>'+escapeHtml(s.status)+'</span></div>').join("");
    drawNuclearTrend(nuclear.trend);
  }catch(error){console.error("Presentation data:",error)}
}
refreshPresentation();setInterval(refreshPresentation,4000);
