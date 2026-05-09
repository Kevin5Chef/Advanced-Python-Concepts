"""
Modern UI Dock Sandbox (Pygame)
- Gradient background
- Glassmorphism blur layer
- Draggable, physics icons
- Real sliders affecting visuals (transparency, blur, glow, icon scale, motion)
- Constructor validation for DockConfig
Requirements: pip install pygame
"""

import pygame
import sys
import math
from pygame import gfxdraw
from pygame import freetype
import colorsys
import time

# ---------------------------
# Configuration / Constants
# ---------------------------
SCREEN_W, SCREEN_H = 1280, 800
FPS = 60

# ---------------------------
# Helper Utilities
# ---------------------------
def clamp(v, a, b):
    return max(a, min(b, v))

def lerp(a, b, t):
    return a + (b - a) * t

def hex_to_rgb(hexstr):
    hexstr = hexstr.lstrip("#")
    return tuple(int(hexstr[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

# ---------------------------
# DockConfig: Constructor Validation
# ---------------------------
class DockConfig:
    def __init__(self,
                 transparency=220,     # 0-255
                 blur_strength=0.12,   # 0.0 - 1.0 (fraction of size)
                 glow_intensity=0.35,  # 0.0 - 1.0
                 icon_scale=1.0,       # 0.5 - 2.0
                 motion_fluidity=0.92, # 0.5 - 0.995 (friction)
                 shadow_depth=8,       # 0 - 40
                 theme_start="#1e293b",
                 theme_end="#0f172a",
                 dock_height=120):
        # Validate ranges
        if not (0 <= transparency <= 255):
            raise ValueError("transparency must be 0..255")
        if not (0.0 <= blur_strength <= 1.0):
            raise ValueError("blur_strength must be 0.0..1.0")
        if not (0.0 <= glow_intensity <= 2.0):
            raise ValueError("glow_intensity must be 0.0..2.0")
        if not (0.5 <= icon_scale <= 2.0):
            raise ValueError("icon_scale must be 0.5..2.0")
        if not (0.5 <= motion_fluidity < 1.0):
            raise ValueError("motion_fluidity must be between 0.5 and 0.995")
        if not (0 <= shadow_depth <= 64):
            raise ValueError("shadow_depth must be 0..64")
        if not isinstance(theme_start, str) or not isinstance(theme_end, str):
            raise ValueError("theme colors must be hex string")

        # Assign
        self.transparency = transparency
        self.blur_strength = blur_strength
        self.glow_intensity = glow_intensity
        self.icon_scale = icon_scale
        self.motion_fluidity = motion_fluidity
        self.shadow_depth = shadow_depth
        self.theme_start = theme_start
        self.theme_end = theme_end
        self.dock_height = dock_height

# ---------------------------
# Visual Utility Functions
# ---------------------------
def create_vertical_gradient_surface(size, color_start, color_end):
    """Create a vertical gradient surface from color_start to color_end."""
    w, h = size
    surf = pygame.Surface((w, h)).convert_alpha()
    rgb_start = hex_to_rgb(color_start)
    rgb_end = hex_to_rgb(color_end)
    for y in range(h):
        t = y / (h - 1) if h > 1 else 0
        r = int(lerp(rgb_start[0], rgb_end[0], t))
        g = int(lerp(rgb_start[1], rgb_end[1], t))
        b = int(lerp(rgb_start[2], rgb_end[2], t))
        pygame.draw.line(surf, (r, g, b), (0, y), (w, y))
    return surf

def fast_blur(surf, amt):
    """
    Fast approximate blur by downscaling/upscaling.
    amt: blur factor: 0.0 (no blur) to ~1.0 (strong)
    Technique recommended for Pygame (downscale -> smoothscale -> upscale).
    """
    if amt <= 0:
        return surf.copy()
    scale = clamp(1.0 - amt, 0.1, 1.0)  # smaller -> blur more
    w, h = surf.get_size()
    sw, sh = max(1, int(w * scale)), max(1, int(h * scale))
    # downscale and upscale using smoothscale for better quality
    small = pygame.transform.smoothscale(surf, (sw, sh))
    blurred = pygame.transform.smoothscale(small, (w, h))
    return blurred

def create_shadow(surface, offset=(6,6), shadow_color=(0,0,0,120), blur=6):
    """Create a shadow surface for a given surface."""
    w, h = surface.get_size()
    shadow = pygame.Surface((w + blur*2, h + blur*2), pygame.SRCALPHA)
    # Place a filled rect approx of the surface's mask
    mask = surface.copy()
    mask.fill((0,0,0))
    # draw basic black rect then blur
    base = pygame.Surface((w, h), pygame.SRCALPHA)
    base.fill(shadow_color)
    shadow.blit(base, (blur, blur))
    shadow = fast_blur(shadow, min(0.9, blur/30.0))
    return shadow

# ---------------------------
# UI Components: Slider, Button
# ---------------------------
class Slider:
    def __init__(self, rect, minv, maxv, val, label, step=0.01):
        self.rect = pygame.Rect(rect)
        self.minv = minv
        self.maxv = maxv
        self.val = clamp(val, minv, maxv)
        self.label = label
        self.dragging = False
        self.step = step

    def draw(self, surf, font):
        # track
        track_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.h//2 - 4, self.rect.w, 8)
        pygame.draw.rect(surf, (50,50,50), track_rect, border_radius=4)
        # knob position
        t = (self.val - self.minv) / (self.maxv - self.minv)
        kx = int(self.rect.x + t * self.rect.w)
        ky = self.rect.y + self.rect.h//2
        pygame.draw.circle(surf, (230,230,230), (kx, ky), 10)
        # label
        lbl = font.render(f"{self.label}: {self.val:.3f}" if isinstance(self.val, float) else f"{self.label}: {self.val}", True, (230,230,230))
        surf.blit(lbl, (self.rect.x, self.rect.y - 22))

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                self.dragging = True
                self.set_val_from_pos(ev.pos[0])
                return True
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            if self.dragging:
                self.dragging = False
                return True
        elif ev.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.set_val_from_pos(ev.pos[0])
                return True
        return False

    def set_val_from_pos(self, x):
        pct = (x - self.rect.x) / self.rect.w
        pct = clamp(pct, 0.0, 1.0)
        raw = self.minv + pct * (self.maxv - self.minv)
        # snap to step
        if isinstance(self.step, float):
            steps = round((raw - self.minv) / self.step)
            raw = self.minv + steps * self.step
        self.val = clamp(raw, self.minv, self.maxv)

# ---------------------------
# Icon (Draggable + Physics)
# ---------------------------
class Icon:
    FONT = None
    def __init__(self, name, size=72, color=(240,240,240), bg=(50,50,60)):
        self.name = name
        self.base_size = size
        self.color = color
        self.bg = bg
        self.scale = 1.0
        self.surface = None
        self.rect = None
        self.pos = pygame.Vector2(0,0)
        self.vel = pygame.Vector2(0,0)
        self.dragging = False
        self.offset = pygame.Vector2(0,0)
        self.create_surface()

    def create_surface(self):
        size = int(self.base_size * self.scale)
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        # rounded rect background
        r = size//8
        bg = self.bg
        pygame.draw.rect(surf, bg, (0,0,size,size), border_radius=r)
        # render short name
        if Icon.FONT is None:
            Icon.FONT = pygame.freetype.SysFont("Arial", max(14, size//6))
        text_surf, _ = Icon.FONT.render(self.name.split()[0], fgcolor=self.color)
        tw, th = text_surf.get_size()
        surf.blit(text_surf, ((size - tw)//2, (size - th)//2))
        self.surface = surf
        self.rect = surf.get_rect()
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, screen, glow=0.0, shadow_depth=8):
        # draw shadow
        if shadow_depth > 0:
            shadow = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
            shadow.fill((0,0,0,180))
            sh = fast_blur(shadow, min(0.9, shadow_depth/30.0))
            screen.blit(sh, (self.pos.x + shadow_depth/2, self.pos.y + shadow_depth/2))
        # glow (simple radial)
        if glow > 0:
            gsurf = pygame.Surface((self.surface.get_width()*2, self.surface.get_height()*2), pygame.SRCALPHA)
            cx = gsurf.get_width()//2
            cy = gsurf.get_height()//2
            maxrad = int(max(cx,cy) * glow * 1.5)
            for r in range(maxrad, 0, -8):
                alpha = int(20 * (1 - r/maxrad))
                pygame.gfxdraw.filled_circle(gsurf, cx, cy, r, (255,255,255,alpha))
            screen.blit(gsurf, (self.pos.x - self.surface.get_width()//2, self.pos.y - self.surface.get_height()//2), special_flags=pygame.BLEND_ADD)
        # blit icon
        screen.blit(self.surface, (self.pos.x, self.pos.y))

    def update(self, dt, friction):
        if not self.dragging:
            self.pos += self.vel * dt
            self.vel *= friction
            # floor / bounds
            if self.pos.x < 0:
                self.pos.x = 0
                self.vel.x *= -0.3
            if self.pos.y < 0:
                self.pos.y = 0
                self.vel.y *= -0.3
            if self.pos.x + self.surface.get_width() > SCREEN_W:
                self.pos.x = SCREEN_W - self.surface.get_width()
                self.vel.x *= -0.3
            if self.pos.y + self.surface.get_height() > SCREEN_H:
                self.pos.y = SCREEN_H - self.surface.get_height()
                self.vel.y *= -0.3
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def start_drag(self, mouse_pos):
        self.dragging = True
        self.offset.x = mouse_pos[0] - self.pos.x
        self.offset.y = mouse_pos[1] - self.pos.y
        self.vel = pygame.Vector2(0,0)

    def drag(self, mouse_pos):
        self.pos.x = mouse_pos[0] - self.offset.x
        self.pos.y = mouse_pos[1] - self.offset.y

    def stop_drag(self):
        self.dragging = False
        # slight inertia on release
        self.vel = pygame.Vector2((0.0, 0.0))

    def set_scale(self, scale):
        if abs(scale - self.scale) > 0.01:
            self.scale = scale
            self.create_surface()

# ---------------------------
# Main Application
# ---------------------------
class UIDockApp:
    def __init__(self):
        pygame.init()
        freetype.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Modern UI Dock Sandbox (Pygame)")
        self.clock = pygame.time.Clock()
        # validated config
        self.config = DockConfig()
        # background gradient
        self.gradient_surface = create_vertical_gradient_surface((SCREEN_W, SCREEN_H), self.config.theme_start, self.config.theme_end)
        self.gradient_dirty = False
        # build UI elements
        self.font = pygame.freetype.SysFont("Arial", 16)
        self.large_font = pygame.freetype.SysFont("Arial", 20)
        self.build_icons()
        self.build_sliders()
        self.dragging_icon = None
        self.last_time = time.time()
        self.running = True
        # caching surfaces
        self.composed_background = None
        self.composed_background_needs_update = True

    def build_icons(self):
        names = ["IceCube", "Plasma", "GlassNotes", "NeonMail", "Quantum", "VisionCam", "NanoStore", "FluidMusic"]
        self.icons = []
        start_x = 120
        y = SCREEN_H - 160
        for i, n in enumerate(names):
            ic = Icon(n, size=80, bg=(50,60,70))
            ic.pos = pygame.Vector2(start_x + i * 110, y)
            ic.create_surface()
            self.icons.append(ic)

    def build_sliders(self):
        # sliders: rect, min, max, val, label
        self.sliders = []
        x = 20
        y = 20
        w = 200
        h = 40
        gap = 70
        s1 = Slider((x, y, w, 30), 50, 255, self.config.transparency, "Transparency", step=1)
        s2 = Slider((x, y+gap, w, 30), 0.0, 0.6, self.config.blur_strength, "Blur", step=0.01)
        s3 = Slider((x, y+gap*2, w, 30), 0.0, 1.5, self.config.glow_intensity, "Glow", step=0.01)
        s4 = Slider((x, y+gap*3, w, 30), 0.5, 2.0, self.config.icon_scale, "IconScale", step=0.01)
        s5 = Slider((x, y+gap*4, w, 30), 0.85, 0.995, self.config.motion_fluidity, "Fluidity", step=0.0005)
        s6 = Slider((x, y+gap*5, w, 30), 0, 40, self.config.shadow_depth, "Shadow", step=1)
        self.sliders = [s1, s2, s3, s4, s5, s6]
        # color pick rectangles
        self.color_start_rect = pygame.Rect(250, 20, 40, 40)
        self.color_end_rect = pygame.Rect(300, 20, 40, 40)

    def update_config_from_sliders(self):
        # map slider values to config
        self.config.transparency = int(self.sliders[0].val)
        self.config.blur_strength = float(self.sliders[1].val)
        self.config.glow_intensity = float(self.sliders[2].val)
        self.config.icon_scale = float(self.sliders[3].val)
        self.config.motion_fluidity = float(self.sliders[4].val)
        self.config.shadow_depth = int(self.sliders[5].val)
        # update icons
        for ic in self.icons:
            ic.set_scale(self.config.icon_scale)
        # mark gradient or background changes if needed
        self.composed_background_needs_update = True

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            # sliders events
            for s in self.sliders:
                if s.handle_event(ev):
                    self.update_config_from_sliders()
            # mouse interactions for icons
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                pos = ev.pos
                # check color pick
                if self.color_start_rect.collidepoint(pos):
                    self.pick_color(is_start=True)
                elif self.color_end_rect.collidepoint(pos):
                    self.pick_color(is_start=False)
                else:
                    for ic in reversed(self.icons):
                        if ic.rect.collidepoint(pos):
                            self.dragging_icon = ic
                            # bring to front
                            self.icons.remove(ic)
                            self.icons.append(ic)
                            ic.start_drag(pos)
                            break
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if self.dragging_icon:
                    self.dragging_icon.stop_drag()
                    self.dragging_icon = None
            elif ev.type == pygame.MOUSEMOTION:
                if self.dragging_icon:
                    self.dragging_icon.drag(ev.pos)

    def pick_color(self, is_start=True):
        # simple color picker using HSL keyboard interactions (since Pygame has no native color dialog)
        # We'll implement a basic modal to pick hue with keys
        picking = True
        hue = 0.5
        sat = 0.6
        val = 0.3
        while picking:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    picking = False
                    self.running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN:
                        picking = False
                    elif ev.key == pygame.K_ESCAPE:
                        picking = False
                    elif ev.key == pygame.K_LEFT:
                        hue = (hue - 0.02) % 1.0
                    elif ev.key == pygame.K_RIGHT:
                        hue = (hue + 0.02) % 1.0
                    elif ev.key == pygame.K_UP:
                        val = clamp(val + 0.05, 0.0, 1.0)
                    elif ev.key == pygame.K_DOWN:
                        val = clamp(val - 0.05, 0.0, 1.0)
                    elif ev.key == pygame.K_s:
                        sat = clamp(sat - 0.05, 0.0, 1.0)
                    elif ev.key == pygame.K_w:
                        sat = clamp(sat + 0.05, 0.0, 1.0)
            # draw a small overlay showing current color
            col = colorsys.hsv_to_rgb(hue, sat, val)
            rgb = tuple(int(c * 255) for c in col)
            overlay = pygame.Surface((320,120), pygame.SRCALPHA)
            overlay.fill((*rgb, 200))
            self.screen.blit(overlay, (480, 320))
            hint = self.font.render("Color picker: Left/Right hue, Up/Down value, W/S sat, Enter accept, Esc cancel", (255,255,255))
            self.screen.blit(hint[0], (480, 450))
            pygame.display.flip()
            self.clock.tick(30)
        hexcol = rgb_to_hex(rgb)
        if is_start:
            self.config.theme_start = hexcol
        else:
            self.config.theme_end = hexcol
        self.gradient_surface = create_vertical_gradient_surface((SCREEN_W, SCREEN_H), self.config.theme_start, self.config.theme_end)
        self.composed_background_needs_update = True

    def compose_background(self):
        """Compose gradient and cached effects (run only when dirty)."""
        base = self.gradient_surface.copy()
        # create a subtle vignette
        vignette = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for y in range(SCREEN_H):
            alpha = int(lerp(0, 120, abs((y - SCREEN_H/2) / (SCREEN_H/2))))
            pygame.draw.line(vignette, (0,0,0,alpha), (0,y), (SCREEN_W,y))
        base.blit(vignette, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
        self.composed_background = base
        self.composed_background_needs_update = False

    def render_glass_layer(self):
        """Create glass layer rectangle near bottom (dock area) and apply blur."""
        dh = self.config.dock_height
        dock_rect = pygame.Rect(60, SCREEN_H - dh - 40, SCREEN_W - 120, dh + 20)
        # capture background portion
        bg_slice = self.composed_background.subsurface(dock_rect).copy()
        # blur by amount (0..1)
        blurred = fast_blur(bg_slice, self.config.blur_strength)
        # tint it slightly
        tint = pygame.Surface(blurred.get_size(), pygame.SRCALPHA)
        tint.fill((255,255,255, int(40)))  # subtle light
        blurred.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        # make rounded rect mask
        mask = pygame.Surface(blurred.get_size(), pygame.SRCALPHA)
        r = 18
        pygame.draw.rect(mask, (255,255,255,255), mask.get_rect(), border_radius=r)
        # compose final glass surface
        glass = pygame.Surface(blurred.get_size(), pygame.SRCALPHA)
        glass.blit(blurred, (0,0))
        glass.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        # apply transparency from config
        glass.set_alpha(self.config.transparency)
        return glass, dock_rect

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # seconds
            self.handle_events()
            # update slider values mapped to config
            self.update_config_from_sliders()
            # update icons physics
            for ic in self.icons:
                ic.update(dt, self.config.motion_fluidity)
            # background compose if needed
            if self.composed_background_needs_update or self.gradient_dirty:
                self.compose_background()
            # draw main
            self.screen.fill((0,0,0))
            # draw gradient background (cached)
            self.screen.blit(self.composed_background, (0,0))
            # render glass layer
            glass_surf, dock_rect = self.render_glass_layer()
            # render dock shadow (slightly larger)
            shadow = fast_blur(glass_surf, 0.6)
            shadow_surf = pygame.Surface((shadow.get_width()+10, shadow.get_height()+10), pygame.SRCALPHA)
            shadow_surf.blit(shadow, (5,5))
            # place shadow and glass
            self.screen.blit(shadow_surf, (dock_rect.x -5, dock_rect.y -5))
            self.screen.blit(glass_surf, dock_rect.topleft)
            # draw icons (icons draw relative to positions; ensure icons can be above glass)
            for ic in self.icons:
                # compute glow and shadow based on config
                ic.draw(self.screen, glow=self.config.glow_intensity, shadow_depth=self.config.shadow_depth)
            # UI overlays: sliders and color boxes
            for s in self.sliders:
                s.draw(self.screen, self.font)
            # draw color rectangles
            pygame.draw.rect(self.screen, hex_to_rgb(self.config.theme_start), self.color_start_rect)
            pygame.draw.rect(self.screen, hex_to_rgb(self.config.theme_end), self.color_end_rect)
            # help text
            help_txt = "Click and drag icons. Use sliders to adjust effects. Click color boxes to pick colors."
            self.font.render_to(self.screen, (20, SCREEN_H - 30), help_txt, fgcolor=(220,220,220))
            # fps display
            fps_text = f"FPS: {int(self.clock.get_fps())}"
            self.font.render_to(self.screen, (SCREEN_W - 120, 10), fps_text, fgcolor=(200,200,200))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    app = UIDockApp()
    app.run()
