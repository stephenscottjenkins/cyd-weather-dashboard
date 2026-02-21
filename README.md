# ESP32 Cheap Yellow Display (CYD2USB) - macOS Setup Guide

## Board Identification

You have the **CYD2USB variant** - the newer dual-port version of the ESP32-2432S028R "Cheap Yellow Display" with both Micro-USB and USB-C ports.

## ⚠️ Critical USB Port Information

Your board has a **hardware flaw** with the USB-C port:
- **The USB-C port lacks the required CC resistors**
- This means it **WILL NOT work with USB-C to USB-C cables**
- If your Mac only has USB-C ports, you need a **USB-C to USB-A adapter**, then use a USB-A to Micro-USB cable

### ✅ Recommendation: Use the Micro-USB Port

The Micro-USB port is more reliable and doesn't have the CC resistor issue.

---

## macOS Connection Setup

### Step 1: Driver Installation

#### For macOS Mojave (10.14) and Later

**Good news**: macOS Mojave and later versions have built-in CH340 drivers from Apple. You likely **don't need to install anything**.

#### For Older macOS Versions or If Needed

1. **Download Official WCH Driver**:
   - Visit: https://github.com/WCHSoftGroup/ch34xser_macos
   - Download and install the `.pkg` file

2. **Grant Permissions**:
   - Go to **System Settings > Privacy & Security**
   - Click **"Allow"** when prompted about the driver

#### For macOS Ventura/Sonoma/Sequoia Users

**Extra step required**:
- Go to **System Settings > Privacy & Security**
- Set **"Allow Accessories to Connect"** to **"Always when unlocked"**
- This is crucial for newer macOS versions to recognize USB devices

---

### Step 2: Verify Connection

After plugging in via **Micro-USB**, open Terminal and run:

```bash
ls /dev/tty.*
```

You should see something like:
```
/dev/tty.wchusbserial14310
```
or
```
/dev/cu.wchusbserial14310
```

(The number suffix may vary)

---

### Step 3: Arduino IDE Setup

#### Install ESP32 Board Support

1. Open **Arduino IDE**
2. Go to **Arduino IDE > Preferences** (or **Settings** in Arduino IDE 2.x)
3. In **"Additional Board Manager URLs"**, add:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Click **OK**
5. Go to **Tools > Board > Boards Manager**
6. Search for **"ESP32"**
7. Install **"esp32 by Espressif Systems"**

#### Board Configuration

- **Board**: Select **"ESP32 Dev Module"** (or any ESP32 board works)
- **Port**: Select `/dev/cu.wchusbserial*` (the one you verified in Step 2)
- **Upload Speed**: Set to **115200** (important - higher speeds can cause upload failures)

---

### Step 4: CYD2USB-Specific Display Configuration

Your dual-USB variant has **inverted colors** and uses the **ST7789 driver** (not ILI9341).

#### Option 1: Use CYD2USB Configuration File (Recommended)

1. Install **TFT_eSPI** library:
   - Go to **Sketch > Include Library > Manage Libraries**
   - Search for **"TFT_eSPI"**
   - Install **"TFT_eSPI by Bodmer"**

2. Download the CYD2USB-specific configuration:
   - Download `User_Setup.h` from:
     https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/blob/main/DisplayConfig/CYD2USB/User_Setup.h

3. Replace the default configuration file:
   - Location: `~/Documents/Arduino/libraries/TFT_eSPI/User_Setup.h`
   - Replace with the downloaded CYD2USB version

#### Option 2: Fix Colors in Code

Add this line to your code after initializing the display:

```cpp
tft.invertDisplay(1); // Fix color inversion for CYD2USB
```

---

## Quick Connection Test

### Test 1: WiFi Scan Example

1. In Arduino IDE, go to **File > Examples > WiFi (ESP32) > WiFiScan**
2. Click **Upload** (ensure upload speed is 115200)
3. Open **Serial Monitor** (set to 115200 baud)
4. Press the **RESET button** on the board
5. You should see nearby WiFi networks listed

### Test 2: Hello World Display Test

```cpp
#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();

void setup() {
  tft.begin();
  tft.setRotation(1); // Landscape orientation
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.setTextSize(2);
  tft.setCursor(10, 10);
  tft.println("Hello CYD2USB!");
}

void loop() {
  // Nothing here
}
```

---

## Troubleshooting

### Problem: No port showing in Arduino IDE

**Solutions**:
- Check **System Settings > Privacy & Security > "Allow Accessories to Connect"** is enabled
- Try a different USB cable (some cables are power-only)
- Use the Micro-USB port instead of USB-C
- Restart Arduino IDE after connecting the board

### Problem: Upload fails or timeout errors

**Solutions**:
- Lower upload speed to **115200** in Tools menu
- Press and hold the **BOOT** button while clicking upload, release after upload starts
- Try a different USB port
- Close any Serial Monitor windows before uploading

### Problem: Display shows wrong colors or inverted colors

**Solutions**:
- Use the CYD2USB-specific `User_Setup.h` file
- Or add `tft.invertDisplay(1);` to your code
- Some CYD2USB boards use ST7789 driver instead of ILI9341

### Problem: "Port busy" or "Access denied" error

**Solutions**:
- Close all Serial Monitor windows
- Disconnect and reconnect the board
- Restart Arduino IDE

### Problem: Board not recognized after macOS update

**Solutions**:
- Check **Privacy & Security** settings again
- Allow the board when prompted
- Reinstall CH340 driver if necessary

---

## Useful Resources

- **CYD Community GitHub**: https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display
- **Arduino-ESP32 Documentation**: https://docs.espressif.com/projects/arduino-esp32/
- **TFT_eSPI Library**: https://github.com/Bodmer/TFT_eSPI
- **Random Nerd Tutorials - CYD Guide**: https://randomnerdtutorials.com/cheap-yellow-display-esp32-2432s028r/

---

## Board Specifications

- **MCU**: ESP32-WROOM-32 (dual-core, WiFi + Bluetooth)
- **Display**: 2.8" TFT LCD (320x240 pixels)
- **Driver**: ST7789 (CYD2USB variant)
- **Touch**: Resistive touchscreen (XPT2046)
- **Storage**: MicroSD card slot
- **Memory**: 4MB Flash, 520KB RAM
- **USB-to-Serial**: CH340 chip
- **Power**: 5V via USB (115mA typical)

---

## Pin Reference

### Display Pins (Reserved - Do Not Use)
- TFT_CS: GPIO 15
- TFT_DC: GPIO 2
- TFT_MOSI: GPIO 13
- TFT_MISO: GPIO 12
- TFT_SCK: GPIO 14
- TFT_RST: -1 (no reset pin)
- TFT_LED: GPIO 21 (backlight)

### Touch Pins (Reserved)
- TOUCH_CS: GPIO 33
- TOUCH_IRQ: GPIO 36

### Available GPIO for Projects
- GPIO 35, GPIO 22, GPIO 27
- TX/RX pins (GPIO 1, GPIO 3) - but used for serial programming

### Other Peripherals
- **RGB LED**: Red (GPIO 4), Green (GPIO 16), Blue (GPIO 17)
- **SD Card**: Uses SPI pins (shared with display)
- **Speaker/Audio**: JST connector available

---

## Next Steps

1. ✅ Connect via Micro-USB port
2. ✅ Verify device shows up in `/dev/tty.*`
3. ✅ Configure Arduino IDE with ESP32 board support
4. ✅ Install TFT_eSPI library and CYD2USB config
5. ✅ Test with WiFi Scan example
6. 🚀 Start building your project!

---

## Notes

- Always use **115200 baud** for uploads to avoid timing issues
- The **BOOT** button can force programming mode if auto-reset fails
- The **RESET** button restarts your program
- Both USB ports are connected to the same CH340 chip - they share the same serial connection
- Remember: USB-C port **requires USB-A adapter** due to missing CC resistors

---

**Happy Making!** 🎉
