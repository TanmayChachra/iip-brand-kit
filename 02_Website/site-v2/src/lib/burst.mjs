// The brand sunburst (kit asset): 24 teeth, outer radius R, inner radius r, as an SVG polygon points string.
export const burst = (cx = 400, cy = 400, R = 340, r = 299, n = 24) =>
  Array.from({ length: n * 2 }, (_, i) => {
    const a = (Math.PI * i) / n - Math.PI / 2, rad = i % 2 ? r : R;
    return `${(cx + rad * Math.cos(a)).toFixed(1)},${(cy + rad * Math.sin(a)).toFixed(1)}`;
  }).join(' ');
