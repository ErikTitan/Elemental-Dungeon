class LevelData:
    def __init__(self):
        self.current_level = 0
        self.levels = [
            {
            # T: Top wall (full wall)
            # L: Left angled wall
            # R: Right angled wall
            # H: Half wall
            # C: Top left single corner
            # D: Top right single corner
            # E: Top right corner
            # F: Top left corner
            # .: Floor
            # Q: ladder

            'layout': [
            "LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTR      LTTTTTTTTTTTTTTTTTTTTTTTTTTR",
            "L.............................R      L..........................R",
            "L.............................R      L..........................R",
            "L.............................R      L..........................R",
            "L.............................R      L..........................R",
            "L.............................TTTTTTTT..........................R",
            "L...............................................................R",
            "L...............................................................R",
            "DHHHHHHHHHE.....................................................R",
            "          L...............FHHHHHHHHHHHHHHE......................R",
            "LTTTTTTTTTT...............R              L......................R",
            "L.........................R              L......................R",
            "L.........................R              L...........FHHHHHHHHHHC",
            "L.........................TTTTTTTTTTTTTTTT...........R           ",
            "L....................................................R           ",
            "L...............................Q....................TTTTTTTTTTTR",
            "L...............................................................R",
            "L...............................................................R",
            "L...............................................................R",
            "L...............................................................R",
            "L...............................................................R",
            "L...............................................................R",
            "DHHHHHHHHHHHE..............FHHHHHHHHHHE.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            DHHHHHHHHHHHHHHC          DHHHHHHHHHHHHHHHHHHHHHHHHHC"
        ],
            # W: cobweb
            # T: torch1
            # B: torch2
            # V: bones1
            # J: bones2
            # X: flag
            # Y: chain
            # Z ladder cover

            'decoration_layout': [
            " WT  Y         T       Y   T          W Y     T          Y   T  ",
            "                                                                 ",
            "                             V                                   ",
            "                                                                 ",
            "                                                                 ",
            "                                  X                              ",
            "                                                         J       ",
            "                  V                                              ",
            "                                                                 ",
            "                                                                 ",
            " W                                                               ",
            "                                                                 ",
            "                   J                                             ",
            " B                           Y   X   Y                           ",
            "                                               J                 ",
            "                                Z                                ",
            " B                                                               ",
            "                                                                 ",
            "                                                                 ",
            " B                                                               ",
            "                       V                                         ",
            "                                                                 ",
            "                                                                 ",
            "                                       B                         ",
            "                                                                 ",
            "                                                                 ",
            "              J                        B               V         ",
            "                                                                 ",
            "                                                                 ",
            "                                       B                         ",
            "                                                                 "
            ]
            },

            {
            'layout': [
            "LTTTTTTTTTR      LTTTTTTTTTTTTTTTTTTR   LTTTTTTTTTTTTTTTTTTTR",
            "L.........R      L..................R   L...................R",
            "L.........R      L..................R   L...................R",
            "L.........TTTTTTTT..........FHHHHHHHC   L...................R",
            "L...........................R           L...................R",
            "L...........................R           L...................R",
            "DHHHHHHHE...................R     FHHHHHHHHHHHHHE...........R",
            "        L.....Q.............R     R             L...........R",
            "        L...................R     R             L...........R",
            "        L...................TTTTTTR             L...........R",
            "LTTTTTTTT.........................R             L...........R",
            "L.................................TTTTTTTTTTTTTTT...........R",
            "L...........................................................R",
            "L...........................................................R",
            "L.........................FHHHHHHHHHE.......................R",
            "L.........................R         L.......................R",
            "L.........................R         L.......................R",
            "L.........................R         L.......................R",
            "L.........................TTTTTTTTTTT.......................R",
            "L...........................................................R",
            "L...........................................................R",
            "L.....................FHHHHHHHHE............................R",
            "L.....................R        L............................R",
            "L.....................R        L............................R",
            "L.....................TTTTTTTTTT............................R",
            "L...........................................................R",
            "L...........................................................R",
            "L............FHHHHHHHHHE....................................R",
            "L............R         L....................................R",
            "L............R         L....................................R",
            "DHHHHHHHHHHHHC         DHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHC"
            ],
            'decoration_layout': [
            " W     Y           T        Y  T           Y           T     ",
            "                                                             ",
            "                                                             ",
            " B                                                           ",
            "                                                             ",
            "                   V                                         ",
            "                                                             ",
            "              Z                                              ",
            "                                                             ",
            "                                                             ",
            "                                                             ",
            "                                     YX   Y     Y            ",
            " B                                                          ",
            "                                                             ",
            "                                                             ",
            " B                                         V                 ",
            "        J                                           J        ",
            "                                                             ",
            " B                          Y   X                            ",
            "                                                             ",
            "                                                             ",
            " B                              B                            ",
            "                                                    V        ",
            "                                B                            ",
            " B   J                   X                                   ",
            "                                                             ",
            "                                                             ",
            " B               X                              J            ",
            "                                                             ",
            "                                                             ",
            "                                                             "
            ]
            },
            {
            'layout': [
            "LTTTTTTTTTTTTTTTTTTTTR      LTTTTTTTTTTTR      LTTTTTTTTTTTTTTTTTTR",
            "L....................R      L...........R      L..................R",
            "L....................R      L...........R      L..................R",
            "L....................TTTTTTTT...........TTTTTTTT..................R",
            "L.................................................................R",
            "L.................................................................R",
            "L.......................FHHHHHHHHHHHHHHHE.........................R",
            "L.......................R               L.........................R",
            "DHHHHHHHE...............R               L.........................R",
            "        L...............R               L.........................R",
            "        L...............R               L.........................R",
            "        L...............R               L.........FHHHHHHHHHHHHHHHC",
            "        L...............TTTTTTTTR       L.........R                ",
            "LTTTTTTTT.......................R       L.........R                ",
            "L...............................R       L.........R                ",
            "L...............................R       L.........TTTTTTTTTTTTTTTTR",
            "L...............................R       L.........................R",
            "L...............Q...............TTTTTTTTT.........................R",
            "L.................................................................R",
            "L.................................................................R",
            "L..................FHHHHHHHHHHHHHHE...............................R",
            "L..................R              L...............................R",
            "L..................R              L...............................R",
            "L..................R              L...............................R",
            "DHHHHHHHHE.........R              L...............................R",
            "         L.........TTTTTTTTTTTTTTTT...............................R",
            "         L........................................................R",
            "         L........................................................R",
            "         L........................................................R",
            "         L........................................................R",
            "         DHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHC"
            ],
            'decoration_layout': [
            " WT    Y    T                                          Y      T     ",
            "                                                                     ",
            "     V                                            J                 ",
            "                                                                     ",
            " B                                                                  ",
            "                   J                                                ",
            "                                                                    ",
            "                                         V                          ",
            "                                                                    ",
            "                                                                    ",
            "                                                                   ",
            "                                                                    ",
            "                                                                   ",
            "               V                                                    ",
            "                                                                    ",
            "                                                                    ",
            " B                                                                 ",
            "                Z                                                   ",
            "                                                                    ",
            " B                                               J                  ",
            "                                                                    ",
            "                                                                    ",
            " B                                                                  ",
            "                                                                    ",
            "                                                                    ",
            "               J                                                    ",
            "                                                                    ",
            "                                                     V              ",
            "                                                                    ",
            "                                                                    ",
            "                                                                    "
            ]
            },
            {
            'layout': [
            "LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTR",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "DHHHHHHHHHHE...................FHHHHHHHHHHHHE....................R",
            "           L...................R            L....................R",
            "           L...................R            L....................R",
            "           L...................R            L........FHHHHHHHHHHHC",
            "           L...................R            L........R            ",
            "           L...................R            L........R            ",
            "           L...................TTTTTTTTTTTTTT........R            ",
            "LTTTTTTTTTTT.........................................TTTTTTTTTTTTR",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "L................................................................R",
            "DHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHC"
            ],
            'decoration_layout': [
            " W    T    Y         T           Y        T          Y       T      ",
            "                                                                    ",
            " B                                    V                             ",
            "                                                                    ",
            "                                                                    ",
            "                                                                   ",
            "                   J                                               ",
            "                                                                    ",
            "                                                                    ",
            "                                                                    ",
            "                                                                    ",
            "                V                                                  ",
            "                                                                    ",
            "                                                      J            ",
            " B                                                                 ",
            "                                                                    ",
            "                                                                    ",
            "                                                                    ",
            " B                                                                 ",
            "                                                                    ",
            "                                                                    ",
            "                                                                   ",
            " B                                                                  ",
            "                   J                                                ",
            "                                                                   ",
            "                                                                    ",
            " B                                            V                     ",
            "                                                                   ",
            "                                                                    ",
            "                                                                    ",
            "                                                                    "
            ]
            }
        ]

    def get_current_level(self):
        return self.levels[self.current_level]

    def next_level(self):
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            return True
        return False

    def reset(self):
        self.current_level = 0