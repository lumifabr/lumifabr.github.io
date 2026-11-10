/* LumiFa · Novos modelos (v2) — comportamento extra por cima do motor atual.
   1) cabeçalho recolhe ao descer (menu some, logo fica, busca vira lupa)
   2) produto com link próprio (#produto=PROD-xxx): o "voltar" do celular fecha o produto
   3) produtos da mesma categoria dentro da tela do produto
   4) entrada suave das seções, vídeo da capa, barra para trocar de modelo */
(function () {
  const root = document.documentElement;
  // sempre abrir no topo (o celular tentava "lembrar" a posição e caía no meio da lista)
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  const topo = () => { if (!/^#produto=/i.test(location.hash)) window.scrollTo(0, 0); };
  topo(); addEventListener('load', topo); addEventListener('pageshow', e => { if (!e.persisted) topo(); });
  const MODELO = root.dataset.modelo;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  // ---------- 1. Cabeçalho ----------
  const header = $('header.main');
  const search = $('header.main .search');
  const input = search && $('input', search);
  const medirCabecalho = () => { if (!root.classList.contains('is-scrolled')) root.style.setProperty('--hh', header.offsetHeight + 'px'); };
  let ticking = false;
  const limite = () => (MODELO === 'a' ? 40 : 90);
  const onScroll = () => {
    ticking = false;
    // seções que já passaram (pulos rápidos, "voltar ao topo") também aparecem
    document.querySelectorAll('[data-reveal]:not(.in)').forEach(el => { if (el.getBoundingClientRect().top < innerHeight) el.classList.add('in'); });
    const desceu = window.scrollY > limite();
    if (desceu !== root.classList.contains('is-scrolled')) {
      root.classList.toggle('is-scrolled', desceu);
      if (!desceu) search.classList.remove('is-open');
      if (desceu && document.activeElement === input && !input.value) input.blur();
      if (typeof toggleMega === 'function') toggleMega(false);
    }
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', medirCabecalho);
  medirCabecalho(); onScroll();

  if (search) {
    search.addEventListener('mousedown', e => {
      if (root.classList.contains('is-scrolled') && !search.classList.contains('is-open')) {
        e.preventDefault(); search.classList.add('is-open'); setTimeout(() => input.focus(), 60);
      }
    });
    input.addEventListener('focus', () => { if (root.classList.contains('is-scrolled')) search.classList.add('is-open'); });
    input.addEventListener('blur', () => setTimeout(() => { if (document.activeElement !== input) search.classList.remove('is-open'); }, 120));
    input.addEventListener('input', () => search.classList.toggle('has-q', !!input.value));
    input.addEventListener('keydown', e => {
      if (e.key === 'Escape') input.blur();
      if (e.key === 'Enter') { input.blur(); const a = document.getElementById('produtos'); if (a) scrollTo({ top: a.getBoundingClientRect().top + scrollY - 80, behavior: 'smooth' }); }
    });
  }

  // ---------- 2. Link próprio do produto + 3. relacionados ----------
  const HASH = /^#produto=([\w-]+)/i;
  let layer = null, abertoPorHash = false;
  const codigoAberto = () => { const m = $('#m-product .m-code'); return m ? m.textContent.replace(/^CÓD\.\s*/i, '').trim() : ''; };
  function relacionados() {
    const body = $('#m-product .m-body'); if (!body || !window.Motor) return;
    const S = Motor.state, H = Motor.H, code = codigoAberto();
    const p = S.byCode && S.byCode.get(code); if (!p) return;
    const grupo = p.group;
    const lista = (S.items || []).filter(it => it.category === p.category && it.code !== code && (!grupo || it.group !== grupo) && it.image);
    for (let i = lista.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [lista[i], lista[j]] = [lista[j], lista[i]]; }
    const sel = lista.slice(0, 4); if (!sel.length) return;
    const old = $('.v2-rel', body); if (old) old.remove();
    const grid = $('.m-grid', body);
    grid.insertAdjacentHTML('beforeend', `<div class="v2-rel"><h4>Mais em ${H.esc(p.category)}</h4><div class="v2-rel-row">${sel.map(it =>
      `<button type="button" data-open="${H.esc(it.code)}"><span class="ri">${H.img(it)}</span><b>${H.esc(it.name)}</b><small>${H.priceLabel(it.price)}</small></button>`).join('')}</div></div>`);
    // copiar link do produto
    const wa = $('.m-wa', body);
    if (wa && !$('.v2-share', body)) wa.insertAdjacentHTML('afterend', `<button type="button" class="v2-share"><i class="fa-solid fa-link"></i> Copiar link deste produto</button>`);
  }
  function aoAbrir() {
    const code = codigoAberto(); if (!code) return;
    const alvo = '#produto=' + code;
    if (location.hash !== alvo) {
      if (HASH.test(location.hash)) history.replaceState({ v2p: 1 }, '', alvo);
      else history.pushState({ v2p: 1 }, '', alvo);
    }
    relacionados();
    const panel = $('#m-product .m-panel'); if (panel) panel.scrollTop = 0;
  }
  function aoFechar() {
    if (HASH.test(location.hash)) {
      if (history.state && history.state.v2p && !abertoPorHash) history.back();
      else history.replaceState(null, '', location.pathname + location.search);
    }
    abertoPorHash = false;
  }
  function ligarProduto() {
    layer = document.getElementById('m-product');
    if (!layer) return setTimeout(ligarProduto, 200);
    // botão "Voltar" (celular) no produto e no orçamento
    const panel = $('.m-panel', layer);
    if (panel) panel.insertAdjacentHTML('afterbegin', `<button type="button" class="v2-voltar v2-pvoltar" onclick="Motor.close('#m-product')"><i class="fa-solid fa-arrow-left"></i> Voltar ao catálogo</button>`);
    const cart = document.getElementById('m-cart');
    if (cart) {
      const ch = $('.c-head', cart);
      if (ch) ch.insertAdjacentHTML('afterbegin', `<button type="button" class="v2-voltar" onclick="Motor.close('#m-cart')"><i class="fa-solid fa-arrow-left"></i> Voltar</button>`);
      // o "voltar" do próprio celular também fecha o orçamento
      let cAberto = false;
      new MutationObserver(() => {
        const agora = cart.classList.contains('is-open');
        if (agora && !cAberto) history.pushState({ v2c: 1 }, '', location.pathname + location.search + '#orcamento');
        if (!agora && cAberto && location.hash === '#orcamento') history.back();
        cAberto = agora;
      }).observe(cart, { attributes: true, attributeFilter: ['class'] });
    }
    let aberto = false, ultimo = '';
    new MutationObserver(() => {
      const agora = layer.classList.contains('is-open');
      const code = codigoAberto();
      if (agora && (!aberto || code !== ultimo)) aoAbrir();
      else if (agora && code && !layer.querySelector('.v2-rel')) relacionados(); // o motor redesenhou a tela
      if (!agora && aberto) aoFechar();
      aberto = agora; ultimo = code;
    }).observe(layer, { attributes: true, attributeFilter: ['class'], subtree: true, childList: true });
    layer.addEventListener('click', e => {
      const b = e.target.closest('.v2-share'); if (!b) return;
      const url = location.href;
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(() => { b.innerHTML = '<i class="fa-solid fa-check"></i> Link copiado — é só colar no WhatsApp'; }).catch(() => prompt('Copie o link:', url));
    });
  }
  addEventListener('popstate', () => {
    const cart = document.getElementById('m-cart');
    if (cart && cart.classList.contains('is-open') && location.hash !== '#orcamento') { Motor.close('#m-cart'); return; }
    if (layer && layer.classList.contains('is-open') && !HASH.test(location.hash)) Motor.close('#m-product');
    else abrirDoHash();
  });
  function abrirDoHash() {
    const m = location.hash.match(HASH);
    if (m && window.Motor && Motor.state.byCode && Motor.state.byCode.get(m[1].toUpperCase())) { abertoPorHash = true; Motor.open(m[1].toUpperCase()); }
  }
  ligarProduto();
  // espera o catálogo carregar para abrir o produto do link
  const fotosOk = () => window.Motor && Motor.state.fotos && Object.keys(Motor.state.fotos).length > 0;
  (function esperar(n) { if (window.Motor && Motor.state.items && Motor.state.items.length && (fotosOk() || n > 40)) abrirDoHash(); else if (n < 100) setTimeout(() => esperar(n + 1), 150); })(0);
  // se um produto foi aberto antes da lista de fotos chegar, reabre com a ficha técnica
  (function fichas(n) {
    if (fotosOk()) {
      const code = codigoAberto();
      if (layer && layer.classList.contains('is-open') && code && Motor.state.gal && Motor.state.gal.length === 1 && Motor.state.fotos[code]) Motor.open(code);
      return;
    }
    if (n < 80) setTimeout(() => fichas(n + 1), 250);
  })(0);

  // ---------- 4. Revelar seções ----------
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' }) : null;
  $$('[data-reveal]').forEach(el => io ? io.observe(el) : el.classList.add('in'));

  // vídeo da capa (modelo A): escolhe o formato pela tela e respeita "reduzir movimento"
  const v = $('.hero video');
  if (v) {
    const tall = matchMedia('(max-width: 900px)').matches;
    v.src = v.dataset[tall ? 'tall' : 'wide'];
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) v.removeAttribute('autoplay'); else v.play().catch(() => {});
    const bt = $('.v2-vctl');
    if (bt) bt.onclick = () => { if (v.paused) { v.play(); bt.innerHTML = '<i class="fa-solid fa-pause"></i>'; } else { v.pause(); bt.innerHTML = '<i class="fa-solid fa-play"></i>'; } };
  }
  // reels (modelo B): tocam só quando aparecem na tela
  const reels = $$('.v2-reel video');
  if (reels.length && 'IntersectionObserver' in window) {
    const ro = new IntersectionObserver(es => es.forEach(e => {
      const vd = e.target;
      if (e.isIntersecting) { if (!vd.src) vd.src = vd.dataset.src; vd.play().catch(() => {}); } else vd.pause();
    }), { threshold: .35 });
    reels.forEach(r => ro.observe(r));
  }
  // modelo C: "prato" de luz atrás do produto da capa
  if (MODELO === 'c') {
    const art = $('[data-hero-art]');
    const pl = () => { const f = art && art.querySelector('figure'); if (f && !f.querySelector('.v2-plate')) f.insertAdjacentHTML('afterbegin', '<span class="v2-plate"></span>'); };
    if (art) new MutationObserver(pl).observe(art, { childList: true, subtree: true });
  }

  // ---------- Barra para trocar de modelo (só nas prévias) ----------
  if (!new URLSearchParams(location.search).has('limpo')) {
    const q = location.search;
    const M = [['a', 'A · Cinema'], ['b', 'B · Galeria'], ['c', 'C · Vitrine']];
    const files = { a: 'a-cinema.html', b: 'b-galeria.html', c: 'c-vitrine.html' };
    document.body.insertAdjacentHTML('beforeend', `<nav id="v2-bar" aria-label="Trocar de modelo"><a href="./" title="Ver a apresentação"><i class="fa-solid fa-table-cells-large"></i> <span class="lbl">Modelos</span></a>${M.map(([k, n]) => `<a href="${files[k]}${q}" class="${k === MODELO ? 'on' : ''}">${n}</a>`).join('')}<button class="x" onclick="this.parentElement.remove()" aria-label="Esconder"><i class="fa-solid fa-xmark"></i></button></nav>`);
  }
})();
