(function () {
  var sidebar = document.getElementById("sidebar");
  if (!sidebar) return;
  var btn = document.querySelector(".menu-btn");
  var scrim = document.querySelector(".scrim");
  var links = Array.prototype.slice.call(sidebar.querySelectorAll(".toc a"));

  /* ----- mobile drawer ----- */
  function setOpen(open) {
    sidebar.classList.toggle("open", open);
    if (scrim) scrim.hidden = !open;
    if (btn) btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  if (btn) btn.addEventListener("click", function () { setOpen(!sidebar.classList.contains("open")); });
  if (scrim) scrim.addEventListener("click", function () { setOpen(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
  links.forEach(function (a) {
    a.addEventListener("click", function () {
      if (window.matchMedia("(max-width: 900px)").matches) setOpen(false);
    });
  });

  /* ----- filter ----- */
  var input = sidebar.querySelector(".toc-filter");
  if (input) {
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      sidebar.querySelectorAll(".toc > li").forEach(function (li) {
        var details = li.querySelector("details");
        var top = li.querySelector("a");
        var topHit = !q || top.textContent.toLowerCase().indexOf(q) > -1;
        var anyKid = false;
        li.querySelectorAll(".toc-h3").forEach(function (k) {
          var hit = !q || topHit || k.textContent.toLowerCase().indexOf(q) > -1;
          k.classList.toggle("hidden", !hit);
          if (hit && q) anyKid = true;
        });
        li.classList.toggle("hidden", !(topHit || anyKid));
        if (details && q) details.open = anyKid || topHit;
      });
    });
  }

  /* ----- highlight current section ----- */
  var map = {};
  links.forEach(function (a) { map[decodeURIComponent(a.getAttribute("href").slice(1))] = a; });
  var heads = Array.prototype.slice.call(document.querySelectorAll(".content h2[id], .content h3[id]"))
    .filter(function (h) { return map[h.id]; });
  var current = null;
  function mark(id) {
    var a = map[id];
    if (!a || a === current) return;
    if (current) current.classList.remove("current");
    a.classList.add("current");
    current = a;
    var d = a.closest("details");
    if (d && !d.open && !(input && input.value)) d.open = true;
    var wrap = sidebar.querySelector(".toc-wrap");
    var r = a.getBoundingClientRect(), w = wrap.getBoundingClientRect();
    if (r.top < w.top + 20 || r.bottom > w.bottom - 20) {
      wrap.scrollTop += r.top - w.top - w.height / 3;
    }
  }
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var y = 150, best = heads[0];
      for (var i = 0; i < heads.length; i++) {
        if (heads[i].getBoundingClientRect().top - y <= 0) best = heads[i]; else break;
      }
      if (best) mark(best.id);
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();
