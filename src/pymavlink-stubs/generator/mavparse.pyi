import os

PROTOCOL_0_9: str
PROTOCOL_1_0: str
PROTOCOL_2_0: str
FLAG_HAVE_TARGET_SYSTEM: int
FLAG_HAVE_TARGET_COMPONENT: int

class MAVField:
    name: str
    name_upper: str
    description: str
    array_length: int
    enum: str
    display: str
    units: str
    multiplier: str
    omit_arg: bool
    print_format: str
    instance: bool
    type_length: int
    type: str
    wire_length: int
    wire_offset: int
    type_upper: str
    def __init__(
        self,
        name: str,
        type: str,
        print_format: str,
        xml: MAVXML,
        description: str = "",
        enum: str = "",
        display: str = "",
        units: str = "",
        multiplier: str = "",
        instance: bool = False,
    ) -> None: ...

class MAVType:
    name: str
    name_lower: str
    linenumber: int
    id: int
    description: str
    fields: list[MAVField]
    fieldnames: list[str]
    extensions_start: int
    needs_pack: bool
    crc_extra: int
    wire_length: int
    wire_min_length: int
    def __init__(self, name: str, id: int, linenumber: int, description: str = "") -> None: ...
    def base_fields(self) -> int: ...

class MAVEnumEntry:
    name: str
    value: int
    description: str
    end_marker: bool
    autovalue: bool
    origin_file: str
    origin_line: int
    has_location: bool
    def __init__(
        self,
        name: str,
        value: int,
        description: str = "",
        end_marker: bool = False,
        autovalue: bool = False,
        origin_file: str = "",
        origin_line: int = 0,
        has_location: bool = False,
    ) -> None: ...

class MAVEnum:
    name: str
    description: str
    entry: list[MAVEnumEntry]
    start_value: int
    highest_value: int
    linenumber: int
    bitmask: bool
    def __init__(self, name: str, linenumber: int, description: str = "", bitmask: bool = False) -> None: ...

class MAVXML:
    filename: os.PathLike[str]
    basename: str
    basename_upper: str
    message: list[MAVType]
    enum: list[MAVEnum]
    parse_time: str
    version: int
    include: list[str]
    wire_protocol_version: str
    protocol_marker: int
    sort_fields: bool
    little_endian: bool
    crc_extra: bool
    crc_struct: bool
    command_24bit: bool
    allow_extensions: bool
    message_lengths: dict[int, int]
    message_min_lengths: dict[int, int]
    message_flags: dict[int, int]
    message_target_system_ofs: dict[int, int]
    message_target_component_ofs: dict[int, int]
    message_crcs: dict[int, int]
    message_names: dict[int, str]
    largest_payload: int
    def __init__(self, filename: os.PathLike[str], wire_protocol_version: str) -> None: ...
