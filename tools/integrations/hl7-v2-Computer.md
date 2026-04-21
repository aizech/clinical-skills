# HL7 v2 Integration

Legacy HL7 messaging for order/result communication.

## Connection

```yaml
host: hl7.example.com
port: 2575
application: RAD_PMS
facility: HOSPITAL
```

## Message Types

### ORM (Order Message)
```
MSH|^~\&|RIS|HOSPITAL|PMS|HOSP|202401151030||ORM^O01|MSG001|P|2.4
PID|1||MRN12345^^^HOSP^MR||DOE^JOHN||19800101|M
ORC|OB|ORD123|ORD123|12345||CM||||202401151000
OBR|1|ORD123|ORD123|CT^CT Chest||...
```

### ORU (Observation Result)
```
MSH|^~\&|RIS|HOSPITAL|PMS|HOSP|202401151030||ORU^R01|RES001|P|2.4
PID|1||MRN12345^^^HOSP^MR||DOE^JOHN||19800101|M
OBR|1|ORD123|ORD123|CT^CT Chest||...
OBX|1|NM|GAIN^Slice@Thickness||3.0||mm|0-5|N|||F
OBX|2|TX|FIND^Findings||Normal chest CT. No acute findings.||...
```

## MLLP Framing

HL7 over TCP uses MLLP (Minimal Lower Layer Protocol):
```
<SB> (0x0B) - Start Block
[Message]
<EB> (0x1C) - End Block
<CR> (0x0D) - Carriage Return
```

## Key Segments

| Segment | Description |
|---------|-------------|
| MSH | Message Header |
| PID | Patient Identification |
| OBR | Observation Request |
| OBX | Observation/Result |
| ORC | Common Order |

## Parsing

```python
import hl7

message = hl7.parse(raw_hl7)
patient_id = message.pid('3.1')  # PID.3.1 = ID
accession = message.orc('2.1')   # ORC.2.1 = Placer Order Number
findings = message.obx('5.1')     # OBX.5.1 = Observation Value
```

## Acknowledgments

```
MSH|^~\&|PMS|HOSP|RIS|HOSP|...||ACK^O01|...|P|2.4
MSA|AA|MSG001|Success
```

## Tool Registration

```json
{
  "name": "hl7_v2",
  "description": "HL7 v2 ORM/ORU message parsing and transmission",
  "category": "interoperability",
  "message_types": ["ORM", "ORU", "ACK", "ADT"]
}
```
