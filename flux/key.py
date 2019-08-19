import pygame


class Key:
    BACKSPACE = pygame.K_BACKSPACE
    TAB       = pygame.K_TAB
    CLEAR     = pygame.K_CLEAR
    RETURN    = pygame.K_RETURN
    PAUSE     = pygame.K_PAUSE
    ESCAPE    = pygame.K_ESCAPE
    SPACE     = pygame.K_SPACE
    EXCLAIM   = pygame.K_EXCLAIM
    QUOTEDBL  = pygame.K_QUOTEDBL
    HASH      = pygame.K_HASH
    DOLLAR    = pygame.K_DOLLAR
    AMPERSAND = pygame.K_AMPERSAND
    QUOTE     = pygame.K_QUOTE
    LEFTPAREN = pygame.K_LEFTPAREN
    RIGHTPARE = pygame.K_RIGHTPAREN
    ASTERISK  = pygame.K_ASTERISK
    PLUS      = pygame.K_PLUS
    COMMA     = pygame.K_COMMA
    MINUS     = pygame.K_MINUS
    PERIOD    = pygame.K_PERIOD
    SLASH     = pygame.K_SLASH
    num_0     = pygame.K_0
    num_1     = pygame.K_1
    num_2     = pygame.K_2
    num_3     = pygame.K_3
    num_4     = pygame.K_4
    num_5     = pygame.K_5
    num_6     = pygame.K_6
    num_7     = pygame.K_7
    num_8     = pygame.K_8
    num_9     = pygame.K_9
    COLON     = pygame.K_COLON
    SEMICOLON = pygame.K_SEMICOLON
    LESS      = pygame.K_LESS
    EQUALS    = pygame.K_EQUALS
    GREATER   = pygame.K_GREATER
    QUESTION  = pygame.K_QUESTION
    AT        = pygame.K_AT
    LEFTBRACK = pygame.K_LEFTBRACKET
    BACKSLASH = pygame.K_BACKSLASH
    RIGHTBRAC = pygame.K_RIGHTBRACKET
    CARET     = pygame.K_CARET
    UNDERSCOR = pygame.K_UNDERSCORE
    BACKQUOTE = pygame.K_BACKQUOTE
    a         = pygame.K_a
    b         = pygame.K_b
    c         = pygame.K_c
    d         = pygame.K_d
    e         = pygame.K_e
    f         = pygame.K_f
    g         = pygame.K_g
    h         = pygame.K_h
    i         = pygame.K_i
    j         = pygame.K_j
    k         = pygame.K_k
    l         = pygame.K_l
    m         = pygame.K_m
    n         = pygame.K_n
    o         = pygame.K_o
    p         = pygame.K_p
    q         = pygame.K_q
    r         = pygame.K_r
    s         = pygame.K_s
    t         = pygame.K_t
    u         = pygame.K_u
    v         = pygame.K_v
    w         = pygame.K_w
    x         = pygame.K_x
    y         = pygame.K_y
    z         = pygame.K_z
    DELETE    = pygame.K_DELETE
    KP0       = pygame.K_KP0
    KP1       = pygame.K_KP1
    KP2       = pygame.K_KP2
    KP3       = pygame.K_KP3
    KP4       = pygame.K_KP4
    KP5       = pygame.K_KP5
    KP6       = pygame.K_KP6
    KP7       = pygame.K_KP7
    KP8       = pygame.K_KP8
    KP9       = pygame.K_KP9
    KP_PERIOD = pygame.K_KP_PERIOD
    KP_DIVIDE = pygame.K_KP_DIVIDE
    KP_MULTIP = pygame.K_KP_MULTIPLY
    KP_MINUS  = pygame.K_KP_MINUS
    KP_PLUS   = pygame.K_KP_PLUS
    KP_ENTER  = pygame.K_KP_ENTER
    KP_EQUALS = pygame.K_KP_EQUALS
    UP        = pygame.K_UP
    DOWN      = pygame.K_DOWN
    RIGHT     = pygame.K_RIGHT
    LEFT      = pygame.K_LEFT
    INSERT    = pygame.K_INSERT
    HOME      = pygame.K_HOME
    END       = pygame.K_END
    PAGEUP    = pygame.K_PAGEUP
    PAGEDOWN  = pygame.K_PAGEDOWN
    F1        = pygame.K_F1
    F2        = pygame.K_F2
    F3        = pygame.K_F3
    F4        = pygame.K_F4
    F5        = pygame.K_F5
    F6        = pygame.K_F6
    F7        = pygame.K_F7
    F8        = pygame.K_F8
    F9        = pygame.K_F9
    F10       = pygame.K_F10
    F11       = pygame.K_F11
    F12       = pygame.K_F12
    F13       = pygame.K_F13
    F14       = pygame.K_F14
    F15       = pygame.K_F15
    NUMLOCK   = pygame.K_NUMLOCK
    CAPSLOCK  = pygame.K_CAPSLOCK
    RSHIFT    = pygame.K_RSHIFT
    LSHIFT    = pygame.K_LSHIFT
    RCTRL     = pygame.K_RCTRL
    LCTRL     = pygame.K_LCTRL
    RALT      = pygame.K_RALT
    LALT      = pygame.K_LALT
    RMETA     = pygame.K_RMETA
    LMETA     = pygame.K_LMETA
    LSUPER    = pygame.K_LSUPER
    RSUPER    = pygame.K_RSUPER
    MODE      = pygame.K_MODE
    HELP      = pygame.K_HELP
    PRINT     = pygame.K_PRINT
    SYSREQ    = pygame.K_SYSREQ
    BREAK     = pygame.K_BREAK
    MENU      = pygame.K_MENU
    POWER     = pygame.K_POWER
    EURO      = pygame.K_EURO
    SCROLLOCK = pygame.K_SCROLLOCK

    def is_ESCAPE(self, event):
        return event.key == self.ESCAPE

