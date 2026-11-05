"""deckkit: opinionated python-pptx helpers that encode slide design rules.

Every layout here already follows the rules in ../SKILL.md: one dominant colour,
0.5" margins, 36pt+ titles, 14-18pt body, left-aligned body text, a visual on
every content slide, no accent bars/stripes, text sized to fit its box.

Usage (see ../SKILL.md for the full workflow):

    from deckkit import Deck, PALETTES
    d = Deck(palette=PALETTES["forest"], title_font="Georgia", body_font="Calibri")
    d.title_slide("Quarterly review", "What changed and what we do next", "Harry · Nov 2026")
    d.section_slide("Where we are")
    d.bullets_with_visual("Three things moved", ["Revenue up 12%", "Churn flat", "Hiring paused"],
                          image="chart.png")
    d.cards("Options", [("Build", "6 weeks, full control"), ("Buy", "2 weeks, licence cost"),
                        ("Wait", "No cost, no progress")])
    d.stats("By the numbers", [("12%", "revenue growth"), ("0.8%", "monthly churn"), ("41", "open roles")])
    d.table("Comparison", ["", "A", "B"], [["Cost", "Low", "High"], ["Speed", "Fast", "Slow"]])
    d.bar_chart("Pipeline by stage", ["Lead", "Qualified", "Won"], {"2025": [40, 25, 10], "2026": [55, 30, 14]})
    d.closing_slide("Decision needed", "Approve the pilot and name an owner by Friday")
    d.save("review.pptx")

Then: python check_pptx.py review.pptx && bash render.sh review.pptx
"""
from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

sys.path.insert(0, str(Path(__file__).parent))
from check_pptx import wrapped_lines  # noqa: E402  (shared text-fit estimate)

# palette = dark (titles, title-slide bg), accent (one sharp colour), light (card tint), text
PALETTES = {
    "navy":      dict(dark="1E2761", accent="F96167", light="EEF2FA", text="1A1A1A"),
    "forest":    dict(dark="2C5F2D", accent="D98E04", light="EEF4EA", text="1A1A1A"),
    "charcoal":  dict(dark="36454F", accent="E4572E", light="F2F2F2", text="212121"),
    "berry":     dict(dark="6D2E46", accent="E6A157", light="F6EEF1", text="1A1A1A"),
    "ocean":     dict(dark="065A82", accent="21C8A8", light="EAF3F8", text="1A1A1A"),
    "terracotta": dict(dark="7A3B2E", accent="2A9D8F", light="F7EFEA", text="1A1A1A"),
}

W, H = Inches(13.333), Inches(7.5)  # 16:9
MARGIN = Inches(0.6)
TITLE_TOP = Inches(0.45)
TITLE_H = Inches(1.0)
BODY_TOP = Inches(1.65)
BODY_H = H - BODY_TOP - MARGIN
GAP = Inches(0.35)


def rgb(hexstr: str) -> RGBColor:
    return RGBColor.from_string(hexstr)


class Deck:
    def __init__(self, palette=None, title_font="Calibri", body_font="Calibri"):
        self.p = palette or PALETTES["navy"]
        self.title_font = title_font
        self.body_font = body_font
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        self.blank = self.prs.slide_layouts[6]
        self.n = 0

    # ---------- primitives ----------
    def _slide(self, bg=None):
        s = self.prs.slides.add_slide(self.blank)
        if bg:
            fill = s.background.fill
            fill.solid()
            fill.fore_color.rgb = rgb(bg)
        self.n += 1
        return s

    def _text(self, slide, left, top, width, height, text, size=16, bold=False, color=None,
              font=None, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, fit=True, min_size=11):
        """Add a text box whose font shrinks (down to min_size) until the text fits the box."""
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = Inches(0.08)
        tf.margin_top = tf.margin_bottom = Inches(0.05)
        paras = text if isinstance(text, list) else [text]
        if fit:
            size = self._fit_size(paras, size, min_size, width, height, font or self.body_font, bold)
        for i, line in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = align
            run = para.add_run()
            run.text = line
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.name = font or self.body_font
            run.font.color.rgb = rgb(color or self.p["text"])
            if len(paras) > 1:
                para.space_after = Pt(size * 0.5)
        return box

    def _fit_size(self, paras, size, min_size, width, height, family=None, bold=False):
        width_pt = (width - Inches(0.16)) / 12700
        height_pt = (height - Inches(0.1)) / 12700
        while size > min_size:
            total = sum(wrapped_lines(t, size, width_pt, family, bold) * size * 1.2 + (size * 0.5 if len(paras) > 1 else 0)
                        for t in paras)
            if total <= height_pt:
                break
            size -= 1
        return size

    def _bullets(self, slide, left, top, width, height, items, size=18, color=None):
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.08)
        size = self._fit_size(items, size, 12, width - Inches(0.3), height, self.body_font)
        for i, item in enumerate(items):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = PP_ALIGN.LEFT
            para.space_after = Pt(size * 0.6)
            # real bullet via XML, never a literal "•"
            pPr = para._p.get_or_add_pPr()
            pPr.set("marL", str(int(Inches(0.3))))
            pPr.set("indent", str(-int(Inches(0.3))))
            bu = pPr.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}buChar", {"char": "•"})
            pPr.append(bu)
            run = para.add_run()
            run.text = item
            run.font.size = Pt(size)
            run.font.name = self.body_font
            run.font.color.rgb = rgb(color or self.p["text"])
        return box

    def _title(self, slide, text, color=None):
        return self._text(slide, MARGIN, TITLE_TOP, W - 2 * MARGIN, TITLE_H, text, size=38, bold=True,
                          color=color or self.p["dark"], font=self.title_font, anchor=MSO_ANCHOR.MIDDLE, min_size=24)

    def _rect(self, slide, left, top, width, height, fill, shape=MSO_SHAPE.RECTANGLE, line=False):
        r = slide.shapes.add_shape(shape, left, top, width, height)
        r.fill.solid()
        r.fill.fore_color.rgb = rgb(fill)
        if not line:
            r.line.fill.background()
        r.shadow.inherit = False
        if r.has_text_frame:
            r.text_frame.text = ""
        return r

    def _picture(self, slide, path, left, top, max_w, max_h):
        from PIL import Image
        with Image.open(path) as im:
            iw, ih = im.size
        scale = min(max_w / iw, max_h / ih)
        w, h = int(iw * scale), int(ih * scale)
        return slide.shapes.add_picture(str(path), left + (max_w - w) // 2, top + (max_h - h) // 2, w, h)

    def notes(self, slide, text):
        slide.notes_slide.notes_text_frame.text = text

    # ---------- layouts ----------
    def title_slide(self, title, subtitle="", byline="", notes=None):
        s = self._slide(bg=self.p["dark"])
        self._text(s, MARGIN, Inches(2.2), W - 2 * MARGIN, Inches(1.8), title, size=48, bold=True,
                   color="FFFFFF", font=self.title_font, anchor=MSO_ANCHOR.BOTTOM, min_size=32)
        if subtitle:
            self._text(s, MARGIN, Inches(4.1), W - 2 * MARGIN, Inches(1.0), subtitle, size=22, color="DDE3EA")
        if byline:
            self._text(s, MARGIN, H - Inches(1.1), W - 2 * MARGIN, Inches(0.5), byline, size=14, color="B8C2CC")
        if notes:
            self.notes(s, notes)
        return s

    def section_slide(self, title, kicker="", notes=None):
        s = self._slide(bg=self.p["dark"])
        if kicker:
            self._text(s, MARGIN, Inches(2.4), W - 2 * MARGIN, Inches(0.6), kicker.upper(), size=14, color=self.p["accent"], bold=True)
        self._text(s, MARGIN, Inches(3.0), W - 2 * MARGIN, Inches(1.6), title, size=44, bold=True,
                   color="FFFFFF", font=self.title_font, min_size=30)
        if notes:
            self.notes(s, notes)
        return s

    def bullets_with_visual(self, title, bullets, image=None, caption="", notes=None, visual_side="right"):
        """Bullets in one column, an image (or an accent panel with a caption) in the other."""
        s = self._slide(bg="FFFFFF")
        self._title(s, title)
        col_w = (W - 2 * MARGIN - GAP) * 0.55
        vis_w = W - 2 * MARGIN - GAP - col_w
        tx = MARGIN if visual_side == "right" else MARGIN + vis_w + GAP
        vx = MARGIN + col_w + GAP if visual_side == "right" else MARGIN
        self._bullets(s, tx, BODY_TOP, col_w, BODY_H, bullets)
        if image:
            self._picture(s, image, vx, BODY_TOP, vis_w, BODY_H)
        else:
            self._rect(s, vx, BODY_TOP, vis_w, BODY_H, self.p["light"], MSO_SHAPE.ROUNDED_RECTANGLE)
            if caption:
                self._text(s, vx + Inches(0.3), BODY_TOP + Inches(0.3), vis_w - Inches(0.6), BODY_H - Inches(0.6),
                           caption, size=20, color=self.p["dark"], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        if notes:
            self.notes(s, notes)
        return s

    def two_column(self, title, left_head, left_items, right_head, right_items, notes=None):
        s = self._slide(bg="FFFFFF")
        self._title(s, title)
        col_w = (W - 2 * MARGIN - GAP) / 2
        text_w_pt = (col_w - Inches(1.1)) / 12700
        need = max(sum(wrapped_lines(it, 18, text_w_pt, self.body_font) * 18 * 1.2 + 18 * 0.6 for it in items)
                   for items in (left_items, right_items))
        panel_h = min(BODY_H, max(Inches(3.0), Inches(1.4) + Emu(int(need * 12700))))
        for i, (head, items) in enumerate(((left_head, left_items), (right_head, right_items))):
            x = MARGIN + i * (col_w + GAP)
            self._rect(s, x, BODY_TOP, col_w, panel_h, self.p["light"], MSO_SHAPE.ROUNDED_RECTANGLE)
            self._text(s, x + Inches(0.3), BODY_TOP + Inches(0.25), col_w - Inches(0.6), Inches(0.6), head,
                       size=22, bold=True, color=self.p["dark"])
            self._bullets(s, x + Inches(0.3), BODY_TOP + Inches(0.95), col_w - Inches(0.6), panel_h - Inches(1.2), items, size=18)
        if notes:
            self.notes(s, notes)
        return s

    def cards(self, title, items, notes=None):
        """items: list of (heading, body) tuples, 2-4 of them. Cards get a tint, a big numeral, no stripes."""
        s = self._slide(bg="FFFFFF")
        self._title(s, title)
        k = len(items)
        card_w = (W - 2 * MARGIN - GAP * (k - 1)) / k
        body_w_pt = (card_w - Inches(0.76)) / 12700
        longest = max(wrapped_lines(b, 16, body_w_pt, self.body_font) for _, b in items)
        card_h = min(BODY_H, max(Inches(3.4), Inches(2.3) + Emu(int(longest * 16 * 1.2 * 12700)) + Inches(0.4)))
        top = BODY_TOP + max(0, (BODY_H - card_h) // 3)  # sit slightly above centre, not glued to the title
        for i, (head, body) in enumerate(items):
            x = MARGIN + i * (card_w + GAP)
            self._rect(s, x, top, card_w, card_h, self.p["light"], MSO_SHAPE.ROUNDED_RECTANGLE)
            circ = self._rect(s, x + Inches(0.3), top + Inches(0.3), Inches(0.7), Inches(0.7), self.p["accent"], MSO_SHAPE.OVAL)
            tf = circ.text_frame
            tf.text = str(i + 1)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            r = tf.paragraphs[0].runs[0]
            r.font.size, r.font.bold, r.font.name = Pt(20), True, self.body_font
            r.font.color.rgb = rgb("FFFFFF")
            self._text(s, x + Inches(0.3), top + Inches(1.2), card_w - Inches(0.6), Inches(0.8), head,
                       size=22, bold=True, color=self.p["dark"], min_size=16)
            self._text(s, x + Inches(0.3), top + Inches(2.0), card_w - Inches(0.6), card_h - Inches(2.3), body, size=16)
        if notes:
            self.notes(s, notes)
        return s

    def stats(self, title, items, notes=None):
        """items: list of (big_number, label). Big numerals carry the slide."""
        s = self._slide(bg="FFFFFF")
        self._title(s, title)
        k = len(items)
        cell_w = (W - 2 * MARGIN) / k
        for i, (num, label) in enumerate(items):
            x = MARGIN + i * cell_w
            self._text(s, x, BODY_TOP + Inches(0.8), cell_w, Inches(1.6), num, size=66, bold=True,
                       color=self.p["accent"], font=self.title_font, align=PP_ALIGN.CENTER, min_size=40)
            self._text(s, x + Inches(0.3), BODY_TOP + Inches(2.5), cell_w - Inches(0.6), Inches(1.4), label,
                       size=18, color=self.p["text"], align=PP_ALIGN.CENTER)
        if notes:
            self.notes(s, notes)
        return s

    def table(self, title, header, rows, notes=None, col_widths=None):
        s = self._slide(bg="FFFFFF")
        self._title(s, title)
        nrows, ncols = len(rows) + 1, len(header)
        row_h = min(Inches(0.85) if nrows <= 5 else Inches(0.65), BODY_H / nrows)
        shape = s.shapes.add_table(nrows, ncols, MARGIN, BODY_TOP, W - 2 * MARGIN, row_h * nrows)
        tbl = shape.table
        if col_widths:
            total = sum(col_widths)
            for i, cw in enumerate(col_widths):
                tbl.columns[i].width = int((W - 2 * MARGIN) * cw / total)
        size = 18 if nrows <= 5 else 16 if nrows <= 8 else 13
        for c, h in enumerate(header):
            self._cell(tbl.cell(0, c), h, size, bold=True, fill=self.p["dark"], color="FFFFFF")
        for r, row in enumerate(rows, start=1):
            for c, val in enumerate(row):
                self._cell(tbl.cell(r, c), str(val), size, bold=(c == 0),
                           fill=self.p["light"] if r % 2 else "FFFFFF", color=self.p["text"])
        if notes:
            self.notes(s, notes)
        return s

    def _cell(self, cell, text, size, bold=False, fill="FFFFFF", color="1A1A1A"):
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(fill)
        cell.margin_left = cell.margin_right = Inches(0.12)
        tf = cell.text_frame
        tf.text = text
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.size, r.font.bold, r.font.name = Pt(size), bold, self.body_font
                r.font.color.rgb = rgb(color)

    def bar_chart(self, title, categories, series: dict, notes=None, kind="bar", takeaway=""):
        """Native chart. kind: bar (clustered column), line, pie. Styled: palette colours, data labels, light grid."""
        s = self._slide(bg="FFFFFF")
        self._title(s, title)
        data = CategoryChartData()
        data.categories = categories
        for name, vals in series.items():
            data.add_series(name, vals)
        ctype = {"bar": XL_CHART_TYPE.COLUMN_CLUSTERED, "line": XL_CHART_TYPE.LINE_MARKERS, "pie": XL_CHART_TYPE.PIE}[kind]
        chart_h = BODY_H - (Inches(0.9) if takeaway else 0)
        gf = s.shapes.add_chart(ctype, MARGIN, BODY_TOP, W - 2 * MARGIN, chart_h, data)
        ch = gf.chart
        ch.has_legend = len(series) > 1
        if ch.has_legend:
            ch.legend.position = XL_LEGEND_POSITION.BOTTOM
            ch.legend.include_in_layout = False
            ch.legend.font.size = Pt(12)
        colours = [self.p["dark"], self.p["accent"], "8A94A6", "C5CBD6"]
        plot = ch.plots[0]
        plot.has_data_labels = True
        plot.data_labels.font.size = Pt(11)
        plot.data_labels.font.color.rgb = rgb(self.p["text"])
        for i, ser in enumerate(plot.series):
            ser.format.fill.solid()
            ser.format.fill.fore_color.rgb = rgb(colours[i % len(colours)])
        if kind != "pie":
            ch.category_axis.tick_labels.font.size = Pt(12)
            ch.value_axis.tick_labels.font.size = Pt(11)
            ch.value_axis.major_gridlines.format.line.color.rgb = rgb("DDDDDD")
            ch.value_axis.format.line.fill.background()
        if takeaway:
            self._text(s, MARGIN, H - MARGIN - Inches(0.8), W - 2 * MARGIN, Inches(0.8), takeaway,
                       size=18, bold=True, color=self.p["dark"], anchor=MSO_ANCHOR.MIDDLE)
        if notes:
            self.notes(s, notes)
        return s

    def timeline(self, title, steps, notes=None):
        """steps: list of (label, description). Numbered circles joined by a line."""
        s = self._slide(bg="FFFFFF")
        self._title(s, title)
        k = len(steps)
        usable = W - 2 * MARGIN
        step_w = usable / k
        y = BODY_TOP + Inches(1.6)
        self._rect(s, MARGIN + step_w / 2, y + Inches(0.33), usable - step_w, Inches(0.06), "C5CBD6")
        for i, (label, desc) in enumerate(steps):
            cx = MARGIN + step_w * i + step_w / 2
            circ = self._rect(s, cx - Inches(0.36), y, Inches(0.72), Inches(0.72), self.p["dark"], MSO_SHAPE.OVAL)
            tf = circ.text_frame
            tf.text = str(i + 1)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            r = tf.paragraphs[0].runs[0]
            r.font.size, r.font.bold, r.font.name = Pt(18), True, self.body_font
            r.font.color.rgb = rgb("FFFFFF")
            self._text(s, cx - step_w / 2 + Inches(0.1), y + Inches(1.0), step_w - Inches(0.2), Inches(0.7), label,
                       size=18, bold=True, color=self.p["dark"], align=PP_ALIGN.CENTER, min_size=13)
            self._text(s, cx - step_w / 2 + Inches(0.1), y + Inches(1.7), step_w - Inches(0.2), BODY_H - Inches(3.0), desc,
                       size=14, align=PP_ALIGN.CENTER, min_size=11)
        if notes:
            self.notes(s, notes)
        return s

    def closing_slide(self, title, ask, notes=None):
        s = self._slide(bg=self.p["dark"])
        self._text(s, MARGIN, Inches(2.0), W - 2 * MARGIN, Inches(1.4), title, size=40, bold=True,
                   color="FFFFFF", font=self.title_font, min_size=28)
        self._text(s, MARGIN, Inches(3.5), W - 2 * MARGIN, Inches(2.0), ask, size=24, color=self.p["accent"], min_size=16)
        if notes:
            self.notes(s, notes)
        return s

    def sources_slide(self, sources, title="Sources", notes=None):
        s = self._slide(bg="FFFFFF")
        self._title(s, title)
        self._bullets(s, MARGIN, BODY_TOP, W - 2 * MARGIN, BODY_H, sources, size=14)
        if notes:
            self.notes(s, notes)
        return s

    def save(self, path):
        self.prs.save(path)
        return path
