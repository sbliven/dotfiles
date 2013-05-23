base03="#00002B2B3636"
base02="#070736364242"
base01="#58586E6E7575"
base00="#65657B7B8383"
base0="#838394949696"
base1="#9393A1A1A1A1"
base2="#EEEEE8E8D5D5"
base3="#FDFDF6F6E3E3"

yellow="#B5B589890000"
orange="#CBCB4B4B1616"
red="#D3D301010202"
magenta="#D3D336368282"
violet="#6C6C7171C4C4"
blue="#26268B8BD2D2"
cyan="#2A2AA1A19898"
green="#858599990000"

style=${1:-dark}
#style=light

# Check parameters
case $style in
    dark)
        ;;
    light)
        ;;
    *)
        echo "usage: $0 [dark|light]"
        exit
esac

gconftool-2 --set "/apps/gnome-terminal/profiles/Default/use_theme_background" --type bool false
gconftool-2 --set "/apps/gnome-terminal/profiles/Default/use_theme_colors" --type bool false
gconftool-2 --set "/apps/gnome-terminal/profiles/Default/palette" --type string "$base02:$red:$green:$yellow:$blue:$magenta:$cyan:$base2:$base03:$orange:$base01:$base00:$base0:$violet:$base1:$base3"

case $style in
    dark)
        gconftool-2 --set "/apps/gnome-terminal/profiles/Default/background_color" --type string "$base03"
        gconftool-2 --set "/apps/gnome-terminal/profiles/Default/foreground_color" --type string "$base0"
        ;;
    light)
        gconftool-2 --set "/apps/gnome-terminal/profiles/Default/background_color" --type string "$base3"
        gconftool-2 --set "/apps/gnome-terminal/profiles/Default/foreground_color" --type string "$base00"
        ;;
esac
