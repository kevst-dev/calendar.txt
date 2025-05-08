"""Representa una bloque diario con eventos/tareas dentro."""

from __future__ import annotations

import datetime
import re

from event import Event


class Day:
    """Representa un bloque diario en el archivo."""

    def __init__(self, date_str: str, day_name: str, location: str | None = None):
        """Init."""
        self.date: datetime.date = datetime.datetime.strptime(
            date_str, "%Y-%m-%d"
        ).date()
        self.day_name: str = day_name.lower()
        self.location: str | None = location
        self.events: list[Event] = []

    def get_header_str(self) -> str:
        """Genera la cadena de texto del encabezado del día."""
        header = f"{self.date.strftime('%Y-%m-%d')} {self.day_name}"

        if self.location:
            header += f" [{self.location}]"

        return header

    def __str__(self) -> str:
        """
        Genera la representación completa del día en formato calendar.txt.

        La estructura se un encabezado seguido de sus eventos.
        """
        header = self.get_header_str()

        # Ordenar eventos por hora de inicio (si la tienen) puede ser útil
        # self.events.sort(key=lambda ev: ev.start_time or datetime.time.min)
        event_lines = "\n".join(str(event) for event in self.events)

        # Si hay eventos, añadir una nueva línea entre cabecera y eventos
        return f"{header}\n{event_lines}" if event_lines else header

    def __eq__(self, other: object) -> bool:
        """Compara si dos objetos Day son iguales."""
        if not isinstance(other, Day):
            return NotImplemented

        return (
            self.date == other.date
            and self.day_name == other.day_name
            and self.location == other.location
            and self.events == other.events  # Compara las listas de eventos
        )

    def add_event(self, event: Event) -> None:
        """Añade un objeto Event preexistente a la lista de eventos del día."""
        if not isinstance(event, Event):
            msg = "Solo se pueden añadir objetos Event."
            raise TypeError(msg)

        self.events.append(event)

    def add_event_from_string(self, line: str) -> None:
        """
        Parsea una línea de texto de evento y la añade a la lista de eventos del día.

        Adicional: Captura y reporta errores de parseo de la línea.
        """
        event = Event.from_string(line)
        self.add_event(event)

    @classmethod
    def from_header_str(cls, header_line: str) -> Day:
        """
        Crea un objeto Day (sin eventos) parseando la línea de encabezado.

        Args:
            header_line: Cadena de texto del encabezado (e.g., "2024-08-01 jueves [V]").

        Returns:
            Una nueva instancia de Day (sin eventos).

        """
        header_regex = re.compile(
            r"^(\d{4}-\d{2}-\d{2})\s+"  # Grupo 1: Fecha YYYY-MM-DD
            r"(\w+)"  # Grupo 2: Nombre del día
            r"(?:\s+\[([VPL?])\])?$"  # Grupo 3: Ubicación opcional [V/P/L/?]
        )

        match = header_regex.match(header_line.strip())

        if not match:
            msg = f"Formato de línea de encabezado inválido: '{header_line}'"
            raise ValueError(msg)

        date_str, day_name_read, location = match.groups()

        return cls(date_str=date_str, day_name=day_name_read, location=location)
