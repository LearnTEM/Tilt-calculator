from nicegui import ui, Tailwind
from nicegui.events import ValueChangeEventArguments
from tiltdata import TiltData

# def show(event: ValueChangeEventArguments):
#     name = type(event.sender).__name__
#     ui.notify(f'{name}: {event.value}')

def rotate(event: ValueChangeEventArguments):
    dp.style(f"transform: rotate({-data.rotate_theta}deg)")
    # ui.notify(f'{data.rotate_theta}')
    pass

def calculate():
    data.calculate()
    ui.notify(f"α={data.alpha2}\nβ={data.beta2}")

data = TiltData()

ui.markdown("## Tilt Calculator")
ui.markdown("Input index of the zone axis:")

hkl_style = Tailwind().width('10 px')
alphabeta_style = Tailwind().width("20 px")

with ui.row():
    ui.input("h").bind_value_to(data, "h1").tailwind(hkl_style)
    ui.input("k").bind_value_to(data, "k1").tailwind(hkl_style)
    ui.input("l").bind_value_to(data, "l1").tailwind(hkl_style)
# ui.markdown(f"Ensure hkl: {data.hkl1[0]}{data.hkl1[1]}{data.hkl1[2]}")
# ui.label(f"{data.h1}{data.k1}{data.l1}").bind_text_from(data, "h1",lambda a: f"h1: {a}")
ui.markdown("Input current α and β angle:")
with ui.row():
    ui.input("α").bind_value_to(data, "alpha1").tailwind(alphabeta_style)
    ui.input("β").bind_value_to(data, "beta1").tailwind(alphabeta_style)
ui.markdown("Select direction of diffraction pattern:")
dp = ui.image("./100.svg").style("width: 80pt")
ui.slider(min=-90, max=90, step=1, value=0, on_change=rotate).bind_value_to(data, "rotate_theta")
ui.markdown("Input index of target zone axis:")
with ui.row():
    ui.input("h").bind_value_to(data, "h2").tailwind(hkl_style)
    ui.input("k").bind_value_to(data, "k2").tailwind(hkl_style)
    ui.input("l").bind_value_to(data, "l2").tailwind(hkl_style)
ui.button("Calculate!", on_click=calculate)
ui.run(title="Tilt Calculator")