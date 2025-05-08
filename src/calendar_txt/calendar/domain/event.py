"""Representa una línea de evento/tarea dentro de un día."""

from __future__ import annotations

import datetime
import re


class Event:
    """Representa una línea de evento/tarea dentro de un día."""

    EVENT_LINE_REGEX = re.compile(
        r"^\+\s*"  # Inicio: + y espacios opcionales
        r"(?:(\d{2}:\d{2})(?:-(\d{2}:\d{2}))?\s+)?"  # Grupo 1 y 2: Hora(s) opcional
        r"(?:(#\w+)\s+)?"  # Grupo 3: Tag opcional con espacio después
        r"(.*)$"  # Grupo 4: Descripción (el resto)
    )

    def __init__(
        self,
        description: str,
        start_time: str | None = None,
        end_time: str | None = None,
        tag: str | None = None,
    ):
        """Init de Event."""
        self.start_time: datetime.time | None = (
            datetime.datetime.strptime(start_time, "%H:%M").time()
            if start_time
            else None
        )

        self.end_time: datetime.time | None = (
            datetime.datetime.strptime(end_time, "%H:%M").time()
            if self.start_time and end_time
            else None
        )

        self.tag = tag.strip() if tag else None
        self.description = description.strip()

    def __str__(self) -> str:
        """Representación en formato calendar.txt."""
        parts = ["+"]
        time_str = ""

        if self.start_time:
            time_str += self.start_time.strftime("%H:%M")

            if self.end_time:
                time_str += f"-{self.end_time.strftime('%H:%M')}"

        if time_str:
            parts.append(time_str)

        if self.tag:
            parts.append(f"#{self.tag}")

        parts.append(self.description)

        return " ".join(parts)

    def __eq__(self, object: object) -> bool:
        """Equal de Event."""
        if not isinstance(object, Event):
            return NotImplemented

        return (
            self.description == object.description
            and self.start_time == object.start_time
            and self.end_time == object.end_time
            and self.tag == object.tag
        )

    @classmethod
    def from_string(cls, line: str) -> Event:
        """
        Crea una instancia de Event a partir de una línea de texto.

        El formato es: '+ [HH:MM-HH:MM] [#tag] descripción'.

        Args:
            line: La cadena de texto a parsear.

        Returns:
            Una nueva instancia de Event.

        Raises:
            ValueError: Si la línea no tiene el formato esperado
                        o no empieza con '+'.

        """
        line = line.strip()
        if not line.startswith("+"):
            msg = f"La línea de evento debe empezar con '+': '{line}'"
            raise ValueError(msg)

        match = cls.EVENT_LINE_REGEX.match(line)

        if not match:
            msg = f"Formato de línea de evento no válido: '{line}'"
            raise ValueError(msg)

        start_str, end_str, tag_with_hash, desc_str = match.groups()

        # Pasamos los strings directamente, __init__ se encarga de parsear/limpiar
        return cls(
            description=desc_str,
            start_time=start_str,
            end_time=end_str,
            tag=tag_with_hash.replace("#", "") if tag_with_hash else None,
        )
