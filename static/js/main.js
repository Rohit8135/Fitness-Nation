// =======================================
//  FITNESS NATION – Main JavaScript
// =======================================

document.addEventListener('DOMContentLoaded', () => {

  // ---- NAVBAR SCROLL ----
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  });

  // ---- HAMBURGER MENU ----
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks');
  hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navLinks.classList.toggle('open');
  });

  // Close menu on link click
  navLinks?.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
    });
  });

  // ---- ACTIVE NAV LINK ON SCROLL ----
  const sections = document.querySelectorAll('section[id]');
  const allLinks = document.querySelectorAll('.nav-link');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        allLinks.forEach(l => l.classList.remove('active'));
        const active = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
        if (active) active.classList.add('active');
      }
    });
  }, { threshold: 0.4 });
  sections.forEach(s => observer.observe(s));

  // ---- SCROLL REVEAL ----
  const reveals = document.querySelectorAll(
    '.plan-card, .facility-card, .testimonial-card, .gallery-item, .stat-card'
  );
  reveals.forEach(el => el.classList.add('reveal'));
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  reveals.forEach(el => revealObserver.observe(el));

  // ---- PLAN CARD → PRE-SELECT FORM ----
  document.querySelectorAll('[data-plan]').forEach(card => {
    card.addEventListener('click', () => {
      const plan = card.dataset.plan;
      const select = document.getElementById('fplan');
      if (!select) return;
      for (let opt of select.options) {
        if (opt.value.startsWith(plan)) {
          select.value = opt.value;
          break;
        }
      }
      document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // ---- ENQUIRY FORM SUBMIT ----
  const form    = document.getElementById('enquiryForm');
  const formMsg = document.getElementById('formMsg');
  const submitBtn = document.getElementById('submitBtn');

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Sending...</span>';

    const data = new FormData(form);

    try {
      const res  = await fetch('/submit_enquiry', { method: 'POST', body: data });
      const json = await res.json();

      formMsg.className = 'form-msg ' + (json.success ? 'success' : 'error');
      formMsg.textContent = json.message;

      if (json.success) {
        form.reset();
        setTimeout(() => { formMsg.className = 'form-msg'; }, 5000);
      }
    } catch {
      formMsg.className = 'form-msg error';
      formMsg.textContent = 'Something went wrong. Please try again.';
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<span>Send Enquiry</span><span class="btn-arrow">→</span>';
    }
  });

  // ---- SMOOTH COUNTER ANIMATION ----
  function animateCounter(el, target, duration = 1500) {
    const start = performance.now();
    const update = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(ease * target) + (el.dataset.suffix || '');
      if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  }
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el  = entry.target;
        const val = parseInt(el.dataset.count);
        if (!isNaN(val)) animateCounter(el, val);
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach(el => counterObserver.observe(el));

});
