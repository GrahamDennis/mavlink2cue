import os
import pathlib
import textwrap

import click
from attrs import frozen
from pymavlink.generator import mavparse

_INDENT = "  "


@frozen
class MavlinkParserError(Exception):
    """Custom exception for MAVLink parsing errors."""

    path: os.PathLike[str]


@click.command()
@click.argument("dialect", type=click.Path(exists=True))
def mavlink2cue(dialect: os.PathLike[str]) -> None:
    """Converts a MAVLink dialect to a CUE schema."""

    mavxmls = parse_dialect(dialect)
    click.echo(convert_dialect(mavxmls))


def parse_dialect(dialect: os.PathLike[str]) -> list[mavparse.MAVXML]:
    mavxmls: list[mavparse.MAVXML] = []
    parsed_paths: set[os.PathLike[str]] = set()
    pending = [dialect]

    while pending:
        current = pending.pop()
        if current in parsed_paths:
            continue

        try:
            mavxml = mavparse.MAVXML(current, wire_protocol_version=mavparse.PROTOCOL_2_0)
        except Exception as e:
            raise MavlinkParserError(path=current) from e

        parsed_paths.add(current)
        mavxmls.append(mavxml)
        include_base = pathlib.Path(current).parent
        pending.extend((include_base.joinpath(include) for include in mavxml.include))

    mavxmls.reverse()
    return mavxmls


def convert_field(field: mavparse.MAVField, include_name: bool = True) -> str:
    fields = [
        f'type: "{field.type}"',
        f"wire_length: {field.wire_length}",
        f"wire_offset: {field.wire_offset}",
    ]
    if field.enum:
        fields.append(f"enum: {field.enum}")
    return f"""{{ {", ".join(fields)} }}"""


def convert_message_metadata(message: mavparse.MAVType) -> str:
    return f"{{ id: {message.id}, crc_extra: {message.crc_extra}, wire_min_length: {message.wire_min_length} }}"


def convert_message(message: mavparse.MAVType) -> str:
    extensions_start = message.extensions_start if message.extensions_start is not None else len(message.fields)
    return "\n".join(
        (
            "{",
            textwrap.indent(
                "\n".join(
                    (
                        f"metadata: {convert_message_metadata(message)}",
                        "fields: {",
                        textwrap.indent(
                            "\n".join(
                                f"{field.name}{'?' if idx >= extensions_start else ''}: {convert_field(field)}"
                                for idx, field in enumerate(message.fields)
                            ),
                            _INDENT,
                        ),
                        "}",
                    )
                ),
                _INDENT,
            ),
            "}",
        )
    )


def convert_enum(enum: mavparse.MAVEnum) -> str:
    return "\n".join(("{", *(textwrap.indent(f"{entry.name}?: {entry.value}", _INDENT) for entry in enum.entry), "}"))


def convert_dialect(mavxmls: list[mavparse.MAVXML]) -> str:
    """Converts a MAVLink XML dialect to a CUE schema."""

    return "\n".join(
        (
            "#schema: {",
            "  enums: {",
            *(
                textwrap.indent(f"{enum.name}?: {convert_enum(enum)}", _INDENT * 2)
                for mavxml in mavxmls
                for enum in mavxml.enum
            ),
            "  }",
            "  messages: {",
            *(
                textwrap.indent(f"{message.name}?: {convert_message(message)}", _INDENT * 2)
                for mavxml in mavxmls
                for message in mavxml.message
            ),
            "  }",
            "}",
        )
    )
