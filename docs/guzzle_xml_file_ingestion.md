---
id: guzzle_xml_file_ingestion
title: Using Guzzle Ingestion Module for Ingesting XML File
sidebar_label: Using Guzzle Ingestion Module for Ingesting XML File
---

Guzzle supports XML data ingestion. Below is example of XML file `Source` configuration for an `Activity` in Guzzle `Ingestion` module job, if source is a nested XML file or a nested XML file with Array.

## Root Tag, Row Tag and Clean Column Names

In here, below sample XML has root tag as `ns0:OTA_HotelProductRS`, row tag as `ns0:HotelProducts`. Here column cleansing would also be required before loading target as tag name contains colon ( : ). If you enable `Clean Column Names` property then Guzzle would auto convert these colons ( : ) and also spaces to underscore ( _ ), as appropriate.

## Nested XML File

Data ingestion from nested XML file is fully supported by Guzzle. Here in below example, there are two rows in the given XML sample.

**Sample nested XML:**

```xml
<?xml version='1.0' encoding='UTF-8'?>
<ns0:OTA_HotelProductRS xmlns:ns0="http://www.opentravel.org/OTA/2003/05">
    <ns0:HotelProducts HotelName="Ascott Orchard Singapore" HotelCode="SG74">
        <ns0:RoomType RoomTypeCode="0EXES AOS" RoomTypeName="Accomm" RoomTypeGroup="0BRM|Studio">
            <ns0:Descriptions>
                <ns0:Description>
                    <ns0:Text>Studio Executive Suite</ns0:Text>
                </ns0:Description>
                <ns0:RoomTypeRefs>
                    <ns0:RoomTypeRef>
                        <ns0:Description RoomTypeCode="0EXES" RoomTypeCodeContext="CustomEDP" InActive="false" Interconnecting="false"/>
                    </ns0:RoomTypeRef>
                </ns0:RoomTypeRefs>
            </ns0:Descriptions>
        </ns0:RoomType>
	</ns0:HotelProducts>
	<ns0:HotelProducts HotelName="Ascott Orchard Singapore" HotelCode="SG74">
        <ns0:RoomType RoomTypeCode="0PRES AOS" RoomTypeName="Accomm" RoomTypeGroup="0BRM|Studio">
            <ns0:Descriptions>
                <ns0:Description>
                    <ns0:Text>Studio Premier Suite</ns0:Text>
                </ns0:Description>
                <ns0:RoomTypeRefs>
                    <ns0:RoomTypeRef>
                        <ns0:Description RoomTypeCode="0PRES" RoomTypeCodeContext="CustomEDP" InActive="false" Interconnecting="false"/>
                    </ns0:RoomTypeRef>
                </ns0:RoomTypeRefs>
            </ns0:Descriptions>
        </ns0:RoomType>
    </ns0:HotelProducts>
</ns0:OTA_HotelProductRS>
```

### Sample Guzzle Activity `Source` configuration to read above nested XML file,

**Source Configuration Settings:**

![Activity_Config_For_XML_Ingestion1](https://github.com/justanalytics/guzzle-docs/blob/guzzle-doc-update-chandra/website/static/img/docs/Activity_Config_For_XML_Ingestion1.PNG)

**Column Mapping:**

![Activity_Config_For_XML_Ingestion2](https://github.com/justanalytics/guzzle-docs/blob/guzzle-doc-update-chandra/website/static/img/docs/Activity_Config_For_XML_Ingestion2.PNG)

## Nested XML File with Array

Data ingestion from nested XML file with Array is also supported to an extend by Guzzle as within an Array all element values will be read comma separated and mapped to single column in target table. Here in below example, column `RoomTypeCode` would be populated like Array with comma separated values as there are two Array elements in target table since `ns0:RoomTypes` is an array of `ns0:RoomType`.

**Sample nested XML with Array:**

```xml
<?xml version='1.0' encoding='UTF-8'?>
<ns0:OTA_HotelProductRS xmlns:ns0="http://www.opentravel.org/OTA/2003/05">
    <ns0:HotelProducts HotelName="Ascott Orchard Singapore" HotelCode="SG74">
        <ns0:HotelProduct>
            <ns0:RoomTypes>
                <ns0:RoomType RoomTypeCode="0EXES AOS" RoomTypeName="Accomm" RoomTypeGroup="0BRM|Studio">
                    <ns0:Descriptions>
                        <ns0:Description>
                            <ns0:Text>Studio Executive Suite</ns0:Text>
                        </ns0:Description>
                        <ns0:RoomTypeRefs>
                            <ns0:RoomTypeRef>
                                <ns0:Description RoomTypeCode="0EXES" RoomTypeCodeContext="CustomEDP" InActive="false" Interconnecting="false"/>
                            </ns0:RoomTypeRef>
                        </ns0:RoomTypeRefs>
                    </ns0:Descriptions>
                </ns0:RoomType>
                <ns0:RoomType RoomTypeCode="0PRES AOS" RoomTypeName="Accomm" RoomTypeGroup="0BRM|Studio">
                    <ns0:Descriptions>
                        <ns0:Description>
                            <ns0:Text>Studio Premier Suite</ns0:Text>
                        </ns0:Description>
                        <ns0:RoomTypeRefs>
                            <ns0:RoomTypeRef>
                                <ns0:Description RoomTypeCode="0PRES" RoomTypeCodeContext="CustomEDP" InActive="false" Interconnecting="false"/>
                            </ns0:RoomTypeRef>
                        </ns0:RoomTypeRefs>
                    </ns0:Descriptions>
                </ns0:RoomType>
            </ns0:RoomTypes>
        </ns0:HotelProduct>
    </ns0:HotelProducts>
</ns0:OTA_HotelProductRS>
```

### Sample Guzzle Activity `Source` configuration to read above nested XML file with Array,

**Source Configuration Settings:**

![Activity_Config_For_XML_Array_Ingestion1](https://github.com/justanalytics/guzzle-docs/blob/guzzle-doc-update-chandra/website/static/img/docs/Activity_Config_For_XML_Array_Ingestion1.PNG)

**Column Mapping:**

![Activity_Config_For_XML_Array_Ingestion2](https://github.com/justanalytics/guzzle-docs/blob/guzzle-doc-update-chandra/website/static/img/docs/Activity_Config_For_XML_Array_Ingestion2.PNG)
