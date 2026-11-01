/* ═══════════════════════════════════════════════════════════
   王鑫鸿个人作品矩阵 · 交互层
   主题切换 / 移动端菜单 / 滚动监听 / 入场动效 / 数字滚动
   无依赖，约 4KB。
   ═══════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 主题 ---------- */
  var themeBtn = document.getElementById("theme-toggle");

  function setTheme(theme, persist) {
    root.setAttribute("data-theme", theme);
    if (persist) {
      try {
        localStorage.setItem("wxh-theme", theme);
      } catch (e) {}
    }
    var color = theme === "dark" ? "#07090E" : "#F5F7FB";
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", color);
    if (themeBtn) {
      themeBtn.setAttribute(
        "aria-label",
        theme === "dark" ? "切换到浅色主题" : "切换到深色主题"
      );
    }
  }

  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      setTheme(next, true);
    });
  }

  // 未手动选过时，跟随系统
  var mql = window.matchMedia("(prefers-color-scheme: light)");
  mql.addEventListener &&
    mql.addEventListener("change", function (e) {
      var saved = null;
      try {
        saved = localStorage.getItem("wxh-theme");
      } catch (err) {}
      if (!saved) setTheme(e.matches ? "light" : "dark", false);
    });

  /* ---------- 移动端菜单 ---------- */
  var menu = document.getElementById("menu");
  var menuBtn = document.getElementById("menu-toggle");

  function closeMenu() {
    if (!menu || !menuBtn) return;
    menu.classList.remove("is-open");
    menuBtn.setAttribute("aria-expanded", "false");
    menuBtn.setAttribute("aria-label", "打开菜单");
  }

  if (menu && menuBtn) {
    menuBtn.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.setAttribute("aria-label", open ? "关闭菜单" : "打开菜单");
    });

    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeMenu();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 1020) closeMenu();
    });
  }

  /* ---------- 导航吸顶描边 ---------- */
  var nav = document.getElementById("nav");
  var lastY = -1;

  function onScroll() {
    var y = window.scrollY;
    if (nav && y !== lastY) {
      nav.classList.toggle("is-stuck", y > 8);
      lastY = y;
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- 滚动监听高亮 ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav__link"));
  var sections = links
    .map(function (a) {
      var id = a.getAttribute("href").slice(1);
      return document.getElementById(id);
    })
    .filter(Boolean);

  if ("IntersectionObserver" in window && sections.length) {
    var spy = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (a) {
            a.classList.toggle(
              "is-active",
              a.getAttribute("href") === "#" + entry.target.id
            );
          });
        });
      },
      { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
    );
    sections.forEach(function (s) {
      spy.observe(s);
    });

    // 首屏内不点亮任何导航项
    window.addEventListener(
      "scroll",
      function () {
        if (window.scrollY < 160) {
          links.forEach(function (a) {
            a.classList.remove("is-active");
          });
        }
      },
      { passive: true }
    );
  }

  /* ---------- 数字滚动 ---------- */
  function format(n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (isNaN(target)) return;
    if (reduceMotion || target < 30) {
      el.textContent = format(target);
      return;
    }
    var start = performance.now();
    var dur = 1100;

    function tick(now) {
      var p = Math.min((now - start) / dur, 1);
      // easeOutCubic
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ---------- 入场动效 ---------- */
  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));

  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          var siblings = Array.prototype.slice.call(
            el.parentElement ? el.parentElement.children : []
          );
          var idx = Math.max(0, siblings.indexOf(el));
          el.style.transitionDelay = Math.min(idx, 3) * 70 + "ms";
          el.classList.add("is-in");
          obs.unobserve(el);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    reveals.forEach(function (el) {
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) {
      el.classList.add("is-in");
    });
  }

  var counters = Array.prototype.slice.call(document.querySelectorAll("[data-count]"));
  if ("IntersectionObserver" in window && !reduceMotion) {
    var cio = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          countUp(entry.target);
          obs.unobserve(entry.target);
        });
      },
      { threshold: 0.6 }
    );
    counters.forEach(function (el) {
      cio.observe(el);
    });
  } else {
    counters.forEach(countUp);
  }
})();
