/* Marketing Studio landing — vanilla JS, no dependencies. */
(function () {
  "use strict";
  var REPO = "https://github.com/Basharlouzon/marketing-studio.git";
  var CMDS = {
    zcode: "git clone --depth 1 " + REPO + " && bash marketing-studio/install.sh",
    claude: "git clone --depth 1 " + REPO + " && SKILLS_DIR=~/.claude/skills bash marketing-studio/install.sh"
  };
  var agent = "zcode";

  /* agent tabs: one choice updates every install command on the page */
  var tabs = document.querySelectorAll(".tab[data-agent]");
  function setAgent(a) {
    agent = a;
    tabs.forEach(function (t) { t.setAttribute("aria-selected", t.dataset.agent === a ? "true" : "false"); });
    document.querySelectorAll("[data-cmd-text]").forEach(function (el) { el.textContent = CMDS[a]; });
  }
  tabs.forEach(function (t) { t.addEventListener("click", function () { setAgent(t.dataset.agent); }); });

  /* copy buttons */
  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text; ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;top:-9999px;opacity:0";
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
  function flash(btn, ok) {
    btn.dataset.orig = btn.dataset.orig || btn.textContent;
    btn.classList.remove("ok", "err");
    btn.classList.add(ok ? "ok" : "err");
    btn.textContent = ok ? "Copied ✓" : "Select & copy";
    clearTimeout(btn._t);
    btn._t = setTimeout(function () { btn.textContent = btn.dataset.orig; btn.classList.remove("ok", "err"); }, 1800);
  }
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-copy-cmd],[data-copy]");
    if (!btn) return;
    var text = btn.hasAttribute("data-copy-cmd") ? CMDS[agent] : btn.getAttribute("data-copy");
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { flash(btn, true); }, function () { flash(btn, fallbackCopy(text)); });
    } else {
      flash(btn, fallbackCopy(text));
    }
  });

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* reel: load only when it scrolls near the viewport */
  var vid = document.querySelector("video[data-src]");
  if (vid) {
    var loadVid = function () {
      if (vid.src) return;
      vid.src = vid.dataset.src;
      if (!reduced) { var p = vid.play(); if (p && p.catch) p.catch(function () {}); }
      else { vid.controls = true; }
    };
    if ("IntersectionObserver" in window) {
      var vio = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { loadVid(); vio.disconnect(); }
      }, { rootMargin: "200px" });
      vio.observe(vid);
    } else { loadVid(); }
  }

  /* terminal: a simplified replay of one campaign run */
  var body = document.getElementById("termBody");
  if (!body) return;
  var RUN = [
    [["$ ", "t-p"], ["Make 12 Instagram posts for my product for December.", "t-c"]],
    [["  intake    ", "t-g"], ["3 questions answered · trends scanned", ""]],
    [["  concept   ", "t-g"], ["locked on a real calendar moment", ""]],
    [["  images    ", "t-g"], ["12 posts @ 1080x1350 ... ", ""], ["done", "t-ok"]],
    [["  motion    ", "t-g"], ["reel.mp4 rendered ... ", ""], ["done", "t-ok"]],
    [["  judge     ", "t-g"], ["kv-close-q3.png ", ""], ["7.1 weak hierarchy", "t-bad"]],
    [["  fix       ", "t-g"], ["root cause fixed once · re-render · re-judge", ""]],
    [["  judge     ", "t-g"], ["kv-close-q3.png ", ""], ["9.4 ship", "t-good"]],
    [["$ ", "t-p"], ["only assets at 9.0+ are handed to you", "t-c"]]
  ];
  function line() { var d = document.createElement("div"); body.appendChild(d); return d; }
  function renderStatic() {
    body.textContent = "";
    RUN.forEach(function (segs) {
      var l = line();
      segs.forEach(function (s) { var sp = document.createElement("span"); sp.className = s[1]; sp.textContent = s[0]; l.appendChild(sp); });
    });
  }
  if (reduced || !("IntersectionObserver" in window)) { renderStatic(); return; }

  var caret = document.createElement("span"); caret.className = "caret";
  var started = false;
  function play() {
    body.textContent = "";
    var li = 0;
    (function nextLine() {
      if (li >= RUN.length) { setTimeout(play, 5000); return; }
      var segs = RUN[li++], l = line(), si = 0;
      l.appendChild(caret);
      (function nextSeg() {
        if (si >= segs.length) { setTimeout(nextLine, li === 1 ? 500 : 260); return; }
        var sp = document.createElement("span"); sp.className = segs[si][1];
        l.insertBefore(sp, caret);
        var text = segs[si++][0], ci = 0;
        (function tick() {
          if (ci < text.length) { sp.textContent += text.charAt(ci++); setTimeout(tick, 22); }
          else nextSeg();
        })();
      })();
    })();
  }
  var tio = new IntersectionObserver(function (es) {
    if (es[0].isIntersecting && !started) { started = true; play(); tio.disconnect(); }
  }, { threshold: 0.3 });
  renderStatic(); /* readable before it animates */
  body.style.minHeight = body.offsetHeight + "px"; /* no layout jump while typing */
  tio.observe(body);
})();
