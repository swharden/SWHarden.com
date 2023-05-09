---
title: ATTiny2313 Controlling a HD44780 LCD with AVR-GCC
date: 2009-05-17 20:27:44
---



__After a day of tinkering I finally figured out how to control a HD44780 display from an ATTiny2313 microcontroller.__ There are a _lot_ of websites out there claiming to show you how to do this on similar AVRs. I tried about 10 of them and, intriguingly, only one of them worked! I think the problem is that many of those websites show code for an ATMega8 and I'm using an ATTiny2313. Since it took me so long to get this right I decided to share it on the internet for anyone else having a similar struggle.

<div class="text-center img-border">

![](https://swharden.com/static/2009/05/17/attiny_2313_lcd_hd44780.jpg)
![](https://swharden.com/static/2009/05/17/attiny_2313_lcd_hd44780_2.jpg)

</div>

__You might recognize this LCD panel__ from some [PC parallel port / LCD interface projects](http://www.swharden.com/blog/old-stuff-of-interest/#lcd) I worked on about 5 years ago. It's a 20-column, 2-row, 8-bit parallel character LCD. This means that rather than telling each little square to light up to form individual letters, you can just output text to the microcontroller embedded in the display and it can draw the letters, move the cursor, or clear the screen. These are the connections I made were:

*   LCD1 -&gt; GND
*   LCD2 -&gt; +5V
*   LCD3 (contrast) -&gt; GND
*   LCD4 (RS) -&gt; AVR D0 (pin2)
*   LCD5 (R/W) -&gt; AVR D1 (pin3)
*   LCD6 (ES) -&gt; AVR D2 (pin6)
*   LCD 11-14 (data) -&gt; AVR B0-B3 (pins 12-15)

__The code to control this LCD from the ATTiny2313__ was found on Martin Thomas' page (dead link removed in 2019). I included the .h and .c files and successfully ran the following program on my AVR. I used the internal RC clock.

```c
// ATTiny2313 / HD44780 LCD INTERFACE
#include <stdlib.h>;
#include <avr/io.h>;
#include <util/delay.h>;
#include "lcd.h"
#include "lcd.c"

int main(void)
{
    int i=0;
    lcd_init(LCD_DISP_ON);
    lcd_clrscr();
    lcd_puts("ATTiny 2313 LCD Demo");
    lcd_puts("  www.SWHarden.com  ");
    _delay_ms(1000);
    lcd_clrscr();
    for (;;) {
        lcd_putc(i);
        i++;
        _delay_ms(50);
    }
}
```

```c
// modified the top of "lcd.h"
#define LCD_PORT         PORTB        /**&lt; port for the LCD lines   */
#define LCD_DATA0_PORT   LCD_PORT     /**&lt; port for 4bit data bit 0 */
#define LCD_DATA1_PORT   LCD_PORT     /**&lt; port for 4bit data bit 1 */
#define LCD_DATA2_PORT   LCD_PORT     /**&lt; port for 4bit data bit 2 */
#define LCD_DATA3_PORT   LCD_PORT     /**&lt; port for 4bit data bit 3 */
#define LCD_DATA0_PIN    0            /**&lt; pin for 4bit data bit 0  */
#define LCD_DATA1_PIN    1            /**&lt; pin for 4bit data bit 1  */
#define LCD_DATA2_PIN    2            /**&lt; pin for 4bit data bit 2  */
#define LCD_DATA3_PIN    3            /**&lt; pin for 4bit data bit 3  */
#define LCD_RS_PORT      PORTD     /**&lt; port for RS line         */
#define LCD_RS_PIN       0            /**&lt; pin  for RS line         */
#define LCD_RW_PORT      PORTD     /**&lt; port for RW line         */
#define LCD_RW_PIN       1            /**&lt; pin  for RW line         */
#define LCD_E_PORT       PORTD     /**&lt; port for Enable line     */
#define LCD_E_PIN        2            /**&lt; pin  for Enable line     */

// AND A LITTLE LOWER, I CHANGED THIS LINE TO 4-BIT MODE
#define LCD_FUNCTION_8BIT     0      /*   DB4: set 8BIT mode (0-&gt;4BIT mode) */
```

__Here is video of the output.__ Notice how this display can show English (lowercase/uppercase/numbers) as well as the Japanese character set!

{{<youtube mMEwFSkr1Ko>}}

<blockquote>

**Note from Future Scott (ten years later, August, 2019):**

The link to the downloadable source code from Martin Thomas' page is no longer functional. These links do work:

* https://senzor.robotika.sk/sensorwiki/index.php/AVR_lcd.c 

* https://senzor.robotika.sk/sensorwiki/index.php/AVR_lcd.h 

A more recent project which uses these displays is:

* https://www.swharden.com/wp/2017-04-29-precision-pressure-meter-project/ 

</blockquote>
