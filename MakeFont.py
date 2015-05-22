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

def isBasicLatin(aGlyph):
    return glyph.unicode >= 0 and glyph.unicode <= 0xFFF

def isStretchable(aGlyph):
    return (aGlyph.horizontalVariants is not None or
            aGlyph.horizontalComponents is not None or
            aGlyph.verticalVariants is not None or
            aGlyph.verticalComponents is not None)

if __name__ == "__main__":
    # Check command line argument
    if len(sys.argv) != 4:
        print("usage: python %s input output charList" % sys.argv[0], file=sys.stderr)
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
    with open("metadata.xml", "r") as metadataFile:
        font.woffMetadata = metadataFile.read()

    # Ensure that USE_TYPO_METRICS is set.
    # See https://sourceforge.net/p/stixfonts/tracking/64/
    if font.os2_version and font.os2_version < 4:
        font.os2_version = 4
    font.os2_use_typo_metrics = True

    # Load the list of chars to preserve (MathML operators and mathclass)
    kToPreserve = []
    with open(sys.argv[2], "r") as charList:
        for line in charList:
            codePoints = line[1:len(line)-1].split("-");
            if (len(codePoints) > 1):
                # Let's exclude multiple characters
                continue
            # The list is probably already sorted, but just in case...
            insortWithoutDuplicate(kToPreserve, int(codePoints[0], 16))

    # Remove the Unicode character outside kToPreserve as well as
    # non-stretchable basic latin character.
    font.selection.none()
    for glyph in font.glyphs():
        if glyph.unicode == -1:
            continue
        if ((not binarySearchHasValue(kToPreserve, glyph.unicode)) or
            (isBasicLatin(glyph) and not isStretchable(glyph))):
            font.selection.select(("more", None), glyph.glyphname)
    font.clear()

    # Remove all non-Unicode characters that are not used for operator
    # stretching
    kToPreserve = []
    for glyph in font.glyphs():
        if glyph.horizontalVariants is not None:
            for glyphname in glyph.horizontalVariants.split(" "):
                insortWithoutDuplicate(kToPreserve, glyphname)
        if glyph.verticalVariants is not None:
            for glyphname in glyph.verticalVariants.split(" "):
                insortWithoutDuplicate(kToPreserve, glyphname)
        if glyph.horizontalComponents is not None:
            for component in glyph.horizontalComponents:
                insortWithoutDuplicate(kToPreserve, component[0])
        if glyph.verticalComponents is not None:
            for component in glyph.verticalComponents:
                insortWithoutDuplicate(kToPreserve, component[0])
    font.selection.none()
    for glyph in font.glyphs():
        if (glyph.unicode == -1 and
            (not binarySearchHasValue(kToPreserve, glyph.glyphname))):
            font.selection.select(("more", None), glyph.glyphname)
    font.clear()

    # Generate the subset and close the font.
    font.generate(sys.argv[3])
    font.close()
