import Control.Monad (liftM2)
import Data.Ratio ((%))
import XMonad
import XMonad.Actions.FloatKeys
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ICCCMFocus
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.SetWMName
import XMonad.Layout.Accordion
import XMonad.Layout.Combo
import XMonad.Layout.Grid
import XMonad.Layout.IM
import XMonad.Layout.PerWorkspace
import XMonad.Layout.Tabbed
import XMonad.Layout.TwoPane
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig(additionalKeys)
import System.IO
import System.Cmd (system)
import System.Environment (getEnv)
import System.Exit (exitWith, ExitCode(..) )

import XMonad.Util.Dmenu

myManageHook = composeAll
    [ className =? "Idea" --> doShift "3:dev"
    , className =? "Iceweasel" --> doShift "2:web"
    , className =? "surf" --> doShift "2:web"
    , className =? "Skype" --> doShift "4:comm"
    ]

tabbedLayout = tabbed shrinkText defaultTheme

myLayoutHook = avoidStruts $
    onWorkspace "4:comm" (withIM (1%1) (ClassName "Skype") Grid) $
    tabbedLayout ||| combineTwo (TwoPane 0.03 0.5) tabbedLayout tabbedLayout

-- Multimedia keys definitions

xK_MasterLower=(0,0x1008ff11)
xK_MasterRaise=(0,0x1008ff13)
xK_MasterMute=(0,0x1008ff12)

xK_CaptureLower=(mod4Mask,0x1008ff11)
xK_CaptureRaise=(mod4Mask,0x1008ff13)
xK_CaptureMute=(mod4Mask,0x1008ff12)

-- Main configuration

main = do
    xmproc <- spawnPipe "/usr/bin/xmobar"
    xmonad $ defaultConfig
        { workspaces = ["1:home", "2:web", "3:dev", "4:comm", "5:media", "6:tmp", "7", "8", "9", "0", "-", "="]
        , manageHook = myManageHook <+> manageDocks <+> manageHook defaultConfig
        , layoutHook = myLayoutHook
        , logHook = dynamicLogWithPP xmobarPP
                       { ppOutput = hPutStrLn xmproc
                       , ppTitle = xmobarColor "green" "" . shorten 50
                       }
        , modMask = mod4Mask
        } `additionalKeys`
        [ ((mod4Mask .|. shiftMask, xK_z), spawn "xscreensaver-command -lock")
        -- Screenshot keys
        , ((controlMask, xK_Print), spawn "sleep 0.2; scrot -s")
        , ((0, xK_Print), spawn "scrot")
        -- Special clipboard keys
        , ((mod4Mask, xK_c), spawn "xsel | xclip -i -selection clipboard")
        , ((mod4Mask, xK_v), spawn "xclip -o -selection clipboard")
        -- Multimedia keys
        , (xK_MasterLower, spawn "amixer set Master 655- unmute")
        , (xK_MasterRaise, spawn "amixer set Master 655+ unmute")
        , (xK_MasterMute, spawn "amixer set Master toggle")
        , (xK_CaptureLower, spawn "amixer set Capture 655- unmute")
        , (xK_CaptureRaise, spawn "amixer set Capture 655+ unmute")
        -- Windows move&resize 
        , ((mod4Mask,               xK_Right ), withFocused (keysMoveWindow (10,0)))
        , ((mod4Mask,               xK_Left  ), withFocused (keysMoveWindow (-10,0)))
        , ((mod4Mask,               xK_Up    ), withFocused (keysMoveWindow (0,-10)))
        , ((mod4Mask,               xK_Down  ), withFocused (keysMoveWindow (0,10)))
        , ((mod4Mask .|. shiftMask, xK_Right ), withFocused (keysAbsResizeWindow ( 10,  0) (0, 0)))
        , ((mod4Mask .|. shiftMask, xK_Left  ), withFocused (keysAbsResizeWindow (-10,  0) (0, 0)))
        , ((mod4Mask .|. shiftMask, xK_Up    ), withFocused (keysAbsResizeWindow (  0,-10) (0, 0)))
        , ((mod4Mask .|. shiftMask, xK_Down  ), withFocused (keysAbsResizeWindow (  0, 10) (0, 0)))
        ]
