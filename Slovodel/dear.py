import dearpygui.dearpygui as dpg


dpg.create_context()

with dpg.font_registry():
    with dpg.font("resources/Ostrovsky-Bold_0.otf", 20) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

dpg.bind_font(default_font)
dpg.create_viewport(title='Slovodel', width=600, height=300, resizable=False)

with dpg.window(tag="Primary Window", pos=(0, 0), no_title_bar=True, no_resize=True, no_collapse=True, no_close=True, no_move=True):
    with dpg.group() as slots:
        pass
    dpg.add_same_line()
    with dpg.group() as preview:
        pass
    dpg.add_button(label="Slots", parent=slots)
    dpg.add_button(label="Slots", parent=slots)

    dpg.add_button(label="preview", parent=preview)
    dpg.add_button(label="preview", parent=preview)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()