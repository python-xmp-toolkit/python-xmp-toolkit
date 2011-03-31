# -*- coding: utf8 -*-
# TODO: This is copied from Adobe XMP Toolkit - find out what the license should say about it. The same applies to the sample files.

NS1 = "ns:test1/"
NS2 = "ns:test2/"

RDFCoverage = """<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kRDFCoverage' xmlns:ns1='ns:test1/' xmlns:ns2='ns:test2/'>

    <ns1:SimpleProp1>Simple1 value</ns1:SimpleProp1>
    <ns1:SimpleProp2 xml:lang='x-default'>Simple2 value</ns1:SimpleProp2>

    <ns1:ArrayProp1>
      <rdf:Bag>
        <rdf:li>Item1.1 value</rdf:li>
        <rdf:li>Item1.2 value</rdf:li>
      </rdf:Bag>
    </ns1:ArrayProp1>

    <ns1:ArrayProp2>
      <rdf:Alt>
        <rdf:li xml:lang='x-one'>Item2.1 value</rdf:li>
        <rdf:li xml:lang='x-two'>Item2.2 value</rdf:li>
      </rdf:Alt>
    </ns1:ArrayProp2>

    <ns1:ArrayProp3>
      <rdf:Alt>
        <rdf:li xml:lang='x-one'>Item3.1 value</rdf:li>
        <rdf:li>Item3.2 value</rdf:li>
      </rdf:Alt>
    </ns1:ArrayProp3>

    <ns1:ArrayProp4>
      <rdf:Alt>
        <rdf:li>Item4.1 value</rdf:li>
        <rdf:li xml:lang='x-two'>Item4.2 value</rdf:li>
      </rdf:Alt>
    </ns1:ArrayProp4>

    <ns1:ArrayProp5>
      <rdf:Alt>
        <rdf:li xml:lang='x-xxx'>Item5.1 value</rdf:li>
        <rdf:li xml:lang='x-xxx'>Item5.2 value</rdf:li>
      </rdf:Alt>
    </ns1:ArrayProp5>

    <ns1:StructProp rdf:parseType='Resource'>
      <ns2:Field1>Field1 value</ns2:Field1>
      <ns2:Field2>Field2 value</ns2:Field2>
    </ns1:StructProp>

    <ns1:QualProp1 rdf:parseType='Resource'>
      <rdf:value>Prop value</rdf:value>
      <ns2:Qual>Qual value</ns2:Qual>
    </ns1:QualProp1>

    <ns1:QualProp2 rdf:parseType='Resource'>
      <rdf:value xml:lang='x-default'>Prop value</rdf:value>
      <ns2:Qual>Qual value</ns2:Qual>
    </ns1:QualProp2>

    <!-- NOTE: QualProp3 is not quite kosher. Normally a qualifier on a struct is attached to the -->
    <!-- struct node in the XMP tree, and the same for an array. See QualProp4 and QualProp5. But -->
    <!-- for the pseudo-struct of a qualified simple property there is no final struct node that  -->
    <!-- can own the qualifier. Instead the qualifier is attached to the value. The alternative   -->
    <!-- of attaching the qualifier to the value and all other qualifiers is not compelling. This -->
    <!-- issue only arises for xml:lang, it is the only qualifier that RDF has as an attribute.   -->

    <ns1:QualProp3 xml:lang='x-default' rdf:parseType='Resource'>
      <rdf:value>Prop value</rdf:value>
      <ns2:Qual>Qual value</ns2:Qual>
    </ns1:QualProp3>

    <ns1:QualProp4 xml:lang='x-default' rdf:parseType='Resource'>
      <ns2:Field1>Field1 value</ns2:Field1>
      <ns2:Field2>Field2 value</ns2:Field2>
    </ns1:QualProp4>

    <ns1:QualProp5 xml:lang='x-default'>
      <rdf:Bag>
        <rdf:li>Item1.1 value</rdf:li>
        <rdf:li>Item1.2 value</rdf:li>
      </rdf:Bag>
    </ns1:QualProp5>

    <ns2:NestedStructProp rdf:parseType='Resource'>
      <ns1:Outer rdf:parseType='Resource'>
        <ns1:Middle rdf:parseType='Resource'>
          <ns1:Inner rdf:parseType='Resource'>
            <ns1:Field1>Field1 value</ns1:Field1>
            <ns2:Field2>Field2 value</ns2:Field2>
          </ns1:Inner>
        </ns1:Middle>
      </ns1:Outer>
    </ns2:NestedStructProp>

  </rdf:Description>
</rdf:RDF>"""

SimpleRDF = """<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kSimpleRDF' xmlns:ns1='ns:test1/' xmlns:ns2='ns:test2/'>

    <ns1:SimpleProp>Simple value</ns1:SimpleProp>

    <ns1:ArrayProp>
      <rdf:Bag>
        <rdf:li>Item1 value</rdf:li>
        <rdf:li>Item2 value</rdf:li>
      </rdf:Bag>
    </ns1:ArrayProp>

    <ns1:StructProp rdf:parseType='Resource'>
      <ns2:Field1>Field1 value</ns2:Field1>
      <ns2:Field2>Field2 value</ns2:Field2>
    </ns1:StructProp>

    <ns1:QualProp rdf:parseType='Resource'>
      <rdf:value>Prop value</rdf:value>
      <ns2:Qual>Qual value</ns2:Qual>
    </ns1:QualProp>

    <ns1:AltTextProp>
      <rdf:Alt>
        <rdf:li xml:lang='x-one'>x-one value</rdf:li>
        <rdf:li xml:lang='x-two'>x-two value</rdf:li>
      </rdf:Alt>
    </ns1:AltTextProp>

    <ns1:ArrayOfStructProp>
      <rdf:Bag>
        <rdf:li rdf:parseType='Resource'>
          <ns2:Field1>Item-1</ns2:Field1>
          <ns2:Field2>Field 1.2 value</ns2:Field2>
        </rdf:li>
        <rdf:li rdf:parseType='Resource'>
          <ns2:Field1>Item-2</ns2:Field1>
          <ns2:Field2>Field 2.2 value</ns2:Field2>
        </rdf:li>
      </rdf:Bag>
    </ns1:ArrayOfStructProp>

  </rdf:Description>
</rdf:RDF>"""

NamespaceRDF = """<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kNamespaceRDF' xmlns:ns1='ns:test1/'>

    <ns1:NestedStructProp rdf:parseType='Resource'>
      <ns2:Outer rdf:parseType='Resource' xmlns:ns2='ns:test2/' xmlns:ns3='ns:test3/'>
        <ns3:Middle rdf:parseType='Resource' xmlns:ns4='ns:test4/'>
          <ns4:Inner rdf:parseType='Resource' xmlns:ns5='ns:test5/' xmlns:ns6='ns:test6/'>
            <ns5:Field1>Field1 value</ns5:Field1>
            <ns6:Field2>Field2 value</ns6:Field2>
          </ns4:Inner>
        </ns3:Middle>
      </ns2:Outer>
    </ns1:NestedStructProp>

  </rdf:Description>
</rdf:RDF>"""

XMPMetaRDF = """<x:Outermost xmlns:x='adobe:ns:meta/'>

<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kBogusLeadingRDF' xmlns:ns1='ns:test1/'>
    <ns1:BogusLeadingProp>bogus packet</ns1:BogusLeadingProp>
  </rdf:Description>
</rdf:RDF>

<x:xmpmeta>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kXMPMetaRDF' xmlns:ns1='ns:test1/'>
    <ns1:XMPMetaProp>xmpmeta packet</ns1:XMPMetaProp>
  </rdf:Description>
</rdf:RDF>
</x:xmpmeta>

<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kBogusTrailingRDF' xmlns:ns1='ns:test1/'>
    <ns1:BogusTrailingProp>bogus packet</ns1:BogusTrailingProp>
  </rdf:Description>
</rdf:RDF>

</x:Outermost>"""

NewlineRDF = """<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kNewlineRDF' xmlns:ns1='ns:test1/'>

    <ns1:HasCR>ASCII &#xD; CR</ns1:HasCR>
    <ns1:HasLF>ASCII &#xA; LF</ns1:HasLF>
    <ns1:HasCRLF>ASCII &#xD;&#xA; CRLF</ns1:HasCRLF>

  </rdf:Description>
</rdf:RDF>"""

InconsistentRDF = """<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kInconsistentRDF'
                   xmlns:pdf='http://ns.adobe.com/pdf/1.3/'
                   xmlns:xmp='http://ns.adobe.com/xap/1.0/'
                   xmlns:dc='http://purl.org/dc/elements/1.1/'>

    <pdf:Author>PDF Author</pdf:Author>
    <xmp:Author>XMP Author</xmp:Author>

    <xmp:Authors>
      <rdf:Seq>
        <rdf:li>XMP Authors [1]</rdf:li>
      </rdf:Seq>
    </xmp:Authors>

    <dc:creator>
      <rdf:Seq>
        <rdf:li>DC Creator [1]</rdf:li>
      </rdf:Seq>
    </dc:creator>

  </rdf:Description>
</rdf:RDF>"""

DateTimeRDF = """<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='Test:XMPCoreCoverage/kDateTimeRDF' xmlns:ns1='ns:test1/'>

    <ns1:Date1>2003</ns1:Date1>
    <ns1:Date2>2003-12</ns1:Date2>
    <ns1:Date3>2003-12-31</ns1:Date3>

    <ns1:Date4>2003-12-31T12:34Z</ns1:Date4>
    <ns1:Date5>2003-12-31T12:34:56Z</ns1:Date5>

    <ns1:Date6>2003-12-31T12:34:56.001Z</ns1:Date6>
    <ns1:Date7>2003-12-31T12:34:56.000000001Z</ns1:Date7>

    <ns1:Date8>2003-12-31T10:04:56-02:30</ns1:Date8>
    <ns1:Date9>2003-12-31T15:49:56+03:15</ns1:Date9>

  </rdf:Description>
</rdf:RDF>"""


ShorthandRDF = """
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'> 
<rdf:Description about='' xmlns:tiff='http://ns.adobe.com/tiff/1.0' 
tiff:Make='Canon' 
tiff:Model='Canon PowerShot S300' 
tiff:Orientation='1' 
tiff:XResolution='180/1' 
tiff:YResolution='180/1' 
tiff:ResolutionUnit='2' 
tiff:DateTime='2001-07-25T20:18:27-07:00' 
tiff:YCbCrPositioning='1'> 
</rdf:Description>
</rdf:RDF>
"""

LongTextProperty = """
<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Exempi + XMP Core 4.4.0">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dc="http://purl.org/dc/elements/1.1/">
   <dc:subject>
    <rdf:Bag>
     <rdf:li>XMP</rdf:li>
     <rdf:li>Blue Square</rdf:li>
     <rdf:li>test file</rdf:li>
     <rdf:li>Photoshop</rdf:li>
     <rdf:li>.psd</rdf:li>
    </rdf:Bag>
   </dc:subject>
   <dc:description>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">XMPFiles BlueSquare test file, created in Photoshop CS2, saved as .psd, .jpg, and .tif.</rdf:li>
    </rdf:Alt>
   </dc:description>
   <dc:title>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">Blue Square Test File - .psd</rdf:li>
    </rdf:Alt>
   </dc:title>
   <dc:format>image/tiff</dc:format>
  </rdf:Description>
  <rdf:Description rdf:about=""
    xmlns:xmp="http://ns.adobe.com/xap/1.0/">
   <xmp:ModifyDate>2010-02-16T17:53:30+01:00</xmp:ModifyDate>
   <xmp:CreatorTool>Adobe Photoshop CS4 Macintosh</xmp:CreatorTool>
   <xmp:MetadataDate>2010-02-16T17:53:30+01:00</xmp:MetadataDate>
   <xmp:CreateDate>2005-09-07T15:01:43-07:00</xmp:CreateDate>
  </rdf:Description>
  <rdf:Description rdf:about=""
    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
    xmlns:stRef="http://ns.adobe.com/xap/1.0/sType/ResourceRef#"
    xmlns:stEvt="http://ns.adobe.com/xap/1.0/sType/ResourceEvent#">
   <xmpMM:DerivedFrom rdf:parseType="Resource">
    <stRef:instanceID>xmp.iid:F87F1174072068119D2BDE2E500230D1</stRef:instanceID>
    <stRef:documentID>uuid:9A3B7F4E214211DAB6308A7391270C13</stRef:documentID>
    <stRef:originalDocumentID>uuid:9A3B7F4E214211DAB6308A7391270C13</stRef:originalDocumentID>
   </xmpMM:DerivedFrom>
   <xmpMM:History>
    <rdf:Seq>
     <rdf:li rdf:parseType="Resource">
      <stEvt:action>saved</stEvt:action>
      <stEvt:instanceID>xmp.iid:F77F1174072068119D2BDE2E500230D1</stEvt:instanceID>
      <stEvt:when>2010-02-16T17:46:22+01:00</stEvt:when>
      <stEvt:softwareAgent>Adobe Photoshop CS4 Macintosh</stEvt:softwareAgent>
      <stEvt:changed>/</stEvt:changed>
     </rdf:li>
     <rdf:li rdf:parseType="Resource">
      <stEvt:action>saved</stEvt:action>
      <stEvt:instanceID>xmp.iid:F87F1174072068119D2BDE2E500230D1</stEvt:instanceID>
      <stEvt:when>2010-02-16T17:53:30+01:00</stEvt:when>
      <stEvt:softwareAgent>Adobe Photoshop CS4 Macintosh</stEvt:softwareAgent>
      <stEvt:changed>/</stEvt:changed>
     </rdf:li>
     <rdf:li rdf:parseType="Resource">
      <stEvt:action>converted</stEvt:action>
      <stEvt:parameters>from application/vnd.adobe.photoshop to image/tiff</stEvt:parameters>
     </rdf:li>
     <rdf:li rdf:parseType="Resource">
      <stEvt:action>derived</stEvt:action>
      <stEvt:parameters>converted from application/vnd.adobe.photoshop to image/tiff</stEvt:parameters>
     </rdf:li>
     <rdf:li rdf:parseType="Resource">
      <stEvt:action>saved</stEvt:action>
      <stEvt:instanceID>xmp.iid:F97F1174072068119D2BDE2E500230D1</stEvt:instanceID>
      <stEvt:when>2010-02-16T17:53:30+01:00</stEvt:when>
      <stEvt:softwareAgent>Adobe Photoshop CS4 Macintosh</stEvt:softwareAgent>
      <stEvt:changed>/</stEvt:changed>
     </rdf:li>
    </rdf:Seq>
   </xmpMM:History>
   <xmpMM:OriginalDocumentID>uuid:9A3B7F4E214211DAB6308A7391270C13</xmpMM:OriginalDocumentID>
   <xmpMM:InstanceID>xmp.iid:F97F1174072068119D2BDE2E500230D1</xmpMM:InstanceID>
   <xmpMM:DocumentID>uuid:9A3B7F4E214211DAB6308A7391270C13</xmpMM:DocumentID>
  </rdf:Description>
  <rdf:Description rdf:about=""
    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">
   <photoshop:Headline>The Crab Nebula is the shattered remnant of a massive star that ended its life in a massive supernova explosion. Nearly a thousand years old, the supernova was noted in the constellation of Taurus by Chinese astronomers in the year 1054 AD. The Crab Nebula is the shattered remnant of a massive star that ended its life in a massive supernova explosion. Nearly a thousand years old, the supernova was noted in the constellation of Taurus by Chinese =END=</photoshop:Headline>
   <photoshop:ICCProfile>sRGB IEC61966-2.1</photoshop:ICCProfile>
   <photoshop:ColorMode>3</photoshop:ColorMode>
  </rdf:Description>
  <rdf:Description rdf:about=""
    xmlns:tiff="http://ns.adobe.com/tiff/1.0/">
   <tiff:ResolutionUnit>2</tiff:ResolutionUnit>
   <tiff:YResolution>720000/10000</tiff:YResolution>
   <tiff:XResolution>720000/10000</tiff:XResolution>
   <tiff:PlanarConfiguration>1</tiff:PlanarConfiguration>
   <tiff:SamplesPerPixel>3</tiff:SamplesPerPixel>
   <tiff:Orientation>1</tiff:Orientation>
   <tiff:PhotometricInterpretation>2</tiff:PhotometricInterpretation>
   <tiff:Compression>5</tiff:Compression>
   <tiff:BitsPerSample>
    <rdf:Seq>
     <rdf:li>8</rdf:li>
     <rdf:li>8</rdf:li>
     <rdf:li>8</rdf:li>
    </rdf:Seq>
   </tiff:BitsPerSample>
   <tiff:ImageLength>216</tiff:ImageLength>
   <tiff:ImageWidth>360</tiff:ImageWidth>
   <tiff:NativeDigest>256,257,258,259,262,274,277,284,530,531,282,283,296,301,318,319,529,532,306,270,271,272,305,315,33432;46A23B4E8F942E0E03D60BC6E6769870</tiff:NativeDigest>
  </rdf:Description>
  <rdf:Description rdf:about=""
    xmlns:exif="http://ns.adobe.com/exif/1.0/">
   <exif:PixelYDimension>216</exif:PixelYDimension>
   <exif:PixelXDimension>360</exif:PixelXDimension>
   <exif:ColorSpace>1</exif:ColorSpace>
   <exif:NativeDigest>36864,40960,40961,37121,37122,40962,40963,37510,40964,36867,36868,33434,33437,34850,34852,34855,34856,37377,37378,37379,37380,37381,37382,37383,37384,37385,37386,37396,41483,41484,41486,41487,41488,41492,41493,41495,41728,41729,41730,41985,41986,41987,41988,41989,41990,41991,41992,41993,41994,41995,41996,42016,0,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,22,23,24,25,26,27,28,30;76DBD9F0A5E7ED8F62B4CE8EFA6478B4</exif:NativeDigest>
  </rdf:Description>
  <rdf:Description rdf:about=""
    xmlns:avm="http://www.communicatingastronomy.org/avm/1.0/">
   <avm:Spectral.Band>
    <rdf:Seq/>
   </avm:Spectral.Band>
   <avm:Spectral.ColorAssignment>
    <rdf:Seq/>
   </avm:Spectral.ColorAssignment>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                           
<?xpacket end="w"?>
"""