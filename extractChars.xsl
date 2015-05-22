<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- This Source Code Form is subject to the terms of the Mozilla Public
   - License, v. 2.0. If a copy of the MPL was not distributed with this
   - file, You can obtain one at http://mozilla.org/MPL/2.0/. -->
  <xsl:strip-space elements="*"/>
  <xsl:output method="text"/>

  <xsl:template match="charlist">
    <!-- We extract the list of characters from unicode.xml -->
    <xsl:apply-templates select="character"/>
  </xsl:template>

  <xsl:template match="character">
    <!-- Keep MathML operators and characters with a mathclass -->
    <xsl:if test="operator-dictionary or unicodedata/@mathclass">
      <xsl:value-of select="@id"/>
      <xsl:text>&#xa;</xsl:text>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
