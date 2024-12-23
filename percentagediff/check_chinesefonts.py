import matplotlib.font_manager as fm

# List all fonts available in matplotlib
for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    print(fm.FontProperties(fname=font).get_name())