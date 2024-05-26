import board
import neopixel_spi as neopixel

spi = board.SPI()

NUM_PIXELS = 24
PIXEL_ORDER = neopixel.GRB

pixels = neopixel.NeoPixel_SPI(spi,
                               NUM_PIXELS,
                               pixel_order=PIXEL_ORDER,
                               auto_write=False)

default_brightness = 0.2

def on(brightness=default_brightness):
    pixels.brightness = brightness
    pixels.fill((255, 0, 0))
    pixels.show()
    print(f"WiggleLight: On, brightness = {brightness}")


def off():
    pixels.fill((0, 0, 0))
    pixels.show()
    print(f"WiggleLight: Off")