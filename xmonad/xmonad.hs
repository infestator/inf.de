import XMonad
import Control.Monad (liftM2)
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig(additionalKeys)
import System.IO

import XMonad.Util.Dmenu

myManageHook = composeAll
    [ className =? "Idea" --> doShift "3:dev"
    , className =? "Iceweasel" --> doShift "2:web"
    , className =? "Skype" --> doShift "4:comm"
    ]

main = do
    spawn "/usr/bin/xscreensaver -no-splash"
    --spawn "/usr/bin/trayer --edge top --align right --widthtype percent --width 10 --height 20 --padding 4 --margin 2 --transparent true --alpha 0 --tint 0x000000 --SetDockType true --SetPartialStrut true"
    --spawn "/usr/bin/launchy"
    xmproc <- spawnPipe "/usr/bin/xmobar"
    xmonad $ defaultConfig
        { workspaces = ["1:home", "2:web", "3:dev", "4:comm", "5:media", "6:tmp", "7", "8", "9", "0", "-", "="]
        , manageHook = myManageHook <+> manageDocks <+> manageHook defaultConfig
        , layoutHook = avoidStruts $ layoutHook defaultConfig
        , logHook = dynamicLogWithPP xmobarPP
                       { ppOutput = hPutStrLn xmproc
                       , ppTitle = xmobarColor "green" "" . shorten 50
                       }
        , modMask = mod4Mask
        } `additionalKeys`
        [ ((mod4Mask .|. shiftMask, xK_z), spawn "xscreensaver-command -lock")
        , ((controlMask, xK_Print), spawn "sleep 0.2; scrot -s")
        , ((0, xK_Print), spawn "scrot")
        , ((mod4Mask, xK_x), dmenu)
        ]
