import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.SPI as SPI
# Python library for st7032 LCD using SPI
# COMMANDS

# Write "20H" to DDRAM. and set DDRAM address to "00H" from AC

LCD_CLEARDISPLAY_ = 0x01  

# SET DDRAM address to "00H" from AC and return cursor to its original position if shifted. The contents of DDRAM are not changed.
LCD_RETURNHOME_ = 0x02  

# SETS cursor move direction and specifies display shift. These operations are performed during data write and read.
LCD_ENTRYMODESET_ = 0x04  

# flags for display entry mode
LCD_ENTRYRIGHT_ = 0x00  
LCD_ENTRYLEFT_ = 0x02  
LCD_ENTRYSHIFTINCREMENT_ = 0x01  
LCD_ENTRYSHIFTDECREMENT_ = 0x00  

# SETS: entire display on/off, cursor on/off, cursor position on/off
LCD_DISPLAYCONTROLSET_ = 0x08  

# flags for display control set
LCD_DISPLAYON_ = 0x04  
LCD_DISPLAYOFF_ = 0x00  
LCD_CURSORON_ = 0x02  
LCD_CURSOROFF_ = 0x00  
LCD_BLINKON_ = 0x01  
LCD_BLINKOFF_ = 0x00  

# SETS: interface data is 8/4 bits, number of line is 2/1, double height font, instruction table select.
LCD_FUNCTIONSET_ = 0x20       

# flags for function set
LCD_8BITMODE_ = 0x10  
LCD_4BITMODE_ = 0x00  
LCD_2LINE_ = 0x08  
LCD_1LINE_ = 0x00  
LCD_5x10DOTS_ = 0x04  
LCD_5x8DOTS_ = 0x00  
LCD_INSTRUCTIONTABLE_1_ = 0x01  
LCD_INSTRUCTIONTABLE_0_ = 0x00  

# SET DDRAM address in address counter
LCD_SETDDRAM_ADDR_ = 0x80      

#=== INSTRUCTION TABLE 0 (IS=0)
# SET cursor moving and display shift control bit, and the direction, without changing DDRAM data.
LCD_CURSORSHIFTSET_ = 0x10        

# flags for display/cursor shift
LCD_DISPLAYMOVE_ = 0x08  
LCD_CURSORMOVE_ = 0x00  
LCD_MOVERIGHT_ = 0x04  
LCD_MOVELEFT_ = 0x00
LCD_SETCGRAMADDR_ = 0x40

# Instruction Table 1 (IS=1)
LCD_BIASINTOSCSET_ = 0x10

# Bias selection flags
LCD_BIAS_1_4_ = 0x08
LCD_BIAS_1_5_ = 0x00

# Adjust Internal OSC flags
LCD_OSC_122HZ_ = 0x00
LCD_OSC_131HZ_ = 0x01
LCD_OSC_144HZ_ = 0x02
LCD_OSC_161HZ_ = 0x03
LCD_OSC_183HZ_ = 0x04
LCD_OSC_221HZ_ = 0x05
LCD_OSC_274HZ_ = 0x06
LCD_OSC_347HZ_ = 0x07

# Icon address and power control
LCD_SETICONADDR_ = 0x40
LCD_POWER_CONTROL_ = 0x56

# Power / ICON control / Contrast set (high byte)
LCD_POWICONCONTRASTHSET_ = 0x50

# Power / ICON control / Contrast set flags (high byte)
LCD_ICON_ON_ = 0x08
LCD_ICON_OFF_ = 0x00
LCD_BOOST_ON_ = 0x04
LCD_BOOST_OFF_ = 0x00
LCD_CONTRAST_C5_ON_ = 0x02
LCD_CONTRAST_C4_ON_ = 0x01

# Follower control
LCD_FOLLOWERCONTROLSET_ = 0x60

# Follower control flags
LCD_FOLLOWER_ON_ = 0x08
LCD_FOLLOWER_OFF_ = 0x00

# Rb/Ra ratio settings
LCD_RAB_1_00_ = 0x00
LCD_RAB_1_25_ = 0x01
LCD_RAB_1_50_ = 0x02
LCD_RAB_1_80_ = 0x03
LCD_RAB_2_00_ = 0x04
LCD_RAB_2_50_ = 0x05
LCD_RAB_3_00_ = 0x06
LCD_RAB_3_75_ = 0x07

# Contrast set (low byte)
LCD_CONTRASTSET_ = 0x70

# Contrast set flags (low byte)
LCD_CONTRAST_C3_ON_ = 0x08
LCD_CONTRAST_C2_ON_ = 0x04
LCD_CONTRAST_C1_ON_ = 0x02
LCD_CONTRAST_C0_ON_ = 0x01


class HEL_LCD(object):

    def __init__(self, spi_bus=1,spi_device=0, cs_pin="P9_17", rs_pin="P9_27", rst_pin="P9_23", spi_speed_hz= 4000000 ):
        self.cs_pin = cs_pin
        self.rs_pin = rs_pin
        self.rst_pin = rst_pin

        # Setup GPIO
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.setup(self.rs_pin, GPIO.OUT)
        GPIO.setup(self.rst_pin, GPIO.OUT)

        # Setup SPI
        self.spi = SPI.SPI(spi_bus, spi_device)
        self.spi.msh = spi_speed_hz
        self.spi.mode= 0
        #LCD init
        
        GPIO.output(self.rs_pin, GPIO.HIGH)
        GPIO.output(self.rst_pin, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.rst_pin, GPIO.HIGH)
        time.sleep(0.020)
        self.HEL_LCD_Command(LCD_FUNCTIONSET_ | LCD_8BITMODE_) #wake up 0X30
        time.sleep(0.002)
        self.HEL_LCD_Command(LCD_FUNCTIONSET_ | LCD_8BITMODE_) #wake up 0X30
        self.HEL_LCD_Command(LCD_FUNCTIONSET_ | LCD_8BITMODE_) #wake up 0X30
        self.HEL_LCD_Command(LCD_FUNCTIONSET_ | LCD_8BITMODE_ | LCD_2LINE_ | LCD_INSTRUCTIONTABLE_1_) #0x39 Lcd in 8 bit mode and 2*16 lines
        self.HEL_LCD_Command(LCD_BIASINTOSCSET_  | LCD_BIAS_1_5_ | LCD_OSC_347HZ_) #0x17 Set the lcd to work with the internal oscillator at 347hz
        self.HEL_LCD_Command(LCD_POWICONCONTRASTHSET_ | LCD_BOOST_ON_ | LCD_CONTRAST_C5_ON_)#0x56
        self.HEL_LCD_Command(LCD_FOLLOWERCONTROLSET_ | LCD_FOLLOWER_ON_ | LCD_RAB_2_50_);                   
        time.sleep(0.2)
        self.HEL_LCD_Command(LCD_CONTRASTSET_);                                                            #Set lcd contrast 
        self.HEL_LCD_Command(LCD_DISPLAYCONTROLSET_ | LCD_DISPLAYON_ | LCD_CURSORON_| LCD_BLINKOFF_);      #Lcd display on, Cursor on, Blink off
        self.HEL_LCD_Command(LCD_ENTRYMODESET_ | LCD_ENTRYLEFT_ | LCD_ENTRYSHIFTDECREMENT_);               #Lcd shit from left to right 
        self.HEL_LCD_Command(LCD_CLEARDISPLAY_);                                                           #Clear the display 
        time.sleep( 0.001 );  
        
    # Method to send commands to the lcd 
    def HEL_LCD_Command(self, command):
          GPIO.output(self.rs_pin, GPIO.LOW) # instruction mode 
          GPIO.output(self.cs_pin, GPIO.LOW)
          self.spi.writebytes([command])
          GPIO.output(self.cs_pin, GPIO.HIGH)
          time.sleep(0.00003)
    
    # Method to send data to the lcd     
    def HEL_LCD_Data(self,data):
          GPIO.output(self.rs_pin, GPIO.HIGH) # data mode
          GPIO.output(self.cs_pin, GPIO.LOW)
          self.spi.writebytes([data])
          GPIO.output(self.cs_pin, GPIO.HIGH)
          time.sleep(0.00003)
    
    def HEL_LCD_String(self,string):
          for char in string:
            self.HEL_LCD_Data(ord(char))
    
    def HEL_LCD_SetCursor(self,row,colum):
          if(row != 0):
            row = 0x40;
          else:
            row = 0
          if(colum in range(16)):
            colum = colum
          else:
            colum = 0
          
          self.HEL_LCD_Command( LCD_SETDDRAM_ADDR_ | (row + colum) )
          
    def HEL_LCD_Contrast(self,contrast):
          self.HEL_LCD_Command(LCD_CONTRASTSET_ | (contrast & 0x0F) );
    def HEL_LCD_Clear(self):
          self.HEL_LCD_Command(LCD_CLEARDISPLAY_);
          time.sleep(0.002)

          
        
         
        

if __name__ == '__main__':
    print("iniciando codigo")
    lcd = HEL_LCD(spi_bus = 1,spi_device=0, cs_pin="P9_17", rs_pin="P9_25", rst_pin="P9_23")
    lcd.HEL_LCD_Contrast(0)
    lcd.HEL_LCD_SetCursor(0,5)
    time.sleep(0.8)
    lcd.HEL_LCD_String("MODULAR")
    lcd.HEL_LCD_SetCursor(1,8)
    lcd.HEL_LCD_String("MX")
    time.sleep(5)
    lcd.HEL_LCD_Clear()