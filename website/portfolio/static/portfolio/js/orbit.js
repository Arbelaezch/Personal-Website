// The tethered orbit: the featured projects circle the centre on elastic strings (issue #101).
// Ported from docs/design/orbit-prototype.html, which the owner tuned by hand: keep the numbers
// below unless they ask for a change.
//
// The page works without this file. featured.js owns which project is selected; this module draws
// the orbit, asks for a selection with a "featured:pick" event and follows "featured:selected".

var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var IDLE = reduced ? 0 : 0.12;   // resting spin, radians per second
var BREAK = 8;                   // spin speed at which projects let go
var MAX_SPIN = 16;
var FREE_TIME = 3;               // seconds before released projects return
var HIT = 26;                    // pointer radius around a project
var CLICK_SLOP = 6;              // movement under this counts as a click
var SLACK = 30;                  // pixels past the orbit before the string resists
var STRETCH = 110;               // the most a string can stretch past that
var STRAIN_AT = 0.6;             // share of full stretch that counts as straining
var SNAP_TIME = 1.8;             // seconds of strain before the string breaks
var REST_TIME = 3;               // seconds a dropped project lies on the floor
var STRAIN_COL = '#ff6b5e';        // a strained string
var COMPACT_BELOW = 520;         // stage width under which only the selected project is labelled
var FULL_PULL_WIDTH = 620;       // stage width from which strings stretch the full distance
var MIN_PROJECTS = 3;
var MAX_PROJECTS = 7;
var FONT_BODY = 'Archivo, "Helvetica Neue", Arial, sans-serif';
var FONT_MONO = '"JetBrains Mono", Menlo, Consolas, monospace';
var C = {};  // colours, read from the design tokens in css/site.css

function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }

function readColours(element) {
  var style = getComputedStyle(element);
  var tokens = {
    stage: '--stage', line: '--line', lineStrong: '--line-strong', text: '--text',
    muted: '--muted', node: '--node', accent: '--accent', panel: '--panel'
  };
  for (var name in tokens) C[name] = style.getPropertyValue(tokens[name]).trim() || '#888888';
}

// Where each project sits: up to three on the inner ring, the rest on the outer one, spread evenly
// and offset so that an inner and an outer project never share an angle.
function layout(count) {
  var inner = count <= 3 ? 0 : count <= 6 ? 2 : 3;
  var outer = count - inner;
  var places = [];
  for (var i = 0; i < inner; i++) places.push({ ring: 0, a: i * 2 * Math.PI / inner });
  var offset = outer % 2 ? Math.PI / 2 : Math.PI / outer;
  for (var j = 0; j < outer; j++) places.push({ ring: 1, a: offset + j * 2 * Math.PI / outer });
  return places;
}

function Orbit(section, canvas, projects, status) {
  var self = this;
  this.section = section;
  this.canvas = canvas;
  this.ctx = canvas.getContext('2d');
  this.projects = projects;
  this.status = status;
  this.said = '';
  this.theta = 0;
  this.omega = IDLE;
  this.sel = 0;
  this.hover = -1;
  this.drag = null;
  this.spin = null;
  this.W = 0; this.H = 0;
  this.compact = false;
  this.pull = 1;

  var places = layout(projects.length);
  this.nodes = projects.map(function (p, i) {
    return {
      i: i, ring: places[i].ring, a: places[i].a, x: 0, y: 0, vx: 0, vy: 0,
      mode: 'attached', t: 0, strain: 0, alpha: 1, scale: 1, snapT: 1, stubX: 0, stubY: 0
    };
  });

  canvas.addEventListener('pointerdown', function (e) { self.onDown(e); });
  canvas.addEventListener('pointermove', function (e) { self.onMove(e); });
  canvas.addEventListener('pointerup', function (e) { self.onUp(e); });
  canvas.addEventListener('pointercancel', function (e) { self.onUp(e); });
  canvas.addEventListener('pointerleave', function () { if (!self.drag && !self.spin) self.hover = -1; });

  this.resize(true);
}

Orbit.prototype.pick = function (i) {
  this.section.dispatchEvent(new CustomEvent('featured:pick', { detail: { index: i } }));
};

// "SPIN" and "STRAIN" change every frame and mean nothing read aloud; the countdowns do.
Orbit.prototype.announce = function (label) {
  var text = '';
  if (label !== 'SPIN' && label !== 'STRAIN') {
    text = label.charAt(0) + label.slice(1).toLowerCase().replace(/(\d+)s$/, '$1 seconds');
  }
  if (text !== this.said) {
    this.said = text;
    this.status.textContent = text;
  }
};

Orbit.prototype.resize = function (snap) {
  var rect = this.canvas.getBoundingClientRect();
  var w = Math.max(200, rect.width), h = Math.max(200, rect.height);
  if (!snap && w === this.W && h === this.H) return;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  this.W = w; this.H = h;
  this.canvas.width = Math.round(w * dpr);
  this.canvas.height = Math.round(h * dpr);
  this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  this.cx = w / 2;
  this.cy = h / 2 - 10;
  // On a narrow stage only the selected project is labelled, so the rings can use more of the width.
  this.compact = w < COMPACT_BELOW;
  var base = Math.min(w * (this.compact ? 0.96 : 0.82), h);
  this.radii = [base * 0.25, base * 0.39];
  // Strings stretch less on a small stage, so a finger can still strain one without leaving the screen.
  this.pull = clamp(w / FULL_PULL_WIDTH, 0.5, 1);
  for (var k = 0; k < this.nodes.length; k++) {
    var n = this.nodes[k];
    if (n.mode === 'attached' || snap) {
      var hm = this.home(n);
      n.x = hm.x; n.y = hm.y; n.vx = hm.vx; n.vy = hm.vy;
    }
  }
};

Orbit.prototype.home = function (n) {
  var stretch = 1 + Math.min(0.8, 0.012 * this.omega * this.omega);
  var r = this.radii[n.ring] * stretch;
  var ang = this.theta + n.a;
  var cos = Math.cos(ang), sin = Math.sin(ang);
  return { x: this.cx + r * cos, y: this.cy + r * sin, vx: -this.omega * r * sin, vy: this.omega * r * cos };
};

Orbit.prototype.reset = function () {
  this.omega = IDLE;
  this.spin = null;
  this.drag = null;
  for (var k = 0; k < this.nodes.length; k++) {
    var n = this.nodes[k];
    if (n.mode !== 'attached') n.mode = 'returning';
    n.alpha = 1; n.scale = 1; n.strain = 0;
  }
};

Orbit.prototype.pos = function (e) {
  var r = this.canvas.getBoundingClientRect();
  return { x: e.clientX - r.left, y: e.clientY - r.top };
};

Orbit.prototype.nodeAt = function (p) {
  var best = -1, bestD = HIT * HIT;
  for (var k = 0; k < this.nodes.length; k++) {
    var n = this.nodes[k];
    if (n.mode === 'falling' || n.mode === 'resting' || n.mode === 'fading') continue;
    var dx = n.x - p.x, dy = n.y - p.y, d = dx * dx + dy * dy;
    if (d < bestD) { bestD = d; best = k; }
  }
  return best;
};

Orbit.prototype.onDown = function (e) {
  if (e.button !== undefined && e.button !== 0) return;
  var p = this.pos(e);
  var hit = this.nodeAt(p);
  try { this.canvas.setPointerCapture(e.pointerId); } catch (err) {}
  if (hit >= 0) {
    this.drag = { node: this.nodes[hit], sx: p.x, sy: p.y, tx: p.x, ty: p.y, moved: false, hold: 0 };
  } else {
    this.spin = { ang: Math.atan2(p.y - this.cy, p.x - this.cx), t: performance.now(), last: performance.now() };
  }
  this.canvas.classList.add('grabbing');
};

Orbit.prototype.onMove = function (e) {
  var p = this.pos(e);
  if (this.drag) {
    var d = this.drag;
    d.tx = p.x;
    d.ty = p.y;
    if (!d.moved && Math.hypot(p.x - d.sx, p.y - d.sy) > CLICK_SLOP) {
      d.moved = true;
      d.node.mode = 'dragged';
      this.pick(d.node.i);
    }
  } else if (this.spin) {
    var s = this.spin;
    var ang = Math.atan2(p.y - this.cy, p.x - this.cx);
    var dA = ang - s.ang;
    if (dA > Math.PI) dA -= 2 * Math.PI;
    if (dA < -Math.PI) dA += 2 * Math.PI;
    var now = performance.now();
    var dt = Math.max(0.004, (now - s.t) / 1000);
    this.theta += dA;
    this.omega = clamp(this.omega * 0.7 + (dA / dt) * 0.3, -MAX_SPIN, MAX_SPIN);
    s.ang = ang; s.t = now; s.last = now;
  } else {
    this.hover = this.nodeAt(p);
  }
};

Orbit.prototype.onUp = function (e) {
  try { this.canvas.releasePointerCapture(e.pointerId); } catch (err) {}
  this.canvas.classList.remove('grabbing');
  if (this.drag) {
    var d = this.drag, n = d.node;
    if (!d.moved) {
      this.pick(n.i);
    } else {
      var speed = Math.hypot(n.vx, n.vy);
      if (speed > 2600) { n.vx *= 2600 / speed; n.vy *= 2600 / speed; speed = 2600; }
      n.strain = 0;
      if (n.mode === 'held') {
        n.mode = 'falling'; n.t = 0;
      } else {
        n.mode = 'attached';
      }
    }
    this.drag = null;
  }
  this.spin = null;
};

Orbit.prototype.step = function (dt) {
  var k, n, h;
  if (this.spin) {
    // The pointer drives the angle. Let the measured speed fall away if the pointer stops moving.
    if (performance.now() - this.spin.last > 60) this.omega *= Math.exp(-dt / 0.1);
  } else {
    this.omega += (IDLE - this.omega) * (1 - Math.exp(-dt / 1.2));
    this.theta += this.omega * dt;
  }

  if (Math.abs(this.omega) > BREAK) {
    for (k = 0; k < this.nodes.length; k++) {
      n = this.nodes[k];
      if (n.mode !== 'attached') continue;
      h = this.home(n);
      var ox = n.x - this.cx, oy = n.y - this.cy, ol = Math.hypot(ox, oy) || 1;
      n.vx = h.vx * 0.7 + (ox / ol) * 160;
      n.vy = h.vy * 0.7 + (oy / ol) * 160;
      var sp = Math.hypot(n.vx, n.vy);
      if (sp > 1700) { n.vx *= 1700 / sp; n.vy *= 1700 / sp; }
      n.mode = 'free'; n.t = 0;
    }
  }

  for (k = 0; k < this.nodes.length; k++) {
    n = this.nodes[k];
    h = this.home(n);
    if (n.snapT < 1) n.snapT += dt;
    if ((n.mode === 'dragged' || n.mode === 'held') && this.drag) {
      var dg = this.drag;
      var tx = dg.tx, ty = dg.ty;
      if (n.mode === 'dragged') {
        // The string resists: past the slack, the project falls further behind the pointer.
        var qx = tx - this.cx, qy = ty - this.cy, Lp = Math.hypot(qx, qy) || 1;
        var slack = SLACK * this.pull, stretchMax = STRETCH * this.pull;
        var Ls = this.radii[n.ring] + slack, L = Lp;
        n.strain = 0;
        if (Lp > Ls) {
          L = Ls + stretchMax * (1 - Math.exp(-(Lp - Ls) / stretchMax));
          n.strain = (L - Ls) / stretchMax;
        }
        tx = this.cx + qx / Lp * L;
        ty = this.cy + qy / Lp * L;
        if (n.strain > STRAIN_AT) dg.hold += dt; else dg.hold = Math.max(0, dg.hold - dt * 2);
        if (dg.hold >= SNAP_TIME) {
          n.mode = 'held'; n.strain = 0; n.snapT = 0; n.stubX = n.x; n.stubY = n.y;
        }
      }
      tx = clamp(tx, 14, this.W - 14);
      ty = clamp(ty, 14, this.H - 52);
      if (n.mode === 'held') {
        // Broken free: ease to the pointer, then the stub of string whips back to the centre.
        tx = n.x + (tx - n.x) * Math.min(1, dt * 18);
        ty = n.y + (ty - n.y) * Math.min(1, dt * 18);
      }
      n.vx = n.vx * 0.5 + ((tx - n.x) / dt) * 0.5;
      n.vy = n.vy * 0.5 + ((ty - n.y) / dt) * 0.5;
      n.x = tx; n.y = ty;
    } else if (n.mode === 'falling') {
      var floor = this.H - 52;
      n.t += dt;
      n.vy += 1900 * dt;
      n.x += n.vx * dt; n.y += n.vy * dt;
      if (n.x < 14) { n.x = 14; n.vx = Math.abs(n.vx) * 0.5; }
      if (n.x > this.W - 14) { n.x = this.W - 14; n.vx = -Math.abs(n.vx) * 0.5; }
      if (n.y < 14) { n.y = 14; n.vy = Math.abs(n.vy) * 0.5; }
      if (n.y >= floor) {
        n.y = floor;
        n.vx *= 0.7;
        if (Math.abs(n.vy) < 140 || n.t > 5) { n.vy = 0; n.mode = 'resting'; n.t = 0; }
        else n.vy = -n.vy * 0.38;
      }
    } else if (n.mode === 'resting') {
      n.t += dt;
      n.vx *= Math.exp(-6 * dt);
      n.x = clamp(n.x + n.vx * dt, 14, this.W - 14);
      if (n.t > REST_TIME) { n.mode = 'fading'; n.t = 0; }
    } else if (n.mode === 'fading') {
      n.t += dt;
      n.alpha = Math.max(0, 1 - n.t / 0.5);
      if (n.t >= 0.5) {
        // A replacement grows out of the centre on a new string.
        n.x = this.cx; n.y = this.cy; n.vx = 0; n.vy = 0;
        n.alpha = 1; n.scale = 0; n.mode = 'returning';
      }
    } else if (n.mode === 'attached') {
      // Under-damped spring to the orbit position: this is the elastic snap.
      n.vx += (140 * (h.x - n.x) - 6 * (n.vx - h.vx)) * dt;
      n.vy += (140 * (h.y - n.y) - 6 * (n.vy - h.vy)) * dt;
      n.x += n.vx * dt; n.y += n.vy * dt;
    } else if (n.mode === 'free') {
      n.t += dt;
      var drag = Math.exp(-0.5 * dt);
      n.vx *= drag; n.vy *= drag;
      n.x += n.vx * dt; n.y += n.vy * dt;
      if (n.x < 14) { n.x = 14; n.vx = Math.abs(n.vx) * 0.82; }
      if (n.x > this.W - 14) { n.x = this.W - 14; n.vx = -Math.abs(n.vx) * 0.82; }
      if (n.y < 14) { n.y = 14; n.vy = Math.abs(n.vy) * 0.82; }
      if (n.y > this.H - 44) { n.y = this.H - 44; n.vy = -Math.abs(n.vy) * 0.82; }
      if (n.t > FREE_TIME) n.mode = 'returning';
    } else {
      // Returning: a critically damped spring, so it glides home without overshoot.
      if (n.scale < 1) n.scale = Math.min(1, n.scale + dt / 0.45);
      n.vx += (30 * (h.x - n.x) - 11 * (n.vx - h.vx)) * dt;
      n.vy += (30 * (h.y - n.y) - 11 * (n.vy - h.vy)) * dt;
      n.x += n.vx * dt; n.y += n.vy * dt;
      if (Math.hypot(h.x - n.x, h.y - n.y) < 1.5 && Math.hypot(n.vx - h.vx, n.vy - h.vy) < 30) n.mode = 'attached';
    }
  }
};

Orbit.prototype.draw = function () {
  var ctx = this.ctx, W = this.W, H = this.H, k, n;
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = C.stage;
  ctx.fillRect(0, 0, W, H);

  // Rings
  ctx.lineWidth = 1;
  for (k = 0; k < 2; k++) {
    ctx.beginPath();
    ctx.arc(this.cx, this.cy, this.radii[k], 0, Math.PI * 2);
    ctx.strokeStyle = C.line;
    ctx.setLineDash([3, 7]);
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // Strings
  for (k = 0; k < this.nodes.length; k++) {
    n = this.nodes[k];
    if (n.snapT < 0.2) {
      var back = 1 - n.snapT / 0.2;
      ctx.beginPath();
      ctx.moveTo(this.cx, this.cy);
      ctx.lineTo(this.cx + (n.stubX - this.cx) * back, this.cy + (n.stubY - this.cy) * back);
      ctx.lineWidth = 1; ctx.strokeStyle = STRAIN_COL; ctx.globalAlpha = 0.9; ctx.setLineDash([]);
      ctx.stroke();
    }
    if (n.mode === 'held' || n.mode === 'falling' || n.mode === 'resting' || n.mode === 'fading') continue;
    var dx = n.x - this.cx, dy = n.y - this.cy, len = Math.hypot(dx, dy) || 1;
    var ext = len / this.radii[n.ring] - 1;
    var loose = n.mode === 'free';
    // Bow the string against the direction of travel so it reads as elastic.
    var px = -dy / len, py = dx / len;
    var hm = this.home(n);
    var lag = n.mode === 'dragged' ? 0 : clamp(-((n.vx - hm.vx) * px + (n.vy - hm.vy) * py) * 0.035, -46, 46);
    var tight = n.strain > STRAIN_AT;
    if (tight && !reduced) lag += (Math.random() - 0.5) * 7 * n.strain;
    ctx.beginPath();
    ctx.moveTo(this.cx, this.cy);
    ctx.quadraticCurveTo(this.cx + dx / 2 + px * lag, this.cy + dy / 2 + py * lag, n.x, n.y);
    ctx.lineWidth = loose ? 1 : clamp(2.2 - ext * 1.1 - n.strain * 0.8, 0.6, 2.2);
    ctx.strokeStyle = tight ? STRAIN_COL : (n.i === this.sel ? C.accent : C.node);
    ctx.globalAlpha = loose ? 0.3 : (tight ? 1 : 0.75);
    ctx.setLineDash(loose ? [4, 6] : []);
    ctx.stroke();
  }
  ctx.setLineDash([]);
  ctx.globalAlpha = 1;

  // Centre
  ctx.beginPath();
  ctx.arc(this.cx, this.cy, 34, 0, Math.PI * 2);
  ctx.fillStyle = C.panel;
  ctx.fill();
  ctx.strokeStyle = C.node;
  ctx.lineWidth = 1;
  ctx.stroke();
  ctx.fillStyle = C.text;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.font = '800 18px ' + FONT_BODY;
  ctx.fillText('CA', this.cx, this.cy + 1);

  // Projects
  for (k = 0; k < this.nodes.length; k++) {
    n = this.nodes[k];
    var p = this.projects[n.i];
    var on = n.i === this.sel;
    var col = on ? C.accent : C.node;
    var big = this.hover === k || n.mode === 'dragged' || n.mode === 'held';
    ctx.globalAlpha = n.alpha * Math.min(1, n.scale * 1.5);
    ctx.beginPath();
    ctx.arc(n.x, n.y, (big ? 17 : 13) * n.scale, 0, Math.PI * 2);
    ctx.fillStyle = C.stage;
    ctx.fill();
    ctx.strokeStyle = col;
    ctx.lineWidth = on ? 2 : 1;
    ctx.stroke();
    if (!this.compact) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, 5 * n.scale, 0, Math.PI * 2);
      ctx.fillStyle = col;
      ctx.fill();
    }
    ctx.globalAlpha = n.alpha * n.scale;

    ctx.lineJoin = 'round';
    if (this.compact) {
      ctx.textBaseline = 'middle';
      ctx.font = '500 11px ' + FONT_MONO;
      ctx.fillStyle = col;
      ctx.fillText(String(n.i + 1), n.x, n.y + 1);
    }
    if (!this.compact || on) {
      ctx.textBaseline = 'alphabetic';
      ctx.lineWidth = 5;
      ctx.strokeStyle = C.stage;
      ctx.font = '600 14px ' + FONT_BODY;
      // Keep the label on the stage when its project is against a wall.
      var half = ctx.measureText(p.title).width / 2 + 8;
      var lx = half * 2 < W ? clamp(n.x, half, W - half) : n.x;
      ctx.strokeText(p.title, lx, n.y + 34);
      ctx.fillStyle = on ? C.accent : C.text;
      ctx.fillText(p.title, lx, n.y + 34);
      ctx.font = '400 11px ' + FONT_MONO;
      ctx.strokeText(p.meta, lx, n.y + 49);
      ctx.fillStyle = C.muted;
      ctx.fillText(p.meta, lx, n.y + 49);
    }
    ctx.globalAlpha = 1;
  }

  // Spin meter and status
  var freeLeft = 0;
  for (k = 0; k < this.nodes.length; k++) {
    if (this.nodes[k].mode === 'free') freeLeft = Math.max(freeLeft, FREE_TIME - this.nodes[k].t);
  }
  var restLeft = 0;
  for (k = 0; k < this.nodes.length; k++) {
    if (this.nodes[k].mode === 'resting') restLeft = Math.max(restLeft, REST_TIME - this.nodes[k].t);
  }
  var frac = clamp(Math.abs(this.omega) / BREAK, 0, 1);
  var label = 'SPIN', barCol = frac > 0.7 ? C.accent : C.node;
  if (this.drag && this.drag.node.mode === 'dragged' && this.drag.hold > 0) {
    label = 'STRAIN'; frac = clamp(this.drag.hold / SNAP_TIME, 0, 1); barCol = STRAIN_COL;
  } else if (restLeft > 0) {
    label = 'REPLACING IN ' + Math.ceil(restLeft) + 'S';
  } else if (freeLeft > 0) {
    label = 'RETURNING IN ' + Math.ceil(freeLeft) + 'S';
  }
  ctx.textAlign = 'left';
  ctx.font = '400 11px ' + FONT_MONO;
  ctx.fillStyle = C.muted;
  ctx.fillText(label, 16, 24);
  this.announce(label);
  ctx.fillStyle = C.line;
  ctx.fillRect(16, 32, 120, 4);
  ctx.fillStyle = barCol;
  ctx.fillRect(16, 32, 120 * frac, 4);
};

function start(section) {
  var links = [].slice.call(section.querySelectorAll('[data-featured-link]'));
  var stage = section.querySelector('.featured-stage');
  if (!stage || links.length < MIN_PROJECTS || links.length > MAX_PROJECTS) return;

  var canvas = document.createElement('canvas');
  if (!canvas.getContext || !canvas.getContext('2d')) return;
  canvas.className = 'orbit-canvas';
  canvas.setAttribute('role', 'img');
  canvas.setAttribute('aria-label', 'Interactive orbit of the featured projects. The list after it selects the same projects.');

  var bar = document.createElement('div');
  bar.className = 'orbit-bar';
  var hint = document.createElement('p');
  hint.className = 'orbit-hint';
  hint.textContent = 'Pull a project to stretch its string. Hold it tight to break it. Drag the empty space to spin.';
  var reset = document.createElement('button');
  reset.type = 'button';
  reset.className = 'orbit-reset';
  reset.textContent = 'Reset';
  bar.append(hint, reset);

  var status = document.createElement('p');
  status.className = 'visually-hidden';
  status.setAttribute('aria-live', 'polite');

  readColours(section);
  var projects = links.map(function (link) {
    return { title: link.querySelector('.featured-title').textContent.trim(), meta: link.dataset.orbitMeta || '' };
  });

  stage.prepend(canvas);
  stage.append(bar, status);
  section.classList.add('has-orbit');

  var orbit = new Orbit(section, canvas, projects, status);
  var current = links.findIndex(function (link) { return link.getAttribute('aria-current') === 'true'; });
  orbit.sel = current < 0 ? 0 : current;
  section.addEventListener('featured:selected', function (e) { orbit.sel = e.detail.index; });
  reset.addEventListener('click', function () { orbit.reset(); });

  // Draw only while the stage is on screen (a hidden tab pauses requestAnimationFrame by itself).
  var visible = true, running = false, last = 0;
  function frame(now) {
    if (!visible) { running = false; return; }
    var dt = Math.min(0.033, (now - last) / 1000);
    last = now;
    orbit.resize(false);
    if (dt > 0) {
      orbit.step(dt / 2);
      orbit.step(dt / 2);
    }
    orbit.draw();
    requestAnimationFrame(frame);
  }
  function wake() {
    if (running || !visible) return;
    running = true;
    last = performance.now();
    requestAnimationFrame(frame);
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[entries.length - 1].isIntersecting;
      wake();
    }).observe(canvas);
  }
  wake();
  section.orbit = orbit;  // lets browser tests read the simulation
}

var section = document.querySelector('.featured');
if (section) start(section);
