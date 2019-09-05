import pygame
from layer import Layer
#from events import Events


class Keys:
    BACKSPACE = (pygame.K_BACKSPACE, False)
    TAB       = (pygame.K_TAB, False)
    CLEAR     = (pygame.K_CLEAR, False)
    RETURN    = (pygame.K_RETURN, False)
    PAUSE     = (pygame.K_PAUSE, False)
    ESCAPE    = (pygame.K_ESCAPE, False)
    SPACE     = (pygame.K_SPACE, False)
    EXCLAIM   = (pygame.K_EXCLAIM, False)
    QUOTEDBL  = (pygame.K_QUOTEDBL, False)
    HASH      = (pygame.K_HASH, False)
    DOLLAR    = (pygame.K_DOLLAR, False)
    AMPERSAND = (pygame.K_AMPERSAND, False)
    QUOTE     = (pygame.K_QUOTE, False)
    LEFTPAREN = (pygame.K_LEFTPAREN, False)
    RIGHTPARE = (pygame.K_RIGHTPAREN, False)
    ASTERISK  = (pygame.K_ASTERISK, False)
    PLUS      = (pygame.K_PLUS, False)
    COMMA     = (pygame.K_COMMA, False)
    MINUS     = (pygame.K_MINUS, False)
    PERIOD    = (pygame.K_PERIOD, False)
    SLASH     = (pygame.K_SLASH, False)
    num_0     = (pygame.K_0, False)
    num_1     = (pygame.K_1, False)
    num_2     = (pygame.K_2, False)
    num_3     = (pygame.K_3, False)
    num_4     = (pygame.K_4, False)
    num_5     = (pygame.K_5, False)
    num_6     = (pygame.K_6, False)
    num_7     = (pygame.K_7, False)
    num_8     = (pygame.K_8, False)
    num_9     = (pygame.K_9, False)
    COLON     = (pygame.K_COLON, False)
    SEMICOLON = (pygame.K_SEMICOLON, False)
    LESS      = (pygame.K_LESS, False)
    EQUALS    = (pygame.K_EQUALS, False)
    GREATER   = (pygame.K_GREATER, False)
    QUESTION  = (pygame.K_QUESTION, False)
    AT        = (pygame.K_AT, False)
    LEFTBRACK = (pygame.K_LEFTBRACKET, False)
    BACKSLASH = (pygame.K_BACKSLASH, False)
    RIGHTBRAC = (pygame.K_RIGHTBRACKET, False)
    CARET     = (pygame.K_CARET, False)
    UNDERSCOR = (pygame.K_UNDERSCORE, False)
    BACKQUOTE = (pygame.K_BACKQUOTE, False)
    a         = (pygame.K_a, False)
    b         = (pygame.K_b, False)
    c         = (pygame.K_c, False)
    d         = (pygame.K_d, False)
    e         = (pygame.K_e, False)
    f         = (pygame.K_f, False)
    g         = (pygame.K_g, False)
    h         = (pygame.K_h, False)
    i         = (pygame.K_i, False)
    j         = (pygame.K_j, False)
    k         = (pygame.K_k, False)
    l         = (pygame.K_l, False)
    m         = (pygame.K_m, False)
    n         = (pygame.K_n, False)
    o         = (pygame.K_o, False)
    p         = (pygame.K_p, False)
    q         = (pygame.K_q, False)
    r         = (pygame.K_r, False)
    s         = (pygame.K_s, False)
    t         = (pygame.K_t, False)
    u         = (pygame.K_u, False)
    v         = (pygame.K_v, False)
    w         = (pygame.K_w, False)
    x         = (pygame.K_x, False)
    y         = (pygame.K_y, False)
    z         = (pygame.K_z, False)
    DELETE    = (pygame.K_DELETE, False)
    KP0       = (pygame.K_KP0, False)
    KP1       = (pygame.K_KP1, False)
    KP2       = (pygame.K_KP2, False)
    KP3       = (pygame.K_KP3, False)
    KP4       = (pygame.K_KP4, False)
    KP5       = (pygame.K_KP5, False)
    KP6       = (pygame.K_KP6, False)
    KP7       = (pygame.K_KP7, False)
    KP8       = (pygame.K_KP8, False)
    KP9       = (pygame.K_KP9, False)
    KP_PERIOD = (pygame.K_KP_PERIOD, False)
    KP_DIVIDE = (pygame.K_KP_DIVIDE, False)
    KP_MULTIP = (pygame.K_KP_MULTIPLY, False)
    KP_MINUS  = (pygame.K_KP_MINUS, False)
    KP_PLUS   = (pygame.K_KP_PLUS, False)
    KP_ENTER  = (pygame.K_KP_ENTER, False)
    KP_EQUALS = (pygame.K_KP_EQUALS, False)
    UP        = (pygame.K_UP, False)
    DOWN      = (pygame.K_DOWN, False)
    RIGHT     = (pygame.K_RIGHT, False)
    LEFT      = (pygame.K_LEFT, False)
    INSERT    = (pygame.K_INSERT, False)
    HOME      = (pygame.K_HOME, False)
    END       = (pygame.K_END, False)
    PAGEUP    = (pygame.K_PAGEUP, False)
    PAGEDOWN  = (pygame.K_PAGEDOWN, False)
    F1        = (pygame.K_F1, False)
    F2        = (pygame.K_F2, False)
    F3        = (pygame.K_F3, False)
    F4        = (pygame.K_F4, False)
    F5        = (pygame.K_F5, False)
    F6        = (pygame.K_F6, False)
    F7        = (pygame.K_F7, False)
    F8        = (pygame.K_F8, False)
    F9        = (pygame.K_F9, False)
    F10       = (pygame.K_F10, False)
    F11       = (pygame.K_F11, False)
    F12       = (pygame.K_F12, False)
    F13       = (pygame.K_F13, False)
    F14       = (pygame.K_F14, False)
    F15       = (pygame.K_F15, False)
    NUMLOCK   = (pygame.K_NUMLOCK, False)
    CAPSLOCK  = (pygame.K_CAPSLOCK, False)
    RSHIFT    = (pygame.K_RSHIFT, False)
    LSHIFT    = (pygame.K_LSHIFT, False)
    RCTRL     = (pygame.K_RCTRL, False)
    LCTRL     = (pygame.K_LCTRL, False)
    RALT      = (pygame.K_RALT, False)
    LALT      = (pygame.K_LALT, False)
    RMETA     = (pygame.K_RMETA, False)
    LMETA     = (pygame.K_LMETA, False)
    LSUPER    = (pygame.K_LSUPER, False)
    RSUPER    = (pygame.K_RSUPER, False)
    MODE      = (pygame.K_MODE, False)
    HELP      = (pygame.K_HELP, False)
    PRINT     = (pygame.K_PRINT, False)
    SYSREQ    = (pygame.K_SYSREQ, False)
    BREAK     = (pygame.K_BREAK, False)
    MENU      = (pygame.K_MENU, False)
    POWER     = (pygame.K_POWER, False)
    EURO      = (pygame.K_EURO, False)
    SCROLLOCK = (pygame.K_SCROLLOCK, False)
    #change this to size of number of keys
    KEYS_PRESSED = [0] * 600

    @classmethod
    def key_pressed(cls, key, layer=None):
        key_value = cls.__dict__[key]

        if layer:
            if Layer.get_layer() == layer:
                return cls.KEYS_PRESSED[key_value]
        else:
            return cls.KEYS_PRESSED[key_value]

    @classmethod
    def key_pressed_once(cls, key, layer=None):
        key_value = cls.__dict__[key]

        if layer:
            if Layer.get_layer() == layer:
                if cls.KEYS_PRESSED[key_value[0]]:
                    if not key_value[1]:
                        key_value[1] = True

        else:
            return cls.KEYS_PRESSED[key_value]

    @classmethod
    def update(cls):
        cls.KEYS_PRESSED = pygame.key.get_pressed()
