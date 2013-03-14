import wrapper

#################
# UPower aliases
wrapper.system.aliases["upower"] = "org.freedesktop.UPower"
# Object path aliases
wrapper.system.upower.aliases = {
                               "upower": "/org/freedesktop/UPower"
                               }
# Interface aliases
wrapper.system.upower.upower.aliases = {
                                        "upower": "org.freedesktop.UPower"
                                       ,"properties": "org.freedesktop.DBus.Properties"
                                       }
