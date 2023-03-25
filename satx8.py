# 60-bits/266-klauses from cfg60-266.json
# there exist 8 sats:
#           5-         4-         3-         2-         1-         0- 
#           9876543210-9876543210-9876543210-9876543210-9876543210-9876543210
#           ------------------------------------------------------------------
#     sat0: 1110010110-1111000111-0011000011-0110001011-0110011000-0011101101
#     sat1: 1110010110-1111000111-0011000011-0111001011-0110011000-0011101101
#     sat2: 1110010110-1111000111-0011000011-1110001011-0110011000-0011101101
#     sat3: 1110010110-1111000111-0011000011-1111001011-0110011000-0011101101
#     sat4: 1110011110-1111000111-0011000011-0110001011-0110011000-0011101101
#     sat5: 1110011110-1111000111-0011000011-0111001011-0110011000-0011101101
#     sat6: 1110011110-1111000111-0011000011-1110001011-0110011000-0011101101
#     sat7: 1110011110-1111000111-0011000011-1111001011-0110011000-0011101101
#-----------------------------------------------------------------------------
SATS = [  
    # --- SATS[0] ---
    # 60.2+57.7+54.1+ 51.2+48.6+
    # 45.5+                      <-- .5/.7
    # 42.7+39.7+36.6+33.2+30.6+
    # 27.1+                      <-- .1/.5
    # 24.5+21.4 +
    #  18x body-sat
    #   4:0  13:1 18:1 19:0 22:0 24:0 
    #   25:0 26:0 27:1 33:0 34:0 39:0 <-- 26:*
    #   41:1 43:0 45:0 47:1 48:1 57:1
    { 0:1,  1:0,  2:1,  3:1,  4:0,  5:1,  6:1,  7:1,  8:0,  9:0,
      10:0, 11:0, 12:0, 13:1, 14:1, 15:0, 16:0, 17:1, 18:1, 19:0,
      20:1, 21:1, 22:0, 23:1, 24:0, 25:0, 26:0, 27:1, 28:1, 29:0,
      30:1, 31:1, 32:0, 33:0, 34:0, 35:0, 36:1, 37:1, 38:0, 39:0,
      40:1, 41:1, 42:1, 43:0, 44:0, 45:0, 46:1, 47:1, 48:1, 49:1,
      50:0, 51:1, 52:1, 53:0, 54:1, 55:0, 56:0, 57:1, 58:1, 59:1
    },
    # --- SATS[1] ---
    # 60.2+57.7+54.1+ 51.2+48.6+45.5+42.7+39.7+36.6+33.2+30.6+27.1+24.5+21.4
    #  18x body-sat
    #   4:0  13:1 18:1 19:0 22:0 24:0 
    #   25:0 26:1 27:1 33:0 34:0 39:0 
    #   41:1 43:0 45:0 47:1 48:1 57:1
    { 0:1,  1:0,  2:1,  3:1,  4:0,  5:1,  6:1,  7:1,  8:0,  9:0,
      10:0, 11:0, 12:0, 13:1, 14:1, 15:0, 16:0, 17:1, 18:1, 19:0,
      20:1, 21:1, 22:0, 23:1, 24:0, 25:0, 26:1, 27:1, 28:1, 29:0,
      30:1, 31:1, 32:0, 33:0, 34:0, 35:0, 36:1, 37:1, 38:0, 39:0,
      40:1, 41:1, 42:1, 43:0, 44:0, 45:0, 46:1, 47:1, 48:1, 49:1,
      50:0, 51:1, 52:1, 53:0, 54:1, 55:0, 56:0, 57:1, 58:1, 59:1
    },
    # --- SATS[2] ---
    # 60.2+57.7+54.1+ 51.2+48.6+45.7+42.7+39.7+36.6+33.2+30.6+27.1+24.5+21.4
    #  18x body-sat
    #   4:0  13:1 18:1 19:0 22:0 24:0 
    #   25:0 26:0 27:1 33:0 34:0 39:0 
    #   41:1 43:0 45:0 47:1 48:1 57:1
    { 0:1,  1:0,  2:1,  3:1,  4:0,  5:1,  6:1,  7:1,  8:0,  9:0,
      10:0, 11:0, 12:0, 13:1, 14:1, 15:0, 16:0, 17:1, 18:1, 19:0,
      20:1, 21:1, 22:0, 23:1, 24:0, 25:0, 26:0, 27:1, 28:1, 29:1,
      30:1, 31:1, 32:0, 33:0, 34:0, 35:0, 36:1, 37:1, 38:0, 39:0,
      40:1, 41:1, 42:1, 43:0, 44:0, 45:0, 46:1, 47:1, 48:1, 49:1,
      50:0, 51:1, 52:1, 53:0, 54:1, 55:0, 56:0, 57:1, 58:1, 59:1
    },
    # --- SATS[3] ---
    # 60.2+57.7+54.1+ 51.2+48.6+45.7+42.7+39.7+36.6+33.2+30.6+27.1+24.5+21.4
    #  18x body-sat
    #   4:0  13:1 18:1 19:0 22:0 24:0 
    #   25:0 26:1 27:1 33:0 34:0 39:0 
    #   41:1 43:0 45:0 47:1 48:1 57:1
    { 0:1,  1:0,  2:1,  3:1,  4:0,  5:1,  6:1,  7:1,  8:0,  9:0,
      10:0, 11:0, 12:0, 13:1, 14:1, 15:0, 16:0, 17:1, 18:1, 19:0,
      20:1, 21:1, 22:0, 23:1, 24:0, 25:0, 26:1, 27:1, 28:1, 29:1,
      30:1, 31:1, 32:0, 33:0, 34:0, 35:0, 36:1, 37:1, 38:0, 39:0,
      40:1, 41:1, 42:1, 43:0, 44:0, 45:0, 46:1, 47:1, 48:1, 49:1,
      50:0, 51:1, 52:1, 53:0, 54:1, 55:0, 56:0, 57:1, 58:1, 59:1
    },
    # --- SATS[4] ---
    # 60.2+57.7+54.1+ 51.2+48.6+45.5+42.7+39.7+36.6+33.2+30.6+27.5+24.5+21.4
    #  18x body-sat
    #   4:0  13:1 18:1 19:0 22:0 24:0 
    #   25:0 26:0 27:1 33:0 34:0 39:0 
    #   41:1 43:0 45:0 47:1 48:1 57:1
    { 0:1,  1:0,  2:1,  3:1,  4:0,  5:1,  6:1,  7:1,  8:0,  9:0,
      10:0, 11:0, 12:0, 13:1, 14:1, 15:0, 16:0, 17:1, 18:1, 19:0,
      20:1, 21:1, 22:0, 23:1, 24:0, 25:0, 26:0, 27:1, 28:1, 29:0,
      30:1, 31:1, 32:0, 33:0, 34:0, 35:0, 36:1, 37:1, 38:0, 39:0,
      40:1, 41:1, 42:1, 43:0, 44:0, 45:0, 46:1, 47:1, 48:1, 49:1,
      50:0, 51:1, 52:1, 53:1, 54:1, 55:0, 56:0, 57:1, 58:1, 59:1
    },
    # --- SATS[5] ---
    # 60.2+57.7+54.1+ 51.2+48.6+45.5+42.7+39.7+36.6+33.2+30.6+27.5+24.5+21.4
    #  18x body-sat
    #   4:0  13:1 18:1 19:0 22:0 24:0 
    #   25:0 26:1 27:1 33:0 34:0 39:0 
    #   41:1 43:0 45:0 47:1 48:1 57:1
    { 0:1,  1:0,  2:1,  3:1,  4:0,  5:1,  6:1,  7:1,  8:0,  9:0,
      10:0, 11:0, 12:0, 13:1, 14:1, 15:0, 16:0, 17:1, 18:1, 19:0,
      20:1, 21:1, 22:0, 23:1, 24:0, 25:0, 26:1, 27:1, 28:1, 29:0,
      30:1, 31:1, 32:0, 33:0, 34:0, 35:0, 36:1, 37:1, 38:0, 39:0,
      40:1, 41:1, 42:1, 43:0, 44:0, 45:0, 46:1, 47:1, 48:1, 49:1,
      50:0, 51:1, 52:1, 53:1, 54:1, 55:0, 56:0, 57:1, 58:1, 59:1
    },
    # --- SATS[6] ---
    # 60.2+57.7+54.1+ 51.2+48.6+45.7+42.7+39.7+36.6+33.2+30.6+27.5+24.5+21.4
    #  18x body-sat
    #   4:0  13:1 18:1 19:0 22:0 24:0 
    #   25:0 26:0 27:1 33:0 34:0 39:0 
    #   41:1 43:0 45:0 47:1 48:1 57:1
    { 0:1,  1:0,  2:1,  3:1,  4:0,  5:1,  6:1,  7:1,  8:0,  9:0,
      10:0, 11:0, 12:0, 13:1, 14:1, 15:0, 16:0, 17:1, 18:1, 19:0,
      20:1, 21:1, 22:0, 23:1, 24:0, 25:0, 26:0, 27:1, 28:1, 29:1,
      30:1, 31:1, 32:0, 33:0, 34:0, 35:0, 36:1, 37:1, 38:0, 39:0,
      40:1, 41:1, 42:1, 43:0, 44:0, 45:0, 46:1, 47:1, 48:1, 49:1,
      50:0, 51:1, 52:1, 53:1, 54:1, 55:0, 56:0, 57:1, 58:1, 59:1
    },
    # --- SATS[7] ---
    # 60.2+57.7+54.1+ 51.2+48.6+45.7+42.7+39.7+36.6+33.2+30.6+27.5+24.5+21.4
    #  18x body-sat
    #   4:0  13:1 18:1 19:0 22:0 24:0 
    #   25:0 26:1 27:1 33:0 34:0 39:0 
    #   41:1 43:0 45:0 47:1 48:1 57:1
    { 0:1,  1:0,  2:1,  3:1,  4:0,  5:1,  6:1,  7:1,  8:0,  9:0,
      10:0, 11:0, 12:0, 13:1, 14:1, 15:0, 16:0, 17:1, 18:1, 19:0,
      20:1, 21:1, 22:0, 23:1, 24:0, 25:0, 26:1, 27:1, 28:1, 29:1,
      30:1, 31:1, 32:0, 33:0, 34:0, 35:0, 36:1, 37:1, 38:0, 39:0,
      40:1, 41:1, 42:1, 43:0, 44:0, 45:0, 46:1, 47:1, 48:1, 49:1,
      50:0, 51:1, 52:1, 53:1, 54:1, 55:0, 56:0, 57:1, 58:1, 59:1
    }
]