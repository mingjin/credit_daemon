# -*- coding: utf-8 -*-

import rabird.winio
import time
import atexit

# KeyBoard Commands
# Command port
KBC_KEY_CMD = 0x64
# Data port
KBC_KEY_DATA = 0x60

__winio = None

KBC_KEY_MAP = {
    '0' : 0x0B,
    '1' : 0x02,
    '2' : 0x03,
    '3' : 0x04,
    '4' : 0x05,
    '5' : 0x06,
    '6' : 0x07,
    '7' : 0x08,
    '8' : 0x09,
    '9' : 0x0A,
    'q' : 0x10,
    'w' : 0x11,
    'e' : 0x12,
    'r' : 0x13,
    't' : 0x14,
    'y' : 0x15,
    'u' : 0x16,
    'i' : 0x17,
    'o' : 0x18,
    'p' : 0x19,
    'a' : 0x1e,
    's' : 0x1f,
    'd' : 0x20,
    'f' : 0x21,
    'g' : 0x22,
    'h' : 0x23,
    'j' : 0x24,
    'k' : 0x25,
    'l' : 0x26,
    'z' : 0x2c,
    'x' : 0x2d,
    'c' : 0x2e,
    'v' : 0x2f,
    'b' : 0x30,
    'n' : 0x31,
    'm' : 0x32,
    }

def __get_winio():
    global __winio

    if __winio is None:
            __winio = rabird.winio.WinIO()
            def __clear_winio():
                    global __winio
                    __winio = None
            atexit.register(__clear_winio)

    return __winio

def wait_for_buffer_empty():
    '''
    Wait keyboard buffer empty
    '''

    winio = __get_winio()

    dwRegVal = 0x02
    while (dwRegVal & 0x02):
            dwRegVal = winio.get_port_byte(KBC_KEY_CMD)

def key_down(scancode):
    winio = __get_winio()

    wait_for_buffer_empty();
    winio.set_port_byte(KBC_KEY_CMD, 0xd2);
    wait_for_buffer_empty();
    winio.set_port_byte(KBC_KEY_DATA, scancode)

def key_up(scancode):
    winio = __get_winio()

    wait_for_buffer_empty();
    winio.set_port_byte( KBC_KEY_CMD, 0xd2);
    wait_for_buffer_empty();
    winio.set_port_byte( KBC_KEY_DATA, scancode | 0x80);

def key_press(scancode, press_time = 0.2):
    key_down( scancode )
    time.sleep( press_time )
    key_up( scancode )

def password_type(password):
    for c in password.strip():
       if c.isalpha():
           if c.isupper():
               upper_case_char_press(c)
           else:
               lower_case_char_press(c)
       elif c.isdigit():
           lower_case_char_press(c)
       else:
           raise Exception(password+' contains invalid characters')

def upper_case_char_press(char, press_time = 0.2):
    key_down(0x2a)
    key_press(KBC_KEY_MAP[char.lower()])
    key_up(0x2a)

def lower_case_char_press(char, press_time = 0.2):
    key_press(KBC_KEY_MAP[char])

if __name__ == '__main__':
    password = 'abcABC123'
    result = password_type(password)
    print result

#End

# Press 'A' key
# Scancodes references : https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
# key_press(0x1E)
