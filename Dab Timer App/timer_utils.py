# timer_utils.py

material_times   = {'Quartz':30, 'Titanium':45, 'Ceramic':40}
style_modifiers  = {'Flat Top':1.0, 'Slanted':0.9, 'Thermal':1.2, 'Terp Slurper':1.1}
wax_cool_times   = {'Shatter':45, 'Budder':50, 'Crumble':47, 'Rosin':43, 'Live Resin':48, 'Sugar':46}

def calculate_heat_time(material: str, style: str, intensity: float) -> int:
    base   = material_times[material]
    mod    = style_modifiers[style]
    return max(1, int(base * mod / intensity))

def calculate_cool_time(wax: str, style: str) -> int:
    base   = wax_cool_times[wax]
    mod    = style_modifiers[style]
    return int(base * mod)