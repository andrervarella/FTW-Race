// Circuito de Cascavel (Autódromo Internacional Zilmar Beux) — única pista do projeto.
//
// ORIGEM DA GEOMETRIA: pontos de controle traçados À MÃO sobre
// referencias/circuitos/cascavel-mapa-esquematico.png (coordenadas em pixels do PNG).
// Só o traçado azul/verde/vermelho foi seguido; as linhas laranja (boxes/pit lane) NÃO fazem parte do circuito.
// Pista, checkpoints e minimapa saem desta mesma lista. Não é medição oficial (sem comprimento/raio/elevação reais).
//
// SENTIDO: a ordem abaixo percorre a reta dos boxes (direita do mapa) para CIMA, passando pela curva 1 (topo),
// depois 2, 3, 4, 5, 6, 7 e 8. Foi herdado da v0.1.0 e NÃO foi confirmado contra o satélite
// (a seta vermelha do satélite sugere o contrário). Use ?sentido=inverso para testar o outro sentido.
import { ROAD_WIDTH, CHECKPOINTS } from './config.js';

export const WAYPOINTS = [
  [420, 164], [420, 108], [420, 78], [410, 53], [388, 38], [365, 35], [343, 43], [327, 64], [322, 91],
  [322, 151], [323, 195], [329, 213], [349, 230], [363, 245], [366, 259], [359, 273], [337, 281], [300, 294],
  [278, 300], [249, 294], [204, 281], [164, 270], [151, 271], [140, 280], [136, 294], [135, 319], [137, 333],
  [147, 340], [176, 337], [231, 330], [287, 323], [344, 316], [395, 307], [414, 298], [420, 281], [420, 225],
];

const catmull = (a, b, c, d, t) =>
  0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (-a + 3 * b - 3 * c + d) * t * t * t);

export function buildTrack({ reverse = false, scale = 3, samples = 24 } = {}) {
  const wp = (reverse ? [WAYPOINTS[0], ...WAYPOINTS.slice(1).reverse()] : WAYPOINTS).map(([x, y]) => ({ x, y }));
  const n = wp.length;
  const points = [];
  for (let i = 0; i < n; i++) {
    const p0 = wp[(i + n - 1) % n], p1 = wp[i], p2 = wp[(i + 1) % n], p3 = wp[(i + 2) % n];
    for (let s = 0; s < samples; s++) {
      const t = s / samples;
      points.push({ x: catmull(p0.x, p1.x, p2.x, p3.x, t) * scale, y: catmull(p0.y, p1.y, p2.y, p3.y, t) * scale });
    }
  }
  points.push({ ...points[0] }); // fecha o circuito
  const cum = [0];
  for (let i = 1; i < points.length; i++) cum.push(cum[i - 1] + Math.hypot(points[i].x - points[i - 1].x, points[i].y - points[i - 1].y));
  const length = cum[cum.length - 1];
  const wrap = (d) => ((d % length) + length) % length;

  function at(d) {
    d = wrap(d);
    let lo = 0, hi = cum.length - 1;
    while (lo + 1 < hi) { const mid = (lo + hi) >> 1; if (cum[mid] <= d) lo = mid; else hi = mid; }
    const f = (d - cum[lo]) / (cum[hi] - cum[lo]);
    return { x: points[lo].x + (points[hi].x - points[lo].x) * f, y: points[lo].y + (points[hi].y - points[lo].y) * f };
  }
  function sample(d) {
    const c = at(d), b = at(d - 4), a = at(d + 4);
    const heading = Math.atan2(a.y - b.y, a.x - b.x);
    const h0 = Math.atan2(c.y - b.y, c.x - b.x), h1 = Math.atan2(a.y - c.y, a.x - c.x);
    const dh = Math.atan2(Math.sin(h1 - h0), Math.cos(h1 - h0));
    return { x: c.x, y: c.y, heading, curvature: dh / 4 }; // curvatura > 0: curva à direita (eixo y para baixo)
  }
  const xs = points.map((p) => p.x), ys = points.map((p) => p.y);
  return {
    points, length, width: ROAD_WIDTH, scale, reverse, wrap, at, sample,
    checkpointAt: (i) => (length * i) / CHECKPOINTS,
    bounds: { minX: Math.min(...xs), maxX: Math.max(...xs), minY: Math.min(...ys), maxY: Math.max(...ys) },
  };
}
