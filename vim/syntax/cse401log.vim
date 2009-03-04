:syntax match Underlined /^[^*].*[^l]legal.*$/
:syntax match Todo /^[^*].*illegal.*$/
:syntax match Error /^.*error.*/
:highlight Underlined cterm=NONE ctermbg=Blue gui=NONE guibg=Blue
