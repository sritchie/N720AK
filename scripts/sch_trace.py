#!/usr/bin/env python3
"""
Net tracing for vector-PDF schematics.

On a drawing like the SkyView interconnect, pin names are text but *which pin
connects to which* exists only in the line geometry. This module rebuilds that
connectivity from the PDF's line segments.

Conventions it encodes, measured on the SteinAir drawings rather than assumed:

* Lines are split wherever anything meets them, crossings included, so
  sharing an endpoint does not by itself mean two lines connect.
* Collinear segments always continue through a meeting point.
* A corner or a T joins -- only three of the four directions are present, so
  the meeting is unambiguous whether or not a dot is drawn.
* A four-way meeting is a CROSSING unless a junction dot is drawn there.
* Diagonal segments and curves do not conduct: on these drawings they are
  switch contacts, arrowheads and shield ovals -- with one exception. A wire
  that crosses another without connecting HOPS it: a small semicircle made of
  two bezier pieces whose ends sit on the same line. Hops are bridged with a
  straight segment so the wire stays whole; the line being hopped then crosses
  that segment's interior and correctly stays separate. Missing this cut every
  hopping wire in two and lost, among others, the GTN-to-ELT GPS feed.
* Dashed lines do not conduct. They are annotation -- the GPS-250's "Builder
  Connection" is a dashed line with a dot on each of four wires, meaning
  "splice each of these here", not "join them". Treating it as a wire fused
  GPS power, ground and Serial 5 into one net.

Connector boxes are recognised by their narrow pin-number columns. A wire
belongs to a pin when it ends on a column's outer edge at that pin's row.
"""

import collections
import re

EPS = 0.6


class UF:
    def __init__(self):
        self.p = {}

    def find(self, a):
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


JACKS, DASHED = [], []          # filled in by load(); see below


def load(pdf, max_width=1.5):
    """Return (segments, rects, dots, words) for page 1.

    Also fills the module-level JACKS (centres of jack contacts) and DASHED
    (dashed enclosures) lists. Two kinds of small filled circle look alike
    and must not be confused: BLACK ones are junction dots, WHITE ones are the
    contacts of a headset jack. Counting the white ones as junctions was an
    early bug.
    """
    JACKS.clear()
    DASHED.clear()
    import pymupdf
    page = pymupdf.open(pdf)[0]
    segs, rects, dots = [], [], []
    hops = 0
    for d in page.get_drawings():
        curves = [(it[1], it[4]) for it in d["items"] if it[0] == "c"]
        for (a0, a1), (b0, b1) in zip(curves, curves[1:]):
            if abs(a1.x - b0.x) > 0.3 or abs(a1.y - b0.y) > 0.3:
                continue
            if abs(a0.y - b1.y) < 0.3 and 3 <= abs(a0.x - b1.x) <= 14 and 1 <= abs(a1.y - a0.y) <= 6:
                segs.append(("H", min(a0.x, b1.x), a0.y, max(a0.x, b1.x), a0.y)); hops += 1
            elif abs(a0.x - b1.x) < 0.3 and 3 <= abs(a0.y - b1.y) <= 14 and 1 <= abs(a1.x - a0.x) <= 6:
                segs.append(("V", a0.x, min(a0.y, b1.y), a0.x, max(a0.y, b1.y))); hops += 1
        r = d["rect"]
        if (d.get("fill") is not None and r.width < 8 and r.height < 8
                and any(it[0] == "c" for it in d["items"])):
            c = ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
            if max(d["fill"]) < 0.5:
                dots.append(c)
            elif 3.5 < r.width < 6:
                JACKS.append(c)
        if str(d.get("dashes") or "[] 0").strip() not in ("[] 0", "[]") and \
                any(it[0] == "re" for it in d["items"]):
            DASHED.append(r)
        dashed = str(d.get("dashes") or "[] 0").strip() not in ("[] 0", "[]")
        for it in d["items"]:
            if it[0] == "l" and (d.get("width") or 0) < max_width and not dashed:
                a, b = it[1], it[2]
                dx, dy = abs(a.x - b.x), abs(a.y - b.y)
                # Within 3 degrees of an axis is a wire, not a diagonal. Three
                # wires on the power sheet are drawn 0.2-1.3 degrees off
                # vertical, and dropping them as "diagonals" cut the FUEL PUMP 2
                # and ECU FAULT SEC lamp wires in two. Real diagonals here --
                # switch blades, arrowheads -- are all 4 degrees or more.
                if dy <= dx * 0.0524:
                    y = (a.y + b.y) / 2
                    segs.append(("H", min(a.x, b.x), y, max(a.x, b.x), y))
                elif dx <= dy * 0.0524:
                    x = (a.x + b.x) / 2
                    segs.append(("V", x, min(a.y, b.y), x, max(a.y, b.y)))
                # steeper diagonals deliberately dropped: they do not conduct
            elif it[0] == "re":
                rects.append(it[1])
    # The drawings stamp many lines two or three times over. Duplicates must
    # go, or a wire's loose end looks like a meeting of two lines and the
    # device it lands on (a grip PTT switch) is never attached.
    segs = sorted(set((o, round(a, 2), round(b, 2), round(c, 2), round(d, 2))
                      for o, a, b, c, d in snap(segs)))
    seen, words = set(), []
    for x0, y0, x1, y1, t, *_ in page.get_text("words"):
        k = (round(x0, 1), round(y0, 1), t)
        if k not in seen:
            seen.add(k)
            words.append((x0, y0, x1, y1, t))
    return segs, rects, dots, words


def snap(segs, radius=1.0, span=2.0):
    """Make coordinates that nearly coincide coincide exactly.

    The drawing tool leaves sub-point gaps at some corners -- one wire on the
    SkyView sheet ends at x=683.4 and turns down at x=684.0 -- and an exact
    meeting test reads that as two unconnected lines. That disconnected both
    grip PTT switches.

    Snapping is done per axis: every x within `radius` of its neighbour (and
    within `span` overall) takes one value, and likewise every y. Snapping
    points instead moved a whole vertical line sideways when only its top end
    was near something, breaking its other end. Parallel wires and pin rows are
    9 pt or more apart, so this cannot merge two real conductors.
    """
    def axis(vals):
        vals = sorted(set(vals))
        out, group = {}, [vals[0]] if vals else []
        for v in vals[1:]:
            if v - group[-1] <= radius and v - group[0] <= span:
                group.append(v)
            else:
                for g_ in group:
                    out[g_] = group[0]
                group = [v]
        for g_ in group:
            out[g_] = group[0]
        return out
    xs = axis([v for o, x0, y0, x1, y1 in segs for v in (x0, x1)])
    ys = axis([v for o, x0, y0, x1, y1 in segs for v in (y0, y1)])
    return [(o, xs[x0], ys[y0], xs[x1], ys[y1]) for o, x0, y0, x1, y1 in segs]


def connectivity(segs, dots):
    """Union-find over segment indices using the meeting rules above."""
    uf = UF()
    for i in range(len(segs)):
        uf.find(i)
    dotset = {(round(x * 2) / 2, round(y * 2) / 2) for x, y in dots}

    def is_dot(pt):
        k = (round(pt[0] * 2) / 2, round(pt[1] * 2) / 2)
        if k in dotset:
            return True
        return any(abs(pt[0] - x) < 1.2 and abs(pt[1] - y) < 1.2 for x, y in dots)

    H = collections.defaultdict(list)
    V = collections.defaultdict(list)
    for i, s in enumerate(segs):
        # H indexed by its y, V by its x -- the line's fixed coordinate.
        # Indexing V by its starting y (an early bug) meant a wire ending
        # partway along a vertical line was never seen to touch it.
        if s[0] == "H":
            H[round(s[2])].append(i)
        else:
            V[round(s[1])].append(i)

    # every meeting point -> list of (seg index, direction leaving the point)
    meet = collections.defaultdict(list)
    for i, (o, x0, y0, x1, y1) in enumerate(segs):
        if o == "H":
            meet[(round(x0 * 2) / 2, round(y0 * 2) / 2)].append((i, "R"))
            meet[(round(x1 * 2) / 2, round(y1 * 2) / 2)].append((i, "L"))
        else:
            meet[(round(x0 * 2) / 2, round(y0 * 2) / 2)].append((i, "D"))
            meet[(round(x1 * 2) / 2, round(y1 * 2) / 2)].append((i, "U"))

    # segments passing THROUGH a meeting point contribute both directions
    for pt in list(meet):
        x, y = pt
        for k in (round(y) - 1, round(y), round(y) + 1):
            for i in H.get(k, ()):
                _, x0, yy, x1, _ = segs[i]
                if abs(yy - y) < EPS and x0 + EPS < x < x1 - EPS:
                    meet[pt] += [(i, "L"), (i, "R")]
        for k in (round(x) - 1, round(x), round(x) + 1):
            for i in V.get(k, ()):
                xx, y0, _, y1 = segs[i][1], segs[i][2], segs[i][3], segs[i][4]
                if abs(xx - x) < EPS and y0 + EPS < y < y1 - EPS:
                    meet[pt] += [(i, "U"), (i, "D")]

    crossings = 0
    for pt, inc in meet.items():
        dirs = {d for _, d in inc}
        horiz = [i for i, d in inc if d in "LR"]
        vert = [i for i, d in inc if d in "UD"]
        for group in (horiz, vert):
            for i in group[1:]:
                uf.union(group[0], i)
        four_way = {"L", "R"} <= dirs and {"U", "D"} <= dirs
        if horiz and vert:
            if four_way and not is_dot(pt):
                crossings += 1
                continue
            uf.union(horiz[0], vert[0])

    # interior-interior crossings carrying a dot are junctions too
    for kx, vlist in V.items():
        for j in vlist:
            x, y0, y1 = segs[j][1], segs[j][2], segs[j][4]
            for ky in range(int(y0), int(y1) + 1):
                for i in H.get(ky, ()):
                    _, hx0, hy, hx1, _ = segs[i]
                    if hx0 + EPS < x < hx1 - EPS and y0 + EPS < hy < y1 - EPS and is_dot((x, hy)):
                        uf.union(i, j)
    return uf, crossings


def pin_columns(rects, words):
    """Narrow pin-number columns, each with its pins as (pin, y_mid)."""
    cols = []
    for r in rects:
        if 12 <= r.width <= 24 and r.height >= 25:
            pins = []
            for x0, y0, x1, y1, t in words:
                if r.x0 - 1 <= x0 and x1 <= r.x1 + 1 and r.y0 <= y0 and y1 <= r.y1 + 1 and t[0].isdigit():
                    pins.append((t, (y0 + y1) / 2))
            if pins:
                cols.append((r, sorted(pins, key=lambda p: p[1])))
    return cols


def component_names(rects, words, cols):
    """Title for each pin column: the header rects stacked directly above."""
    names = {}
    for r, _ in cols:
        stack, top = [], r.y0
        for _ in range(4):
            hdr = [h for h in rects
                   if abs(h.y1 - top) < 2.5 and h.x0 <= r.x0 + 1 and h.x1 >= r.x1 - 1
                   and h.height < 40 and h.width < 400]
            if not hdr:
                break
            h = min(hdr, key=lambda h: h.width)
            txt = " ".join(t for x0, y0, x1, y1, t in sorted(words, key=lambda w: (w[1], w[0]))
                           if h.x0 - 1 <= x0 and x1 <= h.x1 + 1 and h.y0 - 1 <= y0 and y1 <= h.y1 + 1)
            if txt:
                stack.insert(0, txt)
            top = h.y0
        names[id(r)] = " ".join(stack)
    return names


def _text_in(words, r, pad=1.0):
    return " ".join(t for x0, y0, x1, y1, t in sorted(words, key=lambda w: (round(w[1]), w[0]))
                    if r.x0 - pad <= x0 and x1 <= r.x1 + pad and r.y0 - pad <= y0 and y1 <= r.y1 + pad)


def find_boxes(rects, words):
    """Connector boxes, keyed on their headers.

    Every connector has one or more header rects stacked above its body: an
    18 pt title, a 9 pt subtitle, or -- for a component's second and third
    connectors (GMA 245 J2, GTN P1001) -- the 9 pt subtitle alone. Bodies are
    sometimes one wide rect, sometimes narrow pin-number columns either side.

    A box is emitted from the lowest header in a stack (the one with a body
    directly beneath). Its name is the stack's text top to bottom, prefixed by
    any free text just above it (`PFD - LEFT #1`) so that identical units are
    told apart.

    Returns dicts: name, x0, x1, y0, y1, pins = [(side, pin, y_mid)].
    """
    import re
    uniq = {}
    for r in rects:
        uniq[(round(r.x0, 1), round(r.y0, 1), round(r.x1, 1), round(r.y1, 1))] = r
    rects = list(uniq.values())
    hdrs = [r for r in rects if 6 <= r.height <= 40 and 60 <= r.width <= 200 and _text_in(words, r)]
    span = lambda r, t: r.x0 >= t.x0 - 1.5 and r.x1 <= t.x1 + 1.5 and r.x1 - r.x0 > 8
    boxes = []
    for t in hdrs:
        body = [r for r in rects if span(r, t) and abs(r.y0 - t.y1) < 1.5 and r.height > 20]
        if not body:
            continue
        stack, top = [t], t
        while True:
            up = [h for h in hdrs if abs(h.y1 - top.y0) < 1.5 and abs(h.x0 - t.x0) < 1.5 and abs(h.x1 - t.x1) < 1.5]
            if not up:
                break
            top = up[0]
            stack.insert(0, top)
        name = " ".join(_text_in(words, h) for h in stack)
        inside_any = lambda w: any(r.x0 - 0.5 <= w[0] and w[2] <= r.x1 + 0.5 and r.y0 - 0.5 <= w[1]
                                   and w[3] <= r.y1 + 0.5 and r.width < 1000 for r in rects)
        above = [w for w in words if t.x0 - 10 <= w[0] and w[2] <= t.x1 + 10
                 and top.y0 - 26 <= w[1] and w[3] <= top.y0 + 0.5 and not inside_any(w)]
        if above:
            sup = " ".join(w[4] for w in sorted(above, key=lambda w: (round(w[1]), w[0])))
            name = f"{sup} | {name}"
        y1 = max(r.y1 for r in body)
        pins = []
        for x0, y0, x1, y1w, tok in words:
            if not (t.y1 - 0.5 <= y0 and y1w <= y1 + 1 and tok.isdigit()):
                continue
            ym = (y0 + y1w) / 2
            if t.x0 - 1 <= x0 and x1 <= t.x0 + 21:
                pins.append(("L", tok, ym))
            elif t.x1 - 21 <= x0 and x1 <= t.x1 + 1:
                pins.append(("R", tok, ym))
        if pins:
            func = {}
            for side, tok, ym in pins:
                f = [w for w in words if t.x0 + 21 < w[0] and w[2] < t.x1 - 21 and abs((w[1] + w[3]) / 2 - ym) < 4]
                func[tok] = " ".join(w[4] for w in sorted(f, key=lambda w: w[0]))
            boxes.append(dict(name=name, x0=t.x0, x1=t.x1, y0=top.y0, y1=y1, func=func,
                              pins=sorted(set(pins), key=lambda p: (p[0], p[2]))))
    # a bare designator (J2, P1001) inherits the component above it
    for b in boxes:
        core = b["name"].split(" | ")[-1]
        if re.fullmatch(r"[JP]\d+", core.split()[0]):
            above = [o for o in boxes if o is not b and abs(o["x0"] - b["x0"]) < 2
                     and abs(o["x1"] - b["x1"]) < 2 and o["y1"] <= b["y0"] + 2]
            if above:
                parent = max(above, key=lambda o: o["y1"])["name"].split(" | ")[-1].split()[0]
                b["name"] = b["name"].replace(core, parent + " " + core)
    # self-contained boxes: one rect holding title and pins (VP-X SPORT)
    claimed = [(b["x0"], b["y0"], b["x1"], b["y1"]) for b in boxes]
    for r in rects:
        if not (100 <= r.width <= 200 and 40 <= r.height <= 200):
            continue
        if any(cx0 - 2 <= r.x0 and r.x1 <= cx1 + 2 and cy0 - 2 <= r.y0 and r.y1 <= cy1 + 2
               for cx0, cy0, cx1, cy1 in claimed):
            continue
        head = [w for w in words if r.x0 + 21 < w[0] and w[2] < r.x1 - 21 and r.y0 <= w[1] < r.y0 + 22]
        pins = []
        for x0, y0, x1, y1w, tok in words:
            if r.y0 + 20 <= y0 and y1w <= r.y1 and tok.isdigit():
                if r.x0 - 1 <= x0 and x1 <= r.x0 + 21:
                    pins.append(("L", tok, (y0 + y1w) / 2))
                elif r.x1 - 21 <= x0 and x1 <= r.x1 + 1:
                    pins.append(("R", tok, (y0 + y1w) / 2))
        if head and pins:
            func = {}
            for side, tok, ym in pins:
                f = [w for w in words if r.x0 + 21 < w[0] and w[2] < r.x1 - 21 and abs((w[1] + w[3]) / 2 - ym) < 4]
                func[tok] = " ".join(w[4] for w in sorted(f, key=lambda w: w[0]))
            boxes.append(dict(name=" ".join(w[4] for w in sorted(head, key=lambda w: (round(w[1]), w[0]))),
                              x0=r.x0, x1=r.x1, y0=r.y0, y1=r.y1, func=func,
                              pins=sorted(set(pins), key=lambda p: (p[0], p[2]))))
    return boxes


def labels(rects, words, boxes):
    """Small titled rects that are not connector headers: off-sheet tags such
    as `VP-X J10-2` or `GTN650 P3-30,43,44`."""
    out = []
    hdr = {(round(b["x0"]), round(b["y0"])) for b in boxes}
    seen = set()
    for r in rects:
        k = (round(r.x0), round(r.y0), round(r.x1), round(r.y1))
        if k in seen or (round(r.x0), round(r.y0)) in hdr:
            continue
        seen.add(k)
        if 12 <= r.height <= 90 and 40 <= r.width <= 220:
            txt = _text_in(words, r)
            if txt and not txt.isdigit():
                out.append(dict(name=txt, rect=r))
    return out


def trace(pdf):
    """Pins and labels grouped by electrical connection.

    Returns (nets, boxes, uf, segs) where nets is a list of lists of
    node dicts: {kind: pin|label, ref, pin, side}.
    """
    segs, rects, dots, words = load(pdf)
    boxes = find_boxes(rects, words)

    # A box outline is not a wire. Most boxes are drawn as rectangles, but some
    # (the HDX800's left pin column) are drawn with plain lines, and then every
    # wire landing on that side makes a T with the outline and fuses into one
    # net -- which joined Serial 5 TX to GPS-250 power and ground. Wires end ON
    # a box edge but run outside it, so dropping everything on or inside a box
    # outline is safe.
    def in_box(sg):
        o, x0, y0, x1, y1 = sg
        return any(b["x0"] - 0.8 <= x0 and x1 <= b["x1"] + 0.8 and b["y0"] - 0.8 <= y0 and y1 <= b["y1"] + 0.8
                   for b in boxes)
    segs = [sg for sg in segs if not in_box(sg)]
    uf, crossings = connectivity(segs, dots)
    tags = labels(rects, words, boxes)

    ends = collections.defaultdict(list)
    for i, (o, x0, y0, x1, y1) in enumerate(segs):
        ends[(round(x0), round(y0))].append(i)
        ends[(round(x1), round(y1))].append(i)

    def segs_at(x, y, dx=1.5, dy=3.5):
        hit = []
        for xx in range(int(x - dx) - 1, int(x + dx) + 2):
            for yy in range(int(y - dy) - 1, int(y + dy) + 2):
                for i in ends.get((xx, yy), ()):
                    o, x0, y0, x1, y1 = segs[i]
                    if (abs(x0 - x) <= dx and abs(y0 - y) <= dy) or (abs(x1 - x) <= dx and abs(y1 - y) <= dy):
                        hit.append(i)
        return set(hit)

    # Each pin number is printed on both sides of its row and a wire may leave
    # from either side -- but it is one pin, so both sides are the same node.
    anchor = {}
    for bi, b in enumerate(boxes):
        for side, pin, ym in b["pins"]:
            x = b["x0"] if side == "L" else b["x1"]
            hit = segs_at(x, ym)
            if hit:
                i = next(iter(hit))
                key = (bi, pin)
                if key in anchor:
                    uf.union(anchor[key], i)
                else:
                    anchor[key] = i
    groups = collections.defaultdict(list)
    for (bi, pin), i in anchor.items():
        groups[uf.find(i)].append(dict(kind="pin", ref=boxes[bi]["name"], pin=pin, side=""))
    for t in tags:
        r = t["rect"]
        for i, (o, x0, y0, x1, y1) in enumerate(segs):
            for (x, y) in ((x0, y0), (x1, y1)):
                on_edge = ((abs(x - r.x0) < 1.5 or abs(x - r.x1) < 1.5) and r.y0 - 1 <= y <= r.y1 + 1) or \
                          ((abs(y - r.y0) < 1.5 or abs(y - r.y1) < 1.5) and r.x0 - 1 <= x <= r.x1 + 1)
                if on_edge:
                    groups[uf.find(i)].append(dict(kind="label", ref=t["name"], pin="", side=""))
                    break
    # colour labels sit just above (or on) a horizontal run
    COLS = {"Red", "Blk", "Wht", "Yel", "Grn", "Blu", "Ora", "Brn", "Vio", "Gry", "Gray", "Pur"}
    colours = collections.defaultdict(set)
    for x0, y0, x1, y1, tok in words:
        if tok.split("/")[0] not in COLS:
            continue
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        best = None
        for i, (o, sx0, sy0, sx1, sy1) in enumerate(segs):
            if o == "H" and sx0 - 2 <= cx <= sx1 + 2 and -1 <= sy0 - cy <= 9:
                if best is None or abs(sy0 - cy) < abs(segs[best][2] - cy):
                    best = i
        if best is not None:
            colours[uf.find(best)].add(tok)

    deg = collections.Counter()
    for i, (o, x0, y0, x1, y1) in enumerate(segs):
        deg[(round(x0), round(y0))] += 1
        deg[(round(x1), round(y1))] += 1

    # ---- headset jacks: each contact circle is a pin --------------------
    # Contacts that share an x and sit within a few rows of each other belong
    # to one jack; top to bottom they are tip, ring and sleeve.
    jack_cols = collections.defaultdict(list)
    for x, y in JACKS:
        jack_cols[round(x)].append(y)
    jacks = []
    for x, ys in jack_cols.items():
        ys = sorted(set(round(v, 1) for v in ys))
        run = [ys[0]]
        for y in ys[1:]:
            if y - run[-1] <= 32:
                run.append(y)
            else:
                jacks.append((x, run)); run = [y]
        jacks.append((x, run))
    # Jacks are drawn stacked with the same row pitch inside and between
    # them, so a run of six contacts is two jacks. Every jack here has three.
    jacks = [(x, run[k:k + 3]) for x, run in jacks for k in range(0, len(run), 3)]
    for ji, (x, ys) in enumerate(jacks):
        names = ["T", "R", "S"] if len(ys) == 3 else ["T", "S"] if len(ys) == 2 else [str(i + 1) for i in range(len(ys))]
        for y, nm in zip(ys, names):
            for i, (o, x0, y0, x1, y1) in enumerate(segs):
                # The wire leaves a contact sideways; the jack's own spring line
                # meets it from above. Only the wire counts.
                if o == "H" and any(1.5 <= abs(px - x) <= 4.5 and abs(py - y) <= 1.5
                                    for px, py in ((x0, y0), (x1, y1))):
                    groups[uf.find(i)].append(dict(kind="pin", ref=f"JACK@{x},{round(ys[0])}", pin=nm, side=""))
                    break

    # ---- pin columns with a free-text title (the Bose LEMO jacks) --------
    cols = pin_columns(rects, words)
    claimed_cols = [(b["x0"], b["y0"], b["x1"], b["y1"]) for b in boxes]
    for r, pins in cols:
        if any(cx0 - 2 <= r.x0 and r.x1 <= cx1 + 2 and cy0 - 2 <= r.y0 and r.y1 <= cy1 + 2
               for cx0, cy0, cx1, cy1 in claimed_cols):
            continue
        title = [w for w in words if r.x0 - 40 <= w[0] and w[2] <= r.x1 + 40 and r.y0 - 40 <= w[1] < r.y0 - 1]
        if not title:
            continue
        name = " ".join(w[4] for w in sorted(title, key=lambda w: (round(w[1]), w[0])))
        if re.fullmatch(r"DB-?\d+", name):
            continue        # the network-cable pinout table: a reference, not wiring
        for pin, ym in pins:
            for i in segs_at(r.x1, ym):
                groups[uf.find(i)].append(dict(kind="pin", ref=name, pin=pin, side=""))
                break

    # ---- dashed enclosures are devices (grips) ---------------------------
    # A wire that ends inside one ends on that device. Its pin is the button
    # label directly ABOVE the end: each button is drawn with its label over
    # its contacts, and "nearest label" picked the next button down. A switch
    # wired out on both sides (PTT) gets -1 and -2 pins, left to right.
    dev_nodes = collections.defaultdict(list)
    for r in DASHED:
        inside = [w for w in words if r.x0 <= w[0] and w[2] <= r.x1 and r.y0 <= w[1] and w[3] <= r.y1]
        if not inside:
            continue
        # the device is named by the line containing GRIP(S) -- usually the
        # top line, but the copilot trim box puts its title at the bottom
        titled = [w for w in inside if "GRIP" in w[4]]
        ty = titled[0][1] if titled else min(w[1] for w in inside)
        dev = " ".join(w[4] for w in sorted(inside, key=lambda w: w[0]) if abs(w[1] - ty) < 3)
        if dev == "GRIP" or dev == "GRIPS":
            # "COPILOT" printed just outside the box
            near = [w for w in words if -20 <= w[1] - ty < 3 and r.x0 - 60 <= w[0] < r.x1 and w[4].isupper()
                    and w[4] not in ("GRIP", "GRIPS")]
            if near:
                dev = " ".join(w[4] for w in sorted(near, key=lambda w: w[0])) + " " + dev
        labels_in = [w for w in inside if abs(w[1] - ty) >= 3 and (len(w[4]) > 1 or w[4].isdigit())]
        for i, (o, x0, y0, x1, y1) in enumerate(segs):
            for (px, py) in ((x0, y0), (x1, y1)):
                if not (r.x0 - 1 <= px <= r.x1 + 1 and r.y0 - 1 <= py <= r.y1 + 1):
                    continue
                if deg[(round(px), round(py))] != 1:
                    continue
                above = [w for w in labels_in if w[3] <= py + 2 and abs((w[0] + w[2]) / 2 - px) < 45]
                above.sort(key=lambda w: py - w[3])
                if above:
                    row = [w for w in labels_in if abs(w[1] - above[0][1]) < 3]
                else:   # a few buttons are labelled underneath instead
                    below = sorted((w for w in labels_in if abs((w[0] + w[2]) / 2 - px) < 45),
                                   key=lambda w: abs(w[1] - py))
                    row = [w for w in labels_in if below and abs(w[1] - below[0][1]) < 3]
                lab = " ".join(w[4] for w in sorted(row, key=lambda w: w[0])) or "?"
                dev_nodes[dev].append((lab, px, uf.find(i)))
    for dev, ends in dev_nodes.items():
        # ends whose wire goes nowhere but back into the device (the buttons'
        # common return) are dropped before numbering
        ends = [e for e in ends if groups.get(e[2])]
        count = collections.Counter(l for l, _, _ in ends)
        seen = collections.Counter()
        for lab, px, root in sorted(ends, key=lambda e: (e[0], e[1])):
            pin = lab
            if count[lab] > 1:
                seen[lab] += 1
                pin = f"{lab}-{seen[lab]}"
            groups[root].append(dict(kind="pin", ref=dev, pin=pin, side=""))
    # wiring that never leaves a grip (the buttons' common return) is the
    # device's own business, not harness wiring
    for root in list(groups):
        refs = {n["ref"] for n in groups[root]}
        if len(refs) == 1 and next(iter(refs)) in dev_nodes:
            del groups[root]

    # where a traced wire ends at nothing we recognise, name it by nearby text
    deg = collections.Counter()
    for i, (o, x0, y0, x1, y1) in enumerate(segs):
        deg[(round(x0), round(y0))] += 1
        deg[(round(x1), round(y1))] += 1
    claimed = set()
    for b in boxes:
        for side, pin, ym in b["pins"]:
            claimed.add((round(b["x0"] if side == "L" else b["x1"]), round(ym)))
    stop = COLS | {"ga", "Ground", "Power"}
    for root, nodes in list(groups.items()):
        if any(n["kind"] == "label" for n in nodes):
            continue
        # Only name a dangling end from nearby text when the wire would
        # otherwise lead nowhere. A net that already joins two pins does not
        # need it, and stray text (a shield symbol's "S") would be mislabelled.
        if sum(1 for n in nodes if n["kind"] == "pin") >= 2:
            continue
        members = [i for i in range(len(segs)) if uf.find(i) == root]
        hints = []
        for i in members:
            o, x0, y0, x1, y1 = segs[i]
            for (x, y) in ((x0, y0), (x1, y1)):
                k = (round(x), round(y))
                if deg[k] != 1 or any(abs(k[0] - c[0]) <= 2 and abs(k[1] - c[1]) <= 4 for c in claimed):
                    continue
                near = sorted((abs((w[0] + w[2]) / 2 - x) + abs((w[1] + w[3]) / 2 - y), w)
                              for w in words if w[4].split("/")[0] not in stop and not w[4].isdigit()
                              and not any(bb["x0"] - 1 <= w[0] and w[2] <= bb["x1"] + 1
                                          and bb["y0"] - 1 <= w[1] and w[3] <= bb["y1"] + 1 for bb in boxes)
                              and abs((w[0] + w[2]) / 2 - x) < 70 and abs((w[1] + w[3]) / 2 - y) < 22)
                if near:
                    w0 = near[0][1]
                    line = [w for w in words if abs(w[1] - w0[1]) < 3 and abs(w[0] - w0[0]) < 90
                            and w[4].split("/")[0] not in stop]
                    hints.append(" ".join(w[4] for w in sorted(line, key=lambda w: w[0])))
        for h in dict.fromkeys(hints):
            groups[root].append(dict(kind="text", ref=h, pin="", side=""))

    nets = []
    for root, nodes in groups.items():
        uniq, seen = [], set()
        for n in nodes:
            k = (n["kind"], n["ref"], n["pin"])
            if k not in seen:
                seen.add(k)
                uniq.append(n)
        nets.append((root, uniq, sorted(colours.get(root, ()))))
    return nets, boxes, uf, segs, words, crossings
