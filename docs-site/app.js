/* Marketing Studio docs site — vanilla JS, zero dependencies. */
document.documentElement.classList.add("js");
var mobileMenu = document.getElementById("mobileMenu");
var menuBtn2 = document.getElementById("menuBtn");
if (menuBtn2) {
  menuBtn2.addEventListener("click", function () {
    var open = document.body.classList.toggle("menu-open");
    menuBtn2.setAttribute("aria-expanded", open ? "true" : "false");
  });
  mobileMenu.addEventListener("click", function (e) {
    if (e.target.tagName === "A") { document.body.classList.remove("menu-open"); menuBtn2.setAttribute("aria-expanded", "false"); }
  });
}
setTimeout(function () {
  document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
}, 1400);
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ----------------------------------------------------------
     Copy buttons — clipboard API with fallback + rejection states
     ---------------------------------------------------------- */
  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;top:-9999px;opacity:0";
    document.body.appendChild(ta);
    ta.select();
    ta.setSelectionRange(0, text.length);
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function flash(btn, state, label) {
    btn.classList.remove("ok", "err");
    btn.classList.add(state);
    btn.dataset.orig = btn.dataset.orig || btn.textContent;
    btn.textContent = label;
    setTimeout(function () {
      btn.textContent = btn.dataset.orig;
      btn.classList.remove("ok", "err");
    }, 1800);
  }

  function copyText(text, btn) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(
        function () { flash(btn, "ok", "copied ✓"); },
        function () {
          if (fallbackCopy(text)) { flash(btn, "ok", "copied ✓"); }
          else { flash(btn, "err", "press ⌘C"); }
        }
      );
    } else if (fallbackCopy(text)) {
      flash(btn, "ok", "copied ✓");
    } else {
      flash(btn, "err", "press ⌘C");
    }
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-copy]");
    if (!btn) return;
    var text = btn.getAttribute("data-copy");
    if (!text) {
      var pre = btn.parentElement.querySelector("pre");
      if (pre) text = pre.innerText;
    }
    if (text) copyText(text, btn);
  });

  /* ----------------------------------------------------------
     IntersectionObserver reveals — 16px rise + fade, 60ms stagger
     ---------------------------------------------------------- */
  document.querySelectorAll("[data-stagger]").forEach(function (group) {
    Array.prototype.forEach.call(group.querySelectorAll(":scope > .reveal"), function (el, i) {
      el.style.setProperty("--d", (i * 60) + "ms");
    });
  });
  var revealEls = document.querySelectorAll(".reveal");
  if (reduced || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ----------------------------------------------------------
     Docs: mobile drawer + TOC scrollspy
     ---------------------------------------------------------- */
  var menuBtn = document.getElementById("menuBtn");
  var scrim = document.getElementById("scrim");
  function closeDrawer() { document.body.classList.remove("drawer-open"); if (menuBtn) menuBtn.setAttribute("aria-expanded", "false"); }
  if (menuBtn) {
    menuBtn.addEventListener("click", function () {
      var open = document.body.classList.toggle("drawer-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  if (scrim) scrim.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeDrawer();
  });
  document.querySelectorAll(".side-list a").forEach(function (a) {
    a.addEventListener("click", closeDrawer);
  });

  var tocLinks = document.querySelectorAll(".toc a[href^='#']");
  var headings = [];
  tocLinks.forEach(function (a) {
    var h = document.getElementById(decodeURIComponent(a.hash.slice(1)));
    if (h) headings.push({ h: h, a: a });
  });
  if (headings.length && "IntersectionObserver" in window && !reduced) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        tocLinks.forEach(function (a) { a.classList.remove("active"); });
        var hit = headings.find(function (x) { return x.h === entry.target; });
        if (hit) hit.a.classList.add("active");
      });
    }, { rootMargin: "-72px 0px -66% 0px", threshold: 0 });
    headings.forEach(function (x) { spy.observe(x.h); });
  }

  /* ----------------------------------------------------------
     Signature moment: auto-typing campaign run
     ~28 chars/sec, loops every ~12s, honors prefers-reduced-motion
     ---------------------------------------------------------- */
  var termBody = document.getElementById("termBody");
  if (!termBody) return;

  var RUN = [
    { seg: [["$ ", "t-p"], ["studio run --campaign q3-close", "t-c"]], pause: 350 },
    { seg: [["  -> ", "t-m"], ["strategy", "t-g"], ["       draft brief ... concept locked: \"Q3 Close\"", "t-m"]] },
    { seg: [["  -> ", "t-m"], ["image-factory", "t-g"], [" render 12 posts @ 1080x1350 ... ", "t-m"], ["done", "t-ok"]], pause: 250 },
    { seg: [["  -> ", "t-m"], ["motion", "t-g"], ["        animate reel.mp4 (00:14) ... ", "t-m"], ["done", "t-ok"]], pause: 250 },
    { seg: [["  -> ", "t-m"], ["visual-judge", "t-g"], [" kv-close-q3.png ... verdict ", "t-m"], ["7.1 - weak hierarchy", "t-bad"]], pause: 550 },
    { seg: [["  fix", "t-r"], ["        regroup root cause x3 -> re-render -> re-judge", "t-m"]], pause: 650 },
    { seg: [["  -> ", "t-m"], ["visual-judge", "t-g"], [" kv-close-q3.png ... verdict ", "t-m"], ["9.4 - SHIP", "t-good"]], pause: 300 },
    { seg: [["$ ", "t-p"], ["12 images - 1 reel - gate >= 9.0 - shipped", "t-c"]] }
  ];

  var CHAR_MS = 1000 / 28; /* ~28 chars/sec */
  var badge = document.getElementById("termBadge");
  var caret = document.createElement("span");
  caret.className = "term-caret";

  function makeLine() {
    var line = document.createElement("div");
    line.className = "term-line";
    termBody.appendChild(line);
    return line;
  }

  function typeSegments(line, seg, done) {
    var si = 0;
    function nextSeg() {
      if (si >= seg.length) { done(); return; }
      var span = document.createElement("span");
      span.className = seg[si][1];
      line.appendChild(span);
      var text = seg[si][0];
      var ci = 0;
      (function tick() {
        if (ci < text.length) {
          span.textContent += text[ci++];
          setTimeout(tick, CHAR_MS);
        } else {
          si++;
          nextSeg();
        }
      })();
    }
    nextSeg();
  }

  function playLoop() {
    termBody.textContent = "";
    badge.classList.remove("pop");
    var start = Date.now();
    var li = 0;

    function nextLine() {
      if (li >= RUN.length) {
        caret.remove();
        badge.classList.add("pop");
        var elapsed = Date.now() - start;
        setTimeout(playLoop, Math.max(2200, 12000 - elapsed)); /* loop every ~12s */
        return;
      }
      var item = RUN[li++];
      var line = makeLine();
      line.appendChild(caret);
      typeSegments(line, item.seg, function () {
        setTimeout(nextLine, item.pause || 120);
      });
    }
    nextLine();
  }

  function renderStatic() {
    termBody.textContent = "";
    RUN.forEach(function (item) {
      var line = makeLine();
      item.seg.forEach(function (s) {
        var span = document.createElement("span");
        span.className = s[1];
        span.textContent = s[0];
        line.appendChild(span);
      });
    });
    badge.classList.add("pop");
  }

  if (reduced) {
    renderStatic();
  } else {
    playLoop();
  }
})();
