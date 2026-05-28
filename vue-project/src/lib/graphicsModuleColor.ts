/**
 * Алгоритмы конвертации цвета из Graphics_Module (index.html).
 * Логика совпадает с оригинальным модулем: ICC через Flask, запасная формула + simulatePrintAppearance.
 */

/** Прямой URL Flask-сервера ICC (локальная разработка). */
export const GRAPHICS_MODULE_API = 'http://127.0.0.1:5000'

/** Прокси через Vite — для iframe макета без CORS. */
export const GRAPHICS_MODULE_ICC_PROXY = '/graphics-icc'

export type Rgb = { r: number; g: number; b: number }
export type Cmyk = { c: number; m: number; y: number; k: number }

export type ColorConvertResult = {
  cmyk: Cmyk
  cmykPercents: { c: number; m: number; y: number; k: number }
  previewRgb: Rgb
  previewHex: string
  method: 'icc' | 'simple'
  inkWarning: boolean
}

export function hexToRgb(hex: string): Rgb {
  let h = hex.replace('#', '')
  if (h.length === 3) {
    h = h
      .split('')
      .map((c) => c + c)
      .join('')
  }
  return {
    r: parseInt(h.substring(0, 2), 16),
    g: parseInt(h.substring(2, 4), 16),
    b: parseInt(h.substring(4, 6), 16),
  }
}

export function rgbToHex(r: number, g: number, b: number): string {
  const clamp = (n: number) => Math.min(255, Math.max(0, Math.round(n)))
  const cr = clamp(r)
  const cg = clamp(g)
  const cb = clamp(b)
  return (
    '#' +
    cr.toString(16).padStart(2, '0') +
    cg.toString(16).padStart(2, '0') +
    cb.toString(16).padStart(2, '0')
  )
}

function clamp01(value: number): number {
  return Math.min(1, Math.max(0, value))
}

/** Приводит канал CMYK к диапазону 0–100% (защита от двойного масштабирования). */
function sanitizeCmykPercent(value: number): number {
  if (!Number.isFinite(value)) return 0
  let v = value
  if (v > 0 && v <= 1) v *= 100
  while (v > 100) v /= 100
  return Math.min(100, Math.max(0, Math.round(v * 10) / 10))
}

function buildCmykPercents(raw: { c: number; m: number; y: number; k: number }) {
  return {
    c: sanitizeCmykPercent(raw.c),
    m: sanitizeCmykPercent(raw.m),
    y: sanitizeCmykPercent(raw.y),
    k: sanitizeCmykPercent(raw.k),
  }
}

function shouldWarnInkTotal(cmyk: { c: number; m: number; y: number; k: number }): boolean {
  const total = cmyk.c + cmyk.m + cmyk.y + cmyk.k
  if (total <= 240) return false
  const channels = [cmyk.c, cmyk.m, cmyk.y, cmyk.k]
  if (channels.some((v) => v > 100 || v < 0)) return false
  return true
}

/** Математическая формула RGB→CMYK из Flask app.py (rgb_to_cmyk_simple), значения 0–100%. */
export function rgbToCmykMath(r: number, g: number, b: number): {
  c: number
  m: number
  y: number
  k: number
} {
  let rn = r / 255
  let gn = g / 255
  let bn = b / 255
  let k = 1 - Math.max(rn, gn, bn)
  if (k === 1) return { c: 0, m: 0, y: 0, k: 100 }
  const c = (1 - rn - k) / (1 - k)
  const m = (1 - gn - k) / (1 - k)
  const y = (1 - bn - k) / (1 - k)
  const round1 = (n: number) => Math.round(n * 1000) / 10
  return { c: round1(c * 100), m: round1(m * 100), y: round1(y * 100), k: round1(k * 100) }
}

/** Обратное превью CMYK→RGB из Flask app.py (cmyk_to_rgb_approx), c,m,y,k — доли 0–1. */
export function cmykToRgbApprox(c: number, m: number, y: number, k: number): Rgb {
  const cn = clamp01(c)
  const mn = clamp01(m)
  const yn = clamp01(y)
  const kn = clamp01(k)
  return {
    r: Math.round(255 * (1 - cn) * (1 - kn)),
    g: Math.round(255 * (1 - mn) * (1 - kn)),
    b: Math.round(255 * (1 - yn) * (1 - kn)),
  }
}

/** @deprecated Используйте rgbToCmykMath — оставлено для совместимости с index.html */
export function rgbToCmykSimple(r: number, g: number, b: number): Cmyk {
  const p = rgbToCmykMath(r, g, b)
  return { c: p.c / 100, m: p.m / 100, y: p.y / 100, k: p.k / 100 }
}

function rgbToHsl(r: number, g: number, b: number) {
  r /= 255
  g /= 255
  b /= 255
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  let h = 0
  let s = 0
  const l = (max + min) / 2
  if (max !== min) {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0)
        break
      case g:
        h = (b - r) / d + 2
        break
      default:
        h = (r - g) / d + 4
        break
    }
    h /= 6
  }
  return { h, s, l }
}

function hslToRgb(h: number, s: number, l: number): Rgb {
  let r: number
  let g: number
  let b: number
  if (s === 0) {
    r = g = b = l
  } else {
    const hue2rgb = (p: number, q: number, t: number) => {
      let tt = t
      if (tt < 0) tt += 1
      if (tt > 1) tt -= 1
      if (tt < 1 / 6) return p + (q - p) * 6 * tt
      if (tt < 1 / 2) return q
      if (tt < 2 / 3) return p + (q - p) * (2 / 3 - tt) * 6
      return p
    }
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s
    const p = 2 * l - q
    r = hue2rgb(p, q, h + 1 / 3)
    g = hue2rgb(p, q, h)
    b = hue2rgb(p, q, h - 1 / 3)
  }
  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255),
  }
}

/** Визуальная аппроксимация печати (как в модуле). */
export function simulatePrintAppearance(r: number, g: number, b: number): Rgb {
  const hsl = rgbToHsl(r, g, b)
  hsl.s = Math.max(0, hsl.s - 0.25)
  hsl.l = Math.max(0, hsl.l * 0.88)
  if (hsl.h > 0.55 && hsl.h < 0.75) {
    hsl.s = Math.max(0, hsl.s - 0.15)
    hsl.l = Math.max(0, hsl.l * 0.92)
  }
  return hslToRgb(hsl.h, hsl.s, hsl.l)
}

function cmykToPercents(cmyk: Cmyk): { c: number; m: number; y: number; k: number } {
  return {
    c: Math.round(cmyk.c * 100),
    m: Math.round(cmyk.m * 100),
    y: Math.round(cmyk.y * 100),
    k: Math.round(cmyk.k * 100),
  }
}

function resultFromIccOutput(output: {
  cmyk: { c: number; m: number; y: number; k: number }
  preview_rgb: Rgb
  preview_hex: string
}): ColorConvertResult {
  const cmykPercents = buildCmykPercents(output.cmyk)
  return {
    cmyk: {
      c: cmykPercents.c / 100,
      m: cmykPercents.m / 100,
      y: cmykPercents.y / 100,
      k: cmykPercents.k / 100,
    },
    cmykPercents: {
      c: Math.round(cmykPercents.c),
      m: Math.round(cmykPercents.m),
      y: Math.round(cmykPercents.y),
      k: Math.round(cmykPercents.k),
    },
    previewRgb: output.preview_rgb,
    previewHex: output.preview_hex,
    method: 'icc',
    inkWarning: shouldWarnInkTotal(cmykPercents),
  }
}

function resultFromMathOutput(output: {
  cmyk: { c: number; m: number; y: number; k: number }
  preview_rgb: Rgb
  preview_hex: string
}): ColorConvertResult {
  const cmykPercents = buildCmykPercents(output.cmyk)
  return {
    cmyk: {
      c: cmykPercents.c / 100,
      m: cmykPercents.m / 100,
      y: cmykPercents.y / 100,
      k: cmykPercents.k / 100,
    },
    cmykPercents: {
      c: Math.round(cmykPercents.c),
      m: Math.round(cmykPercents.m),
      y: Math.round(cmykPercents.y),
      k: Math.round(cmykPercents.k),
    },
    previewRgb: {
      r: Math.min(255, Math.max(0, Math.round(output.preview_rgb.r))),
      g: Math.min(255, Math.max(0, Math.round(output.preview_rgb.g))),
      b: Math.min(255, Math.max(0, Math.round(output.preview_rgb.b))),
    },
    previewHex: output.preview_hex || '',
    method: 'simple',
    inkWarning: shouldWarnInkTotal(cmykPercents),
  }
}

function withPreviewHex(result: ColorConvertResult): ColorConvertResult {
  return {
    ...result,
    previewHex: rgbToHex(result.previewRgb.r, result.previewRgb.g, result.previewRgb.b),
  }
}

/**
 * Математический алгоритм для страницы «Графический модуль» (как в Graphics_Module):
 * - CMYK: rgb_to_cmyk_simple из Flask app.py
 * - Превью печати: simulatePrintAppearance (визуальная аппроксимация, не обратная формула CMYK→RGB)
 */
export function convertColorMath(hex: string): ColorConvertResult {
  const rgb = hexToRgb(hex)
  const cmyk = rgbToCmykMath(rgb.r, rgb.g, rgb.b)
  const previewRgb = simulatePrintAppearance(rgb.r, rgb.g, rgb.b)

  return withPreviewHex(
    resultFromMathOutput({
      cmyk,
      preview_rgb: previewRgb,
      preview_hex: '',
    }),
  )
}

/** @deprecated Используйте convertColorMath */
export function convertColorSimple(hex: string): ColorConvertResult {
  return convertColorMath(hex)
}

/** Конвертация цвета: сначала ICC (Flask), иначе формула из модуля. */
export async function convertColor(
  hex: string,
  profile: 'coated' | 'uncoated' = 'coated',
): Promise<ColorConvertResult> {
  const rgb = hexToRgb(hex)

  try {
    const response = await fetch(`${GRAPHICS_MODULE_API}/convert-color-icc`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        r: rgb.r,
        g: rgb.g,
        b: rgb.b,
        profile,
      }),
    })
    const data = await response.json()
    if (!data.error && data.output) {
      return resultFromIccOutput(data.output)
    }
  } catch {
    /* Flask недоступен — простая формула */
  }

  return convertColorMath(hex)
}

export async function checkGraphicsModuleHealth(): Promise<boolean> {
  const bases = [GRAPHICS_MODULE_ICC_PROXY, GRAPHICS_MODULE_API]
  for (const base of bases) {
    try {
      const res = await fetch(`${base}/health`)
      if (!res.ok) continue
      const data = (await res.json()) as { littlecms_supported?: boolean }
      return Boolean(data.littlecms_supported)
    } catch {
      /* try next base */
    }
  }
  return false
}
