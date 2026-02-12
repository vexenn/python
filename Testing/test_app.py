import requests

api_url = 'NOAA_API_ENDPOINT'  # Replace with the actual API endpoint

headers = {
    'User-Agent': 'MyPythonWeather/1.0 (vexenn897@gmail.com)'
}

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)  # Process and display your data here
else:
    print(f'Error: {response.status_code}')

# Current Weather Observations
{
  "@context": [
    "string"
  ],
  "id": "string",
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      0,
      0
    ],
    "bbox": [
      0,
      0,
      0,
      0
    ]
  },
  "properties": {
    "@context": [
      "string"
    ],
    "geometry": "string",
    "@id": "string",
    "@type": "wx:ObservationStation",
    "elevation": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "uc:a^hG-t/GSa0]pDp7rm3,#R]UXi~Z*7wu[:|3%Dw-r?@Z~V.gB`",
      "qualityControl": "Z"
    },
    "station": "string",
    "stationId": "string",
    "stationName": "string",
    "timestamp": "2026-02-12T09:03:06.174Z",
    "rawMessage": "string",
    "textDescription": "string",
    "presentWeather": [
      {
        "intensity": "light",
        "modifier": "patches",
        "weather": "fog_mist",
        "rawString": "string",
        "inVicinity": true
      }
    ],
    "temperature": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "MUkHMyEKGqU/oa*\\:y +",
      "qualityControl": "Z"
    },
    "dewpoint": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "wmo:-<`e8rOGBms(_JVL]W:lsLv!C9a1s_Fv9~{yH/8O? qz1\\M3X+PDUyks5;XMCxhY-*7a;)V\\|jU#?B\"YBE\"xyZ@Ub5x^5]",
      "qualityControl": "Z"
    },
    "windDirection": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "Ozqz{!q;vFZ&$Y+xkm7Mydara6Uw^n&$ko!4!#tFe1cUp5Pf;ZMrK",
      "qualityControl": "Z"
    },
    "windSpeed": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "\\(+\",n;rR\"N}>_^`2w@gC(62ach,Aap#fJWGt;,ySp.n=I-yaUxj50ZWmd[{]FjykJc`Y{Sc</M5\\.]+1H/v2eDnunlFQrS=[",
      "qualityControl": "Z"
    },
    "windGust": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "nwsUnit:qL@",
      "qualityControl": "Z"
    },
    "barometricPressure": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "mIF?]iC\\e264OuYxz.K@%FM3k/-@.5n!yn(.|XHNE_U2'!^;%tY-*s}Fh\"wAnv]]^@",
      "qualityControl": "Z"
    },
    "seaLevelPressure": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": ">[qj3/\\[JPmT",
      "qualityControl": "Z"
    },
    "visibility": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "wmoUnit:4vuOGLjj5kFByx\"fWQ)F\\\\X~P]d)Vo}q;8krNAkt|iLYuW_OV",
      "qualityControl": "Z"
    },
    "maxTemperatureLast24Hours": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "nwsUnit:k ja}<&;_kMz'RP{ff;NV:hko#dqhyk_6p8$5",
      "qualityControl": "Z"
    },
    "minTemperatureLast24Hours": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "wmo:(|Uw&MN&r",
      "qualityControl": "Z"
    },
    "precipitationLastHour": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "X3@[^xeM5-AI&cy=uW)60Rfr7}:0~ tG;e[ _c|xi$aF}3nN^nB:G<W,JK;PCwDLJ[TF4ko$VRP6&N>k\\,r`GjlZx0iZEZg/FO",
      "qualityControl": "Z"
    },
    "precipitationLast3Hours": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "A;NzK'_]~As*U-7",
      "qualityControl": "Z"
    },
    "precipitationLast6Hours": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "nwsUnit:Be F`h6w=Yn_0RV7 cZw)~%E<iHy{6Yk`",
      "qualityControl": "Z"
    },
    "relativeHumidity": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "z:sl5gX8?r_9Rbf8[",
      "qualityControl": "Z"
    },
    "windChill": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "wmo:vzW+:)0d6l_.th}42?kC>>B&-Tj^ET\\j%hplL@F]k%SpA[",
      "qualityControl": "Z"
    },
    "heatIndex": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "zxp]bmZ`u*d?6K?'^@_}iw@2pbM]U~k9cJj<1p$xx3~$y/}S3%>)xv[OJ;\\",
      "qualityControl": "Z"
    },
    "cloudLayers": [
      {
        "base": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "2b~7c.S6:p6@S,<xG\"\\t]YUzH.@Or2h?D^$^}\\*M%>C",
          "qualityControl": "Z"
        },
        "amount": "OVC"
      }
    ]
  }
}

# /gridpoints/{wfo}/{x},{y}/forecast

{
  "@context": [
    "string"
  ],
  "id": "string",
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      0,
      0
    ],
    "bbox": [
      0,
      0,
      0,
      0
    ]
  },
  "properties": {
    "@context": [
      "string"
    ],
    "geometry": "string",
    "units": "us",
    "forecastGenerator": "string",
    "generatedAt": "2026-02-12T09:05:24.357Z",
    "updateTime": "2026-02-12T09:05:24.357Z",
    "validTimes": "2007-03-01T13:00:00Z/2008-05-11T15:30:00Z",
    "elevation": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "H,5/\"tPA{kFqP4aV?2DSA41.\">RXHCGC*UI,@\"0q$wX?4{dXuW^1g$,_zzzLTU4YR",
      "qualityControl": "Z"
    },
    "periods": [
      {
        "number": 1,
        "name": "Tuesday Night",
        "startTime": "2026-02-12T09:05:24.358Z",
        "endTime": "2026-02-12T09:05:24.358Z",
        "isDaytime": true,
        "temperature": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "wmoUnit:z7Db-\"uvN<)8^I/2T|oZ[D(^Zb}p5z?K1vSW!2pV-V)gzOK+Aps?F<Bp+Q%2p1xEI.>^-}\\`X*NfR0^RMZWK/o}&c",
          "qualityControl": "Z"
        },
        "temperatureTrend": "rising",
        "probabilityOfPrecipitation": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "wmo:g0H^|.0{vpwgXE ",
          "qualityControl": "Z"
        },
        "windSpeed": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "sOXRYv/Jz+!]Yv`6Su#a'\"l5&8TC,Zo",
          "qualityControl": "Z"
        },
        "windGust": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "wmoUnit:uR&8",
          "qualityControl": "Z"
        },
        "windDirection": "N",
        "shortForecast": "string",
        "detailedForecast": "string"
      }
    ]
  }
}

# grid points forecast error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# grid points hourly

{
  "@context": [
    "string"
  ],
  "id": "string",
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      0,
      0
    ],
    "bbox": [
      0,
      0,
      0,
      0
    ]
  },
  "properties": {
    "@context": [
      "string"
    ],
    "geometry": "string",
    "units": "us",
    "forecastGenerator": "string",
    "generatedAt": "2026-02-12T09:15:37.352Z",
    "updateTime": "2026-02-12T09:15:37.352Z",
    "validTimes": "2007-03-01T13:00:00Z/2008-05-11T15:30:00Z",
    "elevation": {
      "value": 0,
      "maxValue": 0,
      "minValue": 0,
      "unitCode": "wmo:J|Fn&nEdcxZSyE3 C9#2jKAB?p8t:VojxZTHjaZ.|i^s}+Qgj-S$cP3|3MlR(-%`\"",
      "qualityControl": "Z"
    },
    "periods": [
      {
        "number": 1,
        "name": "Tuesday Night",
        "startTime": "2026-02-12T09:15:37.352Z",
        "endTime": "2026-02-12T09:15:37.352Z",
        "isDaytime": true,
        "temperature": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "wmoUnit:BKS)Ue4DY,;=GSlIZ(K#@cX+_mqFn++PvrhAmq*ei[H(wOQ;*yNjmG*2DeXj M$pyd-{wmGzmgwd18(H",
          "qualityControl": "Z"
        },
        "temperatureTrend": "rising",
        "probabilityOfPrecipitation": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "qn20qV^TQhg170=PK2dlDx5Cs55{IDv%b0?2i;V-{[4m*\\RDAn~)s8.rB{6.&%B(o.h<x6h<`y8' 9\"1.z2fr",
          "qualityControl": "Z"
        },
        "dewpoint": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "O,Ro>X\\#%gE]Mp#}FOLW#UKx,\"#8-N+G.!<+^;&c[EaVPNqa0.mfHUQV-T.^<OnbN\\h{_8Em",
          "qualityControl": "Z"
        },
        "relativeHumidity": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "l*X<!-s{ oRaFFx%BiMDnbaWeo]1IgJwb%YuX` ;IqEKS,SWCQY)y}DYiI|_Y3zYEZdtIQ=;S7[j;}8yMxnNN@7Ko",
          "qualityControl": "Z"
        },
        "windSpeed": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "wmoUnit:h>chjODh;<`",
          "qualityControl": "Z"
        },
        "windGust": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "wmo:[62]PV-I-=|jY@>UUwj!K\\u0[i2-:Dk0/W[P#0o^!tD_G'b%:tA$]\";{DZ#BdFJ'RxK^]QfKV",
          "qualityControl": "Z"
        },
        "windDirection": "N",
        "shortForecast": "string",
        "detailedForecast": "string"
      }
    ]
  }
}

# grid points hourly error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# alerts

{
  "@context": [
    "string"
  ],
  "type": "FeatureCollection",
  "features": [
    {
      "@context": [
        "string"
      ],
      "id": "string",
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ],
        "bbox": [
          0,
          0,
          0,
          0
        ]
      },
      "properties": {
        "id": "string",
        "areaDesc": "string",
        "geocode": {
          "UGC": [
            "UTC100"
          ],
          "SAME": [
            "011452"
          ]
        },
        "affectedZones": [
          "string"
        ],
        "references": [
          {
            "@id": "string",
            "identifier": "string",
            "sender": "string",
            "sent": "2026-02-12T09:07:30.128Z"
          }
        ],
        "sent": "2026-02-12T09:07:30.128Z",
        "effective": "2026-02-12T09:07:30.128Z",
        "onset": "2026-02-12T09:07:30.128Z",
        "expires": "2026-02-12T09:07:30.128Z",
        "ends": "2026-02-12T09:07:30.128Z",
        "status": "Actual",
        "messageType": "Alert",
        "category": "Met",
        "severity": "Extreme",
        "certainty": "Observed",
        "urgency": "Immediate",
        "event": "string",
        "sender": "string",
        "senderName": "string",
        "headline": "string",
        "description": "string",
        "instruction": "string",
        "response": "Shelter",
        "parameters": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "scope": "Public",
        "code": "string",
        "language": "string",
        "web": "string",
        "eventCode": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        }
      }
    }
  ],
  "title": "string",
  "updated": "2026-02-12T09:07:30.128Z",
  "pagination": {
    "next": "string"
  }
}

# alerts error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# alerts active

{
  "@context": [
    "string"
  ],
  "type": "FeatureCollection",
  "features": [
    {
      "@context": [
        "string"
      ],
      "id": "string",
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ],
        "bbox": [
          0,
          0,
          0,
          0
        ]
      },
      "properties": {
        "id": "string",
        "areaDesc": "string",
        "geocode": {
          "UGC": [
            "IDC909"
          ],
          "SAME": [
            "789074"
          ]
        },
        "affectedZones": [
          "string"
        ],
        "references": [
          {
            "@id": "string",
            "identifier": "string",
            "sender": "string",
            "sent": "2026-02-12T09:08:05.671Z"
          }
        ],
        "sent": "2026-02-12T09:08:05.671Z",
        "effective": "2026-02-12T09:08:05.671Z",
        "onset": "2026-02-12T09:08:05.671Z",
        "expires": "2026-02-12T09:08:05.671Z",
        "ends": "2026-02-12T09:08:05.671Z",
        "status": "Actual",
        "messageType": "Alert",
        "category": "Met",
        "severity": "Extreme",
        "certainty": "Observed",
        "urgency": "Immediate",
        "event": "string",
        "sender": "string",
        "senderName": "string",
        "headline": "string",
        "description": "string",
        "instruction": "string",
        "response": "Shelter",
        "parameters": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "scope": "Public",
        "code": "string",
        "language": "string",
        "web": "string",
        "eventCode": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        }
      }
    }
  ],
  "title": "string",
  "updated": "2026-02-12T09:08:05.671Z",
  "pagination": {
    "next": "string"
  }
}

# alerts active error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# alerts active count

{
  "total": 0,
  "land": 0,
  "marine": 0,
  "regions": {
    "additionalProp1": 1,
    "additionalProp2": 1,
    "additionalProp3": 1
  },
  "areas": {
    "additionalProp1": 1,
    "additionalProp2": 1,
    "additionalProp3": 1
  },
  "zones": {
    "additionalProp1": 1,
    "additionalProp2": 1,
    "additionalProp3": 1
  }
}

# alerts active count error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# alerts active zone

{
  "@context": [
    "string"
  ],
  "type": "FeatureCollection",
  "features": [
    {
      "@context": [
        "string"
      ],
      "id": "string",
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ],
        "bbox": [
          0,
          0,
          0,
          0
        ]
      },
      "properties": {
        "id": "string",
        "areaDesc": "string",
        "geocode": {
          "UGC": [
            "GMC051"
          ],
          "SAME": [
            "110995"
          ]
        },
        "affectedZones": [
          "string"
        ],
        "references": [
          {
            "@id": "string",
            "identifier": "string",
            "sender": "string",
            "sent": "2026-02-12T09:08:43.823Z"
          }
        ],
        "sent": "2026-02-12T09:08:43.823Z",
        "effective": "2026-02-12T09:08:43.823Z",
        "onset": "2026-02-12T09:08:43.823Z",
        "expires": "2026-02-12T09:08:43.823Z",
        "ends": "2026-02-12T09:08:43.823Z",
        "status": "Actual",
        "messageType": "Alert",
        "category": "Met",
        "severity": "Extreme",
        "certainty": "Observed",
        "urgency": "Immediate",
        "event": "string",
        "sender": "string",
        "senderName": "string",
        "headline": "string",
        "description": "string",
        "instruction": "string",
        "response": "Shelter",
        "parameters": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "scope": "Public",
        "code": "string",
        "language": "string",
        "web": "string",
        "eventCode": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        }
      }
    }
  ],
  "title": "string",
  "updated": "2026-02-12T09:08:43.823Z",
  "pagination": {
    "next": "string"
  }
}

# alerts active zone error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# alerts active area

{
  "@context": [
    "string"
  ],
  "type": "FeatureCollection",
  "features": [
    {
      "@context": [
        "string"
      ],
      "id": "string",
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ],
        "bbox": [
          0,
          0,
          0,
          0
        ]
      },
      "properties": {
        "id": "string",
        "areaDesc": "string",
        "geocode": {
          "UGC": [
            "UTZ719"
          ],
          "SAME": [
            "807290"
          ]
        },
        "affectedZones": [
          "string"
        ],
        "references": [
          {
            "@id": "string",
            "identifier": "string",
            "sender": "string",
            "sent": "2026-02-12T09:10:08.049Z"
          }
        ],
        "sent": "2026-02-12T09:10:08.049Z",
        "effective": "2026-02-12T09:10:08.049Z",
        "onset": "2026-02-12T09:10:08.049Z",
        "expires": "2026-02-12T09:10:08.049Z",
        "ends": "2026-02-12T09:10:08.049Z",
        "status": "Actual",
        "messageType": "Alert",
        "category": "Met",
        "severity": "Extreme",
        "certainty": "Observed",
        "urgency": "Immediate",
        "event": "string",
        "sender": "string",
        "senderName": "string",
        "headline": "string",
        "description": "string",
        "instruction": "string",
        "response": "Shelter",
        "parameters": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "scope": "Public",
        "code": "string",
        "language": "string",
        "web": "string",
        "eventCode": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        }
      }
    }
  ],
  "title": "string",
  "updated": "2026-02-12T09:10:08.049Z",
  "pagination": {
    "next": "string"
  }
}

# alerts active area error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# alerts active region

{
  "@context": [
    "string"
  ],
  "type": "FeatureCollection",
  "features": [
    {
      "@context": [
        "string"
      ],
      "id": "string",
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ],
        "bbox": [
          0,
          0,
          0,
          0
        ]
      },
      "properties": {
        "id": "string",
        "areaDesc": "string",
        "geocode": {
          "UGC": [
            "ILC173"
          ],
          "SAME": [
            "090631"
          ]
        },
        "affectedZones": [
          "string"
        ],
        "references": [
          {
            "@id": "string",
            "identifier": "string",
            "sender": "string",
            "sent": "2026-02-12T09:10:56.230Z"
          }
        ],
        "sent": "2026-02-12T09:10:56.230Z",
        "effective": "2026-02-12T09:10:56.230Z",
        "onset": "2026-02-12T09:10:56.230Z",
        "expires": "2026-02-12T09:10:56.230Z",
        "ends": "2026-02-12T09:10:56.230Z",
        "status": "Actual",
        "messageType": "Alert",
        "category": "Met",
        "severity": "Extreme",
        "certainty": "Observed",
        "urgency": "Immediate",
        "event": "string",
        "sender": "string",
        "senderName": "string",
        "headline": "string",
        "description": "string",
        "instruction": "string",
        "response": "Shelter",
        "parameters": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "scope": "Public",
        "code": "string",
        "language": "string",
        "web": "string",
        "eventCode": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        }
      }
    }
  ],
  "title": "string",
  "updated": "2026-02-12T09:10:56.230Z",
  "pagination": {
    "next": "string"
  }
}

# alerts active region error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# alerts type

{
  "eventTypes": [
    "string"
  ]
}

# alerts type error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# alerts id

{
  "@context": [
    "string"
  ],
  "id": "string",
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      0,
      0
    ],
    "bbox": [
      0,
      0,
      0,
      0
    ]
  },
  "properties": {
    "id": "string",
    "areaDesc": "string",
    "geocode": {
      "UGC": [
        "KSC111"
      ],
      "SAME": [
        "594768"
      ]
    },
    "affectedZones": [
      "string"
    ],
    "references": [
      {
        "@id": "string",
        "identifier": "string",
        "sender": "string",
        "sent": "2026-02-12T09:12:19.093Z"
      }
    ],
    "sent": "2026-02-12T09:12:19.093Z",
    "effective": "2026-02-12T09:12:19.094Z",
    "onset": "2026-02-12T09:12:19.094Z",
    "expires": "2026-02-12T09:12:19.094Z",
    "ends": "2026-02-12T09:12:19.094Z",
    "status": "Actual",
    "messageType": "Alert",
    "category": "Met",
    "severity": "Extreme",
    "certainty": "Observed",
    "urgency": "Immediate",
    "event": "string",
    "sender": "string",
    "senderName": "string",
    "headline": "string",
    "description": "string",
    "instruction": "string",
    "response": "Shelter",
    "parameters": {
      "additionalProp1": [
        "string"
      ],
      "additionalProp2": [
        "string"
      ],
      "additionalProp3": [
        "string"
      ]
    },
    "scope": "Public",
    "code": "string",
    "language": "string",
    "web": "string",
    "eventCode": {
      "additionalProp1": [
        "string"
      ],
      "additionalProp2": [
        "string"
      ],
      "additionalProp3": [
        "string"
      ]
    }
  }
}

# alerts id error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# get stations

{
  "@context": [
    "string"
  ],
  "type": "FeatureCollection",
  "features": [
    {
      "@context": [
        "string"
      ],
      "id": "string",
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ],
        "bbox": [
          0,
          0,
          0,
          0
        ]
      },
      "properties": {
        "@context": [
          "string"
        ],
        "geometry": "string",
        "@id": "string",
        "@type": "wx:ObservationStation",
        "elevation": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "uc:;",
          "qualityControl": "Z"
        },
        "stationIdentifier": "string",
        "name": "string",
        "timeZone": "string",
        "provider": "string",
        "subProvider": "string",
        "forecast": "string",
        "county": "string",
        "fireWeatherZone": "string",
        "distance": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "bC;xOv",
          "qualityControl": "Z"
        },
        "bearing": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "LucK-jyWF~y-7SdMBT+u{Rdge2bX@>r9ihjZnKHi}BW>o'QSk;b\",VO=Hr-Z<t,(ZB-:KMF*",
          "qualityControl": "Z"
        }
      }
    }
  ],
  "observationStations": [
    "string"
  ],
  "pagination": {
    "next": "string"
  }
}

# get stations error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}

# points long / lat

{
  "@context": [
    "string"
  ],
  "id": "string",
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      0,
      0
    ],
    "bbox": [
      0,
      0,
      0,
      0
    ]
  },
  "properties": {
    "@context": [
      "string"
    ],
    "geometry": "string",
    "@id": "string",
    "@type": "wx:Point",
    "cwa": "AKQ",
    "type": "land",
    "forecastOffice": "string",
    "gridId": "AKQ",
    "gridX": 0,
    "gridY": 0,
    "forecast": "string",
    "forecastHourly": "string",
    "forecastGridData": "string",
    "observationStations": "string",
    "relativeLocation": {
      "@context": [
        "string"
      ],
      "id": "string",
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ],
        "bbox": [
          0,
          0,
          0,
          0
        ]
      },
      "properties": {
        "city": "string",
        "state": "string",
        "distance": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "wmo:D/PW={?a`m,62k",
          "qualityControl": "Z"
        },
        "bearing": {
          "value": 0,
          "maxValue": 0,
          "minValue": 0,
          "unitCode": "nwsUnit:nP@1LG(HvO Uo>IG$<T&EJQt|HMd(9#^P",
          "qualityControl": "Z"
        }
      }
    },
    "forecastZone": "string",
    "county": "string",
    "fireWeatherZone": "string",
    "timeZone": "string",
    "radarStation": "string",
    "astronomicalData": {
      "sunrise": "2026-02-12T09:18:26.389Z",
      "sunset": "2026-02-12T09:18:26.389Z",
      "transit": "2026-02-12T09:18:26.389Z",
      "civilTwilightBegin": "2026-02-12T09:18:26.389Z",
      "civilTwilightEnd": "2026-02-12T09:18:26.389Z",
      "nauticalTwilightBegin": "2026-02-12T09:18:26.389Z",
      "nauticalTwilightEnd": "2026-02-12T09:18:26.389Z",
      "astronomicalTwilightBegin": "2026-02-12T09:18:26.389Z",
      "astronomicalTwilightEnd": "2026-02-12T09:18:26.389Z"
    },
    "nwr": {
      "transmitter": "string",
      "sameCode": "string",
      "areaBroadcast": "string",
      "pointBroadcast": "string"
    }
  }
}

# points long / lat error

{
  "type": "urn:noaa:nws:api:UnexpectedProblem",
  "title": "Unexpected Problem",
  "status": 500,
  "detail": "An unexpected problem has occurred.",
  "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
  "additionalProp1": {}
}