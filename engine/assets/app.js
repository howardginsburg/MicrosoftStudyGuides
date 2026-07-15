/* ===== DP-600 Study Guide — interactive app ===== */
(function(){
  "use strict";
  var content = document.getElementById("content");
  var toc = document.getElementById("toc");
  var STORE = "dp600-progress-v1";

  /* ---------- Build Table of Contents ---------- */
  function slug(el, fb){ return el.id || fb; }
  var tocHtml = ['<div class="toc-h">Contents</div>','<ul>'];
  var objectives = [];
  content.querySelectorAll("h1, h2, section.objective > h3").forEach(function(h){
    if(h.tagName === "H1"){
      tocHtml.push('<li><a class="t1" href="#'+h.id+'">'+h.textContent.replace(/\s+/g," ").trim()+'</a></li>');
    } else if(h.tagName === "H2"){
      tocHtml.push('<li><a class="t2" href="#'+h.id+'">'+h.textContent.trim()+'</a></li>');
    } else { /* objective h3 */
      var sec = h.parentElement;
      var id = sec.id || h.id;
      objectives.push(id);
      tocHtml.push('<li class="obj" data-obj="'+id+'">'+
        '<input type="checkbox" title="Mark complete" data-check="'+id+'">'+
        '<a href="#'+id+'">'+h.textContent.trim()+'</a></li>');
    }
  });
  tocHtml.push('</ul>');
  toc.innerHTML = tocHtml.join("");

  /* ---------- Progress (localStorage) ---------- */
  var done = {};
  try{ done = JSON.parse(localStorage.getItem(STORE)) || {}; }catch(e){ done = {}; }
  var indicator = document.getElementById("progress-indicator");
  function refreshProgress(){
    var c = 0;
    objectives.forEach(function(id){ if(done[id]) c++; });
    if(indicator) indicator.textContent = "Progress: " + c + " / " + objectives.length;
  }
  toc.querySelectorAll("input[data-check]").forEach(function(cb){
    var id = cb.getAttribute("data-check");
    cb.checked = !!done[id];
    cb.closest(".obj").classList.toggle("done", !!done[id]);
    cb.addEventListener("change", function(){
      done[id] = cb.checked;
      cb.closest(".obj").classList.toggle("done", cb.checked);
      try{ localStorage.setItem(STORE, JSON.stringify(done)); }catch(e){}
      refreshProgress();
    });
  });
  refreshProgress();

  /* ---------- Collapsible objectives ---------- */
  content.querySelectorAll("section.objective > h3").forEach(function(h){
    h.addEventListener("click", function(){ h.parentElement.classList.toggle("collapsed"); });
  });
  var collapsed = false;
  var caBtn = document.getElementById("collapse-btn");
  if(caBtn) caBtn.addEventListener("click", function(){
    collapsed = !collapsed;
    content.querySelectorAll("section.objective").forEach(function(s){ s.classList.toggle("collapsed", collapsed); });
    caBtn.textContent = collapsed ? "Expand all" : "Collapse all";
  });

  /* ---------- Copy buttons ---------- */
  content.querySelectorAll("div.code").forEach(function(box){
    var code = box.querySelector("code"); if(!code) return;
    var btn = document.createElement("button");
    btn.className = "copy-btn"; btn.textContent = "Copy";
    btn.addEventListener("click", function(){
      var txt = code.innerText;
      navigator.clipboard.writeText(txt).then(function(){
        btn.textContent = "Copied"; btn.classList.add("copied");
        setTimeout(function(){ btn.textContent = "Copy"; btn.classList.remove("copied"); }, 1400);
      });
    });
    box.appendChild(btn);
  });

  /* ---------- Search / filter ---------- */
  var search = document.getElementById("search");
  var noresults = document.getElementById("noresults");
  function clearMarks(root){
    root.querySelectorAll("mark").forEach(function(m){
      var p = m.parentNode; p.replaceChild(document.createTextNode(m.textContent), m); p.normalize();
    });
  }
  var searchT;
  if(search) search.addEventListener("input", function(){
    clearTimeout(searchT); searchT = setTimeout(runSearch, 140);
  });
  function runSearch(){
    var q = search.value.trim().toLowerCase();
    clearMarks(content);
    var objs = content.querySelectorAll("section.objective");
    var anyVisible = false;
    if(!q){
      content.querySelectorAll(".hidden").forEach(function(e){ e.classList.remove("hidden"); });
      objs.forEach(function(o){ o.classList.remove("collapsed"); });
      noresults.style.display = "none"; return;
    }
    objs.forEach(function(o){
      var hit = o.textContent.toLowerCase().indexOf(q) !== -1;
      o.classList.toggle("hidden", !hit);
      o.classList.remove("collapsed");
      if(hit) anyVisible = true;
    });
    /* hide empty skillgroups / domains */
    content.querySelectorAll("section.skillgroup").forEach(function(g){
      var vis = g.querySelector("section.objective:not(.hidden)");
      var hasNonObj = g.querySelectorAll("table.cmp, .code").length && g.textContent.toLowerCase().indexOf(q)!==-1 && !g.querySelector("section.objective");
      g.classList.toggle("hidden", !vis && !hasNonObj);
      if(vis||hasNonObj) anyVisible = true;
    });
    content.querySelectorAll("section.domain").forEach(function(d){
      var vis = d.querySelector("section.objective:not(.hidden), section.skillgroup:not(.hidden)");
      d.classList.toggle("hidden", !vis);
    });
    noresults.style.display = anyVisible ? "none" : "block";
  }

  /* ---------- Scroll-spy ---------- */
  var links = {};
  toc.querySelectorAll("a").forEach(function(a){ links[a.getAttribute("href").slice(1)] = a; });
  var spyTargets = [].slice.call(content.querySelectorAll("h1, h2, section.objective"));
  var spyT;
  function spy(){
    var pos = window.scrollY + 120, cur = null;
    for(var i=0;i<spyTargets.length;i++){ if(spyTargets[i].offsetTop <= pos) cur = spyTargets[i]; }
    toc.querySelectorAll("a.active").forEach(function(a){ a.classList.remove("active"); });
    if(cur){
      var id = cur.id || (cur.querySelector("[id]") && cur.querySelector("[id]").id);
      if(links[id]){ links[id].classList.add("active");
        if(links[id].getBoundingClientRect){} }
    }
  }
  window.addEventListener("scroll", function(){ clearTimeout(spyT); spyT = setTimeout(spy, 80); });
  spy();

  /* ---------- Theme toggle ---------- */
  var tb = document.getElementById("theme-btn");
  var TKEY = "dp600-theme";
  try{ if(localStorage.getItem(TKEY)==="dark") document.documentElement.setAttribute("data-theme","dark"); }catch(e){}
  if(tb) tb.addEventListener("click", function(){
    var dark = document.documentElement.getAttribute("data-theme")==="dark";
    document.documentElement.setAttribute("data-theme", dark?"light":"dark");
    try{ localStorage.setItem(TKEY, dark?"light":"dark"); }catch(e){}
  });

  /* ---------- Mobile menu + print ---------- */
  var mb = document.getElementById("menu-btn");
  if(mb) mb.addEventListener("click", function(){ toc.classList.toggle("open"); });
  toc.addEventListener("click", function(e){ if(e.target.tagName==="A") toc.classList.remove("open"); });
  var pb = document.getElementById("print-btn");
  if(pb) pb.addEventListener("click", function(){ window.print(); });
})();
