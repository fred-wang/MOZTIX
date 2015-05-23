# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
import bisect
import fontforge
import sys

def insortWithoutDuplicate(aList, aValue):
    insertPosition = bisect.bisect_left(aList, aValue)
    if insertPosition == len(aList) or aList[insertPosition] != aValue:
        aList.insert(insertPosition, aValue)

def binarySearchHasValue(aList, aValue):
    insertPosition = bisect.bisect_left(aList, aValue)
    return insertPosition < len(aList) and aList[insertPosition] == aValue

def isBasicLatin(aCodePoint):
    return 0 <= aCodePoint and aCodePoint <= 0xFFF

def isSpacingModifierLetter(aCodePoint):
    return 0x02B0 <= aCodePoint and aCodePoint <= 0x02FF

def isCombiningDiacriticalMark(aCodePoint):
    return 0x0300 <= aCodePoint and aCodePoint <= 0x036F

def isGeneralPunctuation(aCodePoint):
    return 0x2000 <= aCodePoint and aCodePoint <= 0x206F

def isCombiningMarkForSymbols(aCodePoint):
    return 0x20D0 <= aCodePoint and aCodePoint <= 0x20FF

def isArrow(aCodePoint):
    return 0x2190 <= aCodePoint and aCodePoint <= 0x21FF

def isMathematicalSymbol(aCodePoint):
    return 0x2200 <= aCodePoint and aCodePoint <= 0x22FF

def isMiscellaneousTechnical(aCodePoint):
    return 0x2300 <= aCodePoint and aCodePoint <= 0x23FF

def isEnclosedAlphanumeric(aCodePoint):
    return 0x2460 <= aCodePoint and aCodePoint <= 0x24FF

def isGeometricShape(aCodePoint):
    return 0x25A0 <= aCodePoint and aCodePoint <= 0x25FF

def isMiscelleanousSymbol(aCodePoint):
    return 0x2600 <= aCodePoint and aCodePoint <= 0x26FF

def isDingBats(aCodePoint):
    return 0x2700 <= aCodePoint and aCodePoint <= 0x27BF

def isMiscelleanousMathSymbol(aCodePoint):
    return 0x27C0 <= aCodePoint and aCodePoint <= 0x27EF

def isSupplementalArrowA(aCodePoint):
    return 0x27F0 <= aCodePoint and aCodePoint <= 0x27FF

def isSupplementalArrowB(aCodePoint):
    return 0x2900 <= aCodePoint and aCodePoint <= 0x297F

def isMiscelleanousMathSymbolB(aCodePoint):
    return 0x2980 <= aCodePoint and aCodePoint <= 0x29FF

def isMathOperatorSupplement(aCodePoint):
    return 0x2A00 <= aCodePoint and aCodePoint <= 0x2AFF

def isSupplementalSymbolAndArrow(aCodePoint):
    return 0x2B00 <= aCodePoint and aCodePoint <= 0x2BFF

def isHiragana(aCodePoint):
    return 0x3040 <= aCodePoint <= 0x3097

def isBoldMathVariant(aCodePoint):
    return ((0x1D400 <= aCodePoint and aCodePoint <= 0x1D433) or
            (0x1D6A8 <= aCodePoint and aCodePoint <= 0x1D6E1) or
            (0x1D7CA <= aCodePoint and aCodePoint <= 0x1D7CB) or
            (0x1D7CE <= aCodePoint and aCodePoint <= 0x1D7D7))

def isBoldItalicMathVariant(aCodePoint):
    return ((0x1D468 <= aCodePoint and aCodePoint <= 0x1D49B) or
            (0x1D71C <= aCodePoint and aCodePoint <= 0x1D755))

def isBoldScriptMathVariant(aCodePoint):
    return 0x1D4D0 <= aCodePoint and aCodePoint <= 0x1D503

def isBoldFrakturMathVariant(aCodePoint):
    return 0x1D56C <= aCodePoint and aCodePoint <= 0x1D59F

def isSansSerifMathVariant(aCodePoint):
    return ((0x1D5A0 <= aCodePoint and aCodePoint <= 0x1D5D3) or
            (0x1D7E2 <= aCodePoint and aCodePoint <= 0x1D7EB))

def isBoldSansSerifMathVariant(aCodePoint):
    return ((0x1D5D4 <= aCodePoint and aCodePoint <= 0x1D607) or
            (0x1D756 <= aCodePoint and aCodePoint <= 0x1D78F) or
            (0x1D7EC <= aCodePoint and aCodePoint <= 0x1D7F5))

def isSansSerifItalicMathVariant(aCodePoint):
    return 0x1D608 <= aCodePoint and aCodePoint <= 0x1D63B

def isSansSerifBoldItalicMathVariant(aCodePoint):
    return ((0x1D63C <= aCodePoint and aCodePoint <= 0x1D66F) or
            (0x1D790 <= aCodePoint and aCodePoint <= 0x1D7C9))

def isMonospaceMathVariant(aCodePoint):
    return ((0x1D670 <= aCodePoint and aCodePoint <= 0x1D6A3) or
            (0x1D7F6 <= aCodePoint and aCodePoint <= 0x1D7FF))

def isStretchable(aFont, aCodePoint):
    if aCodePoint not in aFont:
        return False
    glyph  = aFont[aCodePoint]
    return (glyph.horizontalVariants is not None or
            glyph.horizontalComponents is not None or
            glyph.verticalVariants is not None or
            glyph.verticalComponents is not None)

def getSSTYList(aGlyph):
    for table in aGlyph.getPosSub("*"):
        if table[0].find("ssty") > 0:
            return table[2:]
    return None

if __name__ == "__main__":
    # Check command line argument
    if len(sys.argv) != 5:
        print("usage: python %s input output charList metadata.xml" % sys.argv[0], file=sys.stderr)
        exit(1)

    # Open the input font.
    font = fontforge.open(sys.argv[1])

    # Rename the font for conformance with OFL
    font.familyname = "MOZTIX Math"
    font.fontname = "MOZTIXMath-Regular"
    font.fullname = "MOZTIX Math Regular"

    # Keep STIX as the font vendor.
    # font.os2_vendor = "STIX"

    # Add Mozilla Corporation as a copyright holder.
    font.copyright = "Copyright (c) 2015 by Mozilla Corporation. %s" % font.copyright

    # Add information for the modified MOZTIX version.
    # This should be kept consistent with the metadata.xml file.
    sfnt_names = []
    for t in font.sfnt_names:
        language = t[0]
        strid = t[1]
        string = t[2]
        if strid == "Fullname":
            # Update the font name. This also fixes the following warning from
            # fontforge:
            # > Note: Mac and Windows entries in the 'name' table differ for the
            # > Fullname string in the language English (US)
            # > Mac String: STIX Math Regular
            # > Windows String: STIXMath-Regular
            string = font.fullname
        elif strid == "Copyright":
            # Update the copyright
            string = font.copyright
        elif strid == "Designer":
            # Add Frederic Wang to the list of designers.
            string = "%s. MOZTIX subset by Frederic Wang." % string
        elif strid == "Descriptor":
            # Add short description of MOZTIX.
            string = "%s In order to bundle a math font into Mozilla products, a minimal subset was extracted to form the MOZTIX font." % string
        elif strid == "Vendor URL":
            # Keep "STIX" as the vendor
            # string = "http://stixfonts.org/"
            None
        elif strid == "UniqueID":
            # Skip this id, so that FontForge will generate a new one.
            continue
        elif strid == "License URL":
            # Use the OFL url instead of the one from the STIX Website.
            string = "http://scripts.sil.org/OFL"
        sfnt_names.append((language, strid, string))
    font.sfnt_names = tuple(sfnt_names)

    # Add WOFF information
    font.woffMajor = 1
    font.woffMinor = 1
    with open(sys.argv[3], "r") as metadataFile:
        font.woffMetadata = metadataFile.read()

    # Ensure that USE_TYPO_METRICS is set.
    # See https://sourceforge.net/p/stixfonts/tracking/64/
    if font.os2_version and font.os2_version < 4:
        font.os2_version = 4
    font.os2_use_typo_metrics = True

    # Add size variants for arrows
    # See https://sourceforge.net/p/stixfonts/tracking/69/
    font[0x2190].horizontalVariants = font[0x27F5].glyphname
    font[0x2192].horizontalVariants = font[0x27F6].glyphname
    font[0x2194].horizontalVariants = font[0x27F7].glyphname
    font[0x21A4].horizontalVariants = font[0x27FB].glyphname
    font[0x21A6].horizontalVariants = font[0x27FC].glyphname
    font[0x21D0].horizontalVariants = font[0x27F8].glyphname
    font[0x21D0].horizontalVariants = font[0x27F8].glyphname
    font[0x21D2].horizontalVariants = font[0x27F9].glyphname
    font[0x21D4].horizontalVariants = font[0x27FA].glyphname

    # Copy some data for short arrows to stretch long arrows
    # See https://sourceforge.net/p/stixfonts/tracking/65/
    font[0x27F5].horizontalComponents = font[0x2190].horizontalComponents
    font[0x27F6].horizontalComponents = font[0x2192].horizontalComponents
    font[0x27F7].horizontalComponents = font[0x2194].horizontalComponents

    # Set data some horizontal accents
    # See https://sourceforge.net/p/stixfonts/tracking/66/
    font[0x00AF].horizontalComponents = \
        (('macron', 0, 0, 50, 311), ('macron', 1, 50, 0, 311))
    font[0x203E].horizontalComponents = font[0x00AF].horizontalComponents
    font[0x005F].horizontalComponents = \
        (('underscore', 0, 0, 50, 500), ('underscore', 1, 50, 0, 500))
    font[0x003D].horizontalComponents = \
        (('equal', 0, 0, 50, 589), ('equal', 1, 50, 0, 589))
    font[0x005E].horizontalComponents = font[0x02C6].horizontalComponents
    font[0x007E].horizontalComponents = font[0x02DC].horizontalComponents

    # Make more arrows stretchable
    # See https://sourceforge.net/p/stixfonts/tracking/70/
    font[0x295A].horizontalComponents = (('uni21BC', 0, 0, 50, 847), ('uni23AF', 1, 50, 50, 315), ('uni22A3', 0, 50, 0, 557))
    font[0x295B].horizontalComponents = (('uni22A2', 0, 0, 50, 557), ('uni23AF', 1, 50, 50, 315), ('uni21C0', 0, 50, 0, 847))
    font[0x295E].horizontalComponents = (('uni21BD', 0, 0, 50, 847), ('uni23AF', 1, 50, 50, 315), ('uni22A3', 0, 50, 0, 557))
    font[0x295F].horizontalComponents = (('uni22A2', 0, 0, 50, 557), ('uni23AF', 1, 50, 50, 315), ('uni21C1', 0, 50, 0, 847))
    font[0x21C1].horizontalComponents = (('uni23AF', 1, 0, 50, 315), ('uni21C1', 0, 50, 0, 847))
    font[0x294E].horizontalComponents = (('uni21BC', 0, 0, 50, 847), ('uni23AF', 1, 50, 50, 315), ('uni21C0', 0, 50, 0, 847))
    font[0x2950].horizontalComponents = (('uni21BD', 0, 0, 50, 847), ('uni23AF', 1, 50, 50, 315), ('uni21C1', 0, 50, 0, 847))
    # FIXME: These are no longer stretchable in STIX1.1.1: U+21A9, U+21AA

    # Set components to stretch integral
    # FIXME: these characters are missing from STIX 1.1.1
    # See https://sourceforge.net/p/stixfonts/tracking/68/
    # font[0x222B].verticalComponents = 0x2321, 0x23AE, 0x2320

    # Set data for lmoustache/rmoustache
    # FIXME: these characters are missing from STIX 1.1.1
    # See https://sourceforge.net/p/stixfonts/tracking/67/
    # font[0x23B0].verticalComponents =
    # font[0x23B1].verticalComponents =

    # Load the list of chars to preserve (MathML operators and mathclass)
    kBaseCharsToPreserve = []
    with open(sys.argv[2], "r") as charList:
        for line in charList:
            codePoints = line[1:len(line)-1].split("-");
            if len(codePoints) > 1:
                # Exclude multiple characters.
                continue

            codePoint = int(codePoints[0], 16)

            # Exclude more non-stretchable characters
            if ((not isStretchable(font, codePoint)) and
                (isBasicLatin(codePoint) or
                 isSpacingModifierLetter(codePoint) or
                 isCombiningDiacriticalMark(codePoint) or
                 isGeneralPunctuation(codePoint) or
                 isCombiningMarkForSymbols(codePoint) or
                 isArrow(codePoint) or
                 isMathematicalSymbol(codePoint) or
                 isMiscellaneousTechnical(codePoint) or
                 isEnclosedAlphanumeric(codePoint) or
                 isGeometricShape(codePoint) or
                 isMiscelleanousSymbol(codePoint) or
                 isDingBats(codePoint) or
                 isMiscelleanousMathSymbol(codePoint) or
                 isSupplementalArrowA(codePoint) or
                 isSupplementalArrowB(codePoint) or
                 isMiscelleanousMathSymbolB(codePoint) or
                 isMathOperatorSupplement(codePoint) or
                 isSupplementalSymbolAndArrow(codePoint) or
                 isHiragana(codePoint) or
                 isBoldMathVariant(codePoint) or
                 isBoldItalicMathVariant(codePoint) or
                 isBoldScriptMathVariant(codePoint) or
                 isBoldFrakturMathVariant(codePoint) or
                 isSansSerifMathVariant(codePoint) or
                 isBoldSansSerifMathVariant(codePoint) or
                 isSansSerifItalicMathVariant(codePoint) or
                 isSansSerifBoldItalicMathVariant(codePoint) or
                 isMonospaceMathVariant(codePoint))):
                    continue

            # Exclude some stretchable characters that are not "stretchy" in the
            # MathML operator dictionary.
            if (codePoint == 0x002F or # Slash
                codePoint == 0x005C or # Backslash
                codePoint == 0x0303 or # Combining tilde
                codePoint == 0x0305 or # Combining overline
                codePoint == 0x030C or # Combining caron
                codePoint == 0x0330 or # Combining tilde below
                codePoint == 0x0332 or # Combining low line
                codePoint == 0x0338 or # Combining long solidius overlay
                codePoint == 0x20D0 or # Combining left harpoon above
                codePoint == 0x20D1 or # Combining ...
                codePoint == 0x20D6 or # Combining ...
                codePoint == 0x20D7 or # Combining ...
                codePoint == 0x20E1 or # Combining ...
                codePoint == 0x20EC or # Combining ...
                codePoint == 0x20ED or # Combining ...
                codePoint == 0x20EE or # Combining ...
                codePoint == 0x20EF or # Combining ...
                codePoint == 0x221B or # Cubic root
                codePoint == 0x221C or # Fourth root
                codePoint == 0x29F8 or # big solidus
                codePoint == 0x29F9): # big reverse solidus
                continue

            # Exclude some LetterLike symbols
            if (codePoint == 0x2129 or
                codePoint == 0x2132 or
                codePoint == 0x2141 or
                codePoint == 0x2142 or
                codePoint == 0x2143 or
                codePoint == 0x2144 or
                codePoint == 0x214B):
                continue

            # The list is probably already sorted, but just in case...
            insortWithoutDuplicate(kBaseCharsToPreserve, codePoint)

    # Determine the list of glyphs to preserve. It is made of glyphs used for
    # characters in kBaseCharsToPreserve.
    kGlyphsToPreserve = []
    for u in kBaseCharsToPreserve:
        if u not in font:
            continue
        glyph = font[u]

        # Preserve the glyph for the base size.
        insortWithoutDuplicate(kGlyphsToPreserve, glyph.glyphname)

        # Preserve glyphs for size variants.
        if glyph.horizontalVariants is not None:
            for glyphname in glyph.horizontalVariants.split(" "):
                insortWithoutDuplicate(kGlyphsToPreserve, glyphname)
        if glyph.verticalVariants is not None:
            for glyphname in glyph.verticalVariants.split(" "):
                insortWithoutDuplicate(kGlyphsToPreserve, glyphname)

        # Preserve glyphs used as components.
        if glyph.horizontalComponents is not None:
            for component in glyph.horizontalComponents:
                insortWithoutDuplicate(kGlyphsToPreserve, component[0])
        if glyph.verticalComponents is not None:
            for component in glyph.verticalComponents:
                insortWithoutDuplicate(kGlyphsToPreserve, component[0])

        # Preserve glyphs used for ssty variants.
        sstyList = getSSTYList(glyph)
        if sstyList is not None:
            for glyphname in sstyList:
                insortWithoutDuplicate(kGlyphsToPreserve, glyphname)

    # Now remove all the glyphs outside kGlyphsToPreserve.
    font.selection.none()
    for glyph in font.glyphs():
        if (not binarySearchHasValue(kGlyphsToPreserve, glyph.glyphname)):
            font.selection.select(("more", None), glyph.glyphname)
    font.clear()

    # Clear more data from the MATH table.
    UNSPECIFIED_TOP_ACCENT=32767
    for glyph in font.glyphs():
        glyph.isExtendedShape = False
        glyph.topaccent = UNSPECIFIED_TOP_ACCENT

    # Generate the subset and close the font.
    font.generate(sys.argv[4])
    font.close()
