// Approved cover composition. Keep artwork separate from physical-size controls.
const titleAsset = name => new URL(`../assets/v4/title/${name}`, import.meta.url).href;
const portrait = key => key === 'felipe' ? titleAsset('felipe-front-portrait.webp') : new URL(`../assets/v4/drivers/${key}-portrait.webp`, import.meta.url).href;

export function titleMarkup(soundButton) {
  return `<section class="title-screen cover-screen" aria-label="FTW Race — Cascavel">
    <div class="cover-viewport"><div class="cover-frame">
      <div class="cover-artboard">
        <div class="cover-landscape" aria-hidden="true" style="background-image:radial-gradient(ellipse at 49% 42%,#7a816e80 0,#17232455 37%,#101613 73%),url('${titleAsset('background.webp')}')"></div>
        <div class="cover-nightfall" aria-hidden="true"></div>
        <div class="cover-aura cover-left" aria-hidden="true"></div><div class="cover-aura cover-right" aria-hidden="true"></div>
        <div class="cover-stripe cover-left" aria-hidden="true"></div><div class="cover-stripe cover-right" aria-hidden="true"></div>
        <div class="cover-edge" aria-hidden="true"></div>
        <div class="cover-team"><div class="cover-dv-crop"><img src="${titleAsset('diabo-verde-official.png')}" alt="Diabo Verde" draggable="false"></div></div>
        <div class="cover-race-marks" aria-hidden="true"><span></span><span></span><span></span></div>
        <header class="cover-title-lockup">
          <div class="cover-ftw-crop"><img src="${titleAsset('ftw-official.png')}" alt="FTW" draggable="false"></div>
          <h1>RACE</h1><p class="cover-location">CASCAVEL</p>
        </header>
        <div class="cover-hero cover-daniel"><img src="${portrait('daniel')}" alt="Daniel Mencacci com boné preto e uniforme preto e verde, voltado ao centro" draggable="false"></div>
        <div class="cover-hero cover-felipe"><img src="${portrait('felipe')}" alt="Felipe Mencacci em pose frontal, com boné vermelho número 25 e uniforme vermelho" draggable="false"></div>
        <div class="cover-hero-ground" aria-hidden="true"></div>
        <div class="cover-car-shadow cover-daniel" aria-hidden="true"></div><div class="cover-car-shadow cover-felipe" aria-hidden="true"></div>
        <div class="cover-road-line" aria-hidden="true"></div>
        <div class="cover-car cover-daniel"><img src="${titleAsset('daniel-front-sheet.webp')}" alt="Carro verde de Daniel, número 22" draggable="false"></div>
        <div class="cover-car cover-felipe"><img src="${titleAsset('felipe-front-sheet.webp')}" alt="Carro vermelho de Felipe, número 25" draggable="false"></div>
      </div>
      <div class="cover-start"><button type="button" class="press-start cover-press-start" id="press-start" data-confirm>PRESS START</button><p class="cover-field">6 CARROS · 1 CAMPEÃO</p></div>
    </div></div>
    <footer class="cover-footer"><p>PRÉVIA V4 · CAPA E PILOTOS APROVADOS</p>${soundButton}<button type="button" class="text-button cover-fullscreen" id="fs">TELA CHEIA</button></footer>
  </section>`;
}

export function mountTitle(root) {
  const viewport = root.querySelector('.cover-viewport');
  const frame = root.querySelector('.cover-frame');
  const start = root.querySelector('#press-start');
  let active = true;
  const fit = () => {
    if (!active || !frame.isConnected) return;
    const scale = Math.min(viewport.clientWidth / 1600, viewport.clientHeight / 900);
    if (scale <= 0) return;
    frame.style.width = `${1600 * scale}px`;
    frame.style.height = `${900 * scale}px`;
    for (const [name, value] of Object.entries({
      '--cover-scale': scale,
      '--cover-cta-bottom': `${75 * scale}px`,
      '--cover-cta-height': `${Math.max(44, 75 * scale)}px`,
      '--cover-control-font': `${Math.max(16, 32 * scale)}px`,
      '--cover-field-font': `${Math.max(14, 17 * scale)}px`,
      '--cover-field-gap': `${Math.max(8, 20 * scale)}px`,
      '--cover-field-tracking': `${scale < .6 ? 0 : 4 * scale}px`,
      '--cover-location-font': `${Math.max(21, 14 / scale)}px`,
    })) frame.style.setProperty(name, String(value));
    start.disabled = innerHeight > innerWidth;
  };
  const observer = typeof ResizeObserver === 'function' ? new ResizeObserver(fit) : null;
  if (observer) observer.observe(viewport);
  else window.addEventListener('resize', fit);
  fit();
  return () => {
    if (!active) return;
    active = false;
    observer?.disconnect();
    window.removeEventListener('resize', fit);
  };
}
