"""Renderiza o vídeo vertical (1080x1920) a partir das fotos do anúncio, sem texto na tela.

Uso: python -I render.py <timeline.json> <pasta_fotos> <saida_sem_audio.mp4> [--preview]
Modos de cena (timeline.json):
  branco: foto de fundo branco ocupando a tela, com zoom/pan
  cheio : recorte vertical da foto preenchendo a tela
  card  : recorte (sem o texto embutido) em cartão arredondado sobre fundo desfocado
Entradas: punch (corte seco com leve zoom), whip (deslize lateral com desfoque), flash (clarão branco).
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
import torch
import torch.nn.functional as F

torch.set_grad_enabled(False)
torch.set_num_threads(max(1, os.cpu_count() - 2))

WHIP = 0.12  # meia duração do deslize (s)
PUNCH = 0.2


def ease(name, p):
    p = min(max(p, 0.0), 1.0)
    if name == "outcubic":
        return 1 - (1 - p) ** 3
    if name == "linear":
        return p
    return -(math.cos(math.pi * p) - 1) / 2  # inoutsine


def inoutcubic(p):
    p = min(max(p, 0.0), 1.0)
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def load_image(path):
    info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                           "-of", "csv=p=0", path], capture_output=True, text=True, check=True).stdout.strip()
    w, h = map(int, info.split(",")[:2])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(h, w, 3)
    return torch.from_numpy(a.copy()).permute(2, 0, 1).float().div(255)[None]  # [1,3,H,W]


def make_src(img, white):
    """RGBA pré-multiplicado. No modo branco: clareia o fundo quase-branco e suaviza as bordas."""
    _, _, H, W = img.shape
    rgb = img.clone()
    if white:
        rgb = (rgb / 0.965).clamp(0, 1)
    feather = 10.0 if white else 1.0
    yy = torch.arange(H).float()[:, None] + 0.5
    xx = torch.arange(W).float()[None, :] + 0.5
    d = torch.minimum(torch.minimum(xx, W - xx), torch.minimum(yy, H - yy))
    a = (d / feather).clamp(0, 1)[None, None]
    return torch.cat([rgb * a, a], 1)


def sample(src, rect, dw, dh, mode="bicubic"):
    x, y, w, h = rect
    _, _, H, W = src.shape
    gx = (x + (torch.arange(dw).float() + 0.5) / dw * w) / W * 2 - 1
    gy = (y + (torch.arange(dh).float() + 0.5) / dh * h) / H * 2 - 1
    GY, GX = torch.meshgrid(gy, gx, indexing="ij")
    grid = torch.stack([GX, GY], -1)[None]
    return F.grid_sample(src, grid, mode=mode, padding_mode="zeros", align_corners=False).clamp(0, 1)


def gauss_kernel(sigma, r):
    x = torch.arange(-r, r + 1).float()
    k = torch.exp(-x ** 2 / (2 * sigma ** 2))
    return k / k.sum()


def blur(img, sigma):
    r = max(1, int(sigma * 3))
    k = gauss_kernel(sigma, r)
    c = img.shape[1]
    img = F.conv2d(F.pad(img, (r, r, 0, 0), mode="replicate"), k.view(1, 1, 1, -1).repeat(c, 1, 1, 1), groups=c)
    img = F.conv2d(F.pad(img, (0, 0, r, r), mode="replicate"), k.view(1, 1, -1, 1).repeat(c, 1, 1, 1), groups=c)
    return img


def rounded_mask(w, h, r):
    yy = torch.arange(h).float()[:, None] + 0.5
    xx = torch.arange(w).float()[None, :] + 0.5
    dx = torch.clamp(torch.maximum(r - xx, xx - (w - r)), min=0)
    dy = torch.clamp(torch.maximum(r - yy, yy - (h - r)), min=0)
    dist = torch.sqrt(dx ** 2 + dy ** 2)
    return (r - dist + 0.5).clamp(0, 1)[None, None]


def rect_at(spec, aspect):
    cx, cy = spec["c"]
    w = spec["w"]
    h = w / aspect
    return [cx - w / 2, cy - h / 2, w, h]


class Shot:
    def __init__(self, c, end, fotos, W, H, cache):
        self.c, self.ini, self.end = c, c["ini"], end
        self.mode = c["modo"]
        self.W, self.H = W, H
        key = (c["foto"], self.mode == "branco")
        if key not in cache:
            cache[key] = make_src(load_image(os.path.join(fotos, c["foto"])), self.mode == "branco")
        self.src = cache[key]
        if self.mode == "card":
            self.cw, self.ch = c["card"]
            self.cx, self.cy = (W - self.cw) // 2, (H - self.ch) // 2
            self.aspect = self.cw / self.ch
            self.mask = rounded_mask(self.cw, self.ch, 44)
            sh = torch.zeros(1, 1, H, W)
            sh[..., self.cy + 22:self.cy + 22 + self.ch, self.cx:self.cx + self.cw] = 1
            self.shadow = blur(F.interpolate(sh, scale_factor=0.25, mode="area"), 6)
            self.shadow = F.interpolate(self.shadow, size=(H, W), mode="bilinear", align_corners=False) * 0.55
            self.small = F.interpolate(self.src, scale_factor=0.25, mode="area")
        else:
            self.aspect = W / H

    def rect(self, t):
        p = (t - self.ini) / (self.end - self.ini)
        e = ease(self.c.get("ease", "inoutsine"), p)
        r0, r1 = rect_at(self.c["r0"], self.aspect), rect_at(self.c["r1"], self.aspect)
        return [a + (b - a) * e for a, b in zip(r0, r1)]

    def frame(self, t):
        W, H = self.W, self.H
        r = self.rect(t)
        if self.mode == "branco":
            s = sample(self.src, r, W, H)
            out = s[:, :3] + (1 - s[:, 3:4])
        elif self.mode == "cheio":
            s = sample(self.src, r, W, H)
            out = s[:, :3] / s[:, 3:4].clamp(min=1e-4)
        else:
            # fundo: mesmo recorte, ampliado para cobrir a tela, bem desfocado e escurecido
            x, y, w, h = r
            bh = h
            bw = bh * W / H
            br = [x + w / 2 - bw / 2 * 1.15, y + h / 2 - bh / 2 * 1.15, bw * 1.15, bh * 1.15]
            br_small = [v * 0.25 for v in br]
            bg = sample(self.small, br_small, 54, 96, mode="bilinear")
            bg = bg[:, :3] / bg[:, 3:4].clamp(min=1e-4)
            bg = blur(bg, 2.5)
            bg = F.interpolate(bg, size=(H, W), mode="bicubic", align_corners=False).clamp(0, 1)
            lum = bg.mean(1, keepdim=True)
            bg = (lum + (bg - lum) * 0.8) * 0.5
            bg = bg * (1 - self.shadow)
            fg = sample(self.src, r, self.cw, self.ch)
            fg = fg[:, :3] / fg[:, 3:4].clamp(min=1e-4)
            m = self.mask
            region = bg[..., self.cy:self.cy + self.ch, self.cx:self.cx + self.cw]
            bg[..., self.cy:self.cy + self.ch, self.cx:self.cx + self.cw] = region * (1 - m) + fg * m
            out = bg
        tl = t - self.ini
        ent = self.c["entrada"]
        if ent in ("punch", "flash") and 0 <= tl < PUNCH:
            z = 1 + 0.08 * (1 - ease("outcubic", tl / PUNCH))
            out = zoom(out, z)
        if ent == "flash" and 0 <= tl < 0.2:
            a = 0.9 * (1 - tl / 0.2) ** 2
            out = out * (1 - a) + a
        return out


def zoom(img, z):
    _, _, H, W = img.shape
    return sample(img, [W / 2 - W / z / 2, H / 2 - H / z / 2, W / z, H / z], W, H, mode="bilinear")


def shift(img, dx):
    out = torch.zeros_like(img)
    W = img.shape[-1]
    if dx >= W or dx <= -W:
        return out
    if dx >= 0:
        out[..., dx:] = img[..., :W - dx]
    else:
        out[..., :W + dx] = img[..., -dx:]
    return out


def hblur(img, k):
    """Média móvel horizontal de largura k (ímpar)."""
    if k <= 1:
        return img
    r = k // 2
    p = F.pad(img, (r + 1, r, 0, 0), mode="replicate")
    c = p.cumsum(-1)
    return (c[..., k:] - c[..., :-k]) / k


def sharpen(img, amount=0.45):
    return (img + amount * (img - blur(img, 1.0))).clamp(0, 1)


def main(tl_path, fotos, out_path, preview=False):
    with open(tl_path, encoding="utf-8") as f:
        tl = json.load(f)
    fps, W, H, dur = tl["fps"], tl["w"], tl["h"], tl["dur"]
    cache = {}
    cenas = tl["cenas"]
    shots = [Shot(c, cenas[i + 1]["ini"] if i + 1 < len(cenas) else dur, fotos, W, H, cache) for i, c in enumerate(cenas)]
    n_frames = int(round(dur * fps))

    def at(t):
        for i, s in enumerate(shots):
            nxt = shots[i + 1] if i + 1 < len(shots) else None
            if nxt and nxt.c["entrada"] == "whip" and abs(t - nxt.ini) < WHIP:
                q0 = (t - (nxt.ini - WHIP)) / (2 * WHIP)
                a, b = s.frame(t), nxt.frame(t)
                q = inoutcubic(q0)
                comp = shift(a, -int(round(q * W))) + shift(b, int(round((1 - q) * W)))
                # desfoque de movimento: borrão horizontal do tamanho de meio quadro de deslocamento
                dq = (inoutcubic(q0 + 0.01) - inoutcubic(q0 - 0.01)) / 0.02
                px = dq * W / (2 * WHIP) / fps * 0.5
                return hblur(comp, int(px) | 1)
            if s.ini <= t < s.end:
                return s.frame(t)
        return shots[-1].frame(t)

    if preview:
        # folha de contato: um quadro do meio de cada cena + quadros de transição
        os.makedirs(out_path, exist_ok=True)
        for s in shots:
            for tag, t in (("meio", (s.ini + s.end) / 2), ("inicio", s.ini + 0.02)):
                fr = sharpen(at(t))
                arr = (fr[0].permute(1, 2, 0).numpy() * 255 + 0.5).astype(np.uint8)
                p = os.path.join(out_path, f'{s.c["id"]}_{tag}.png')
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                "-i", "-", "-vf", "scale=360:-1", p], input=arr.tobytes(), check=True)
        print("preview ok")
        return

    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
           "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n_frames):
        fr = sharpen(at(k / fps))
        arr = (fr[0].permute(1, 2, 0).numpy() * 255 + 0.5).astype(np.uint8)
        proc.stdin.write(arr.tobytes())
        if k % 60 == 0:
            print(f"quadro {k}/{n_frames}", flush=True)
    proc.stdin.close()
    proc.wait()
    print("ok:", out_path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], "--preview" in sys.argv)
