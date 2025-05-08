from __future__ import annotations

import pytest

from calendar_txt.calendar.domain.event import Event, InvalidEventFormatError

# ---- Test for Event.__Init__() ----


def test_event_to_str_with_times_and_tag() -> None:
    event = Event(
        description="Hacer ejercicio", start_time="07:00", end_time="08:00", tag="h"
    )
    except_event_str = "+ 07:00-08:00 #h Hacer ejercicio"

    assert str(event) == except_event_str


def test_event_to_str_with_start_time_and_tag() -> None:
    event = Event(
        description="Hacer ejercicio",
        start_time="07:00",
        # end_time
        tag="h",
    )
    except_event_str = "+ 07:00 #h Hacer ejercicio"

    assert str(event) == except_event_str


def test_event_to_str_with_tag() -> None:
    event = Event(
        description="Hacer ejercicio",
        # start_time
        # end_time
        tag="h",
    )
    except_event_str = "+ #h Hacer ejercicio"

    assert str(event) == except_event_str


def test_event_to_str_with_only_description() -> None:
    event = Event(
        description="Hacer ejercicio",
        # start_time
        # end_time
        # tag
    )
    except_event_str = "+ Hacer ejercicio"

    assert str(event) == except_event_str


# ---- Test for Event.from_string() ----


def test_event_from_string_full() -> None:
    line = "+ 10:00-11:30 #w Reunión importante"
    event = Event.from_string(line)

    except_event = Event(
        description="Reunión importante", start_time="10:00", end_time="11:30", tag="w"
    )
    assert event == except_event


def test_event_from_string_start_time_tag() -> None:
    line = "+ 08:00 #p Revisar código"
    event = Event.from_string(line)

    except_event = Event(description="Revisar código", start_time="08:00", tag="p")
    assert event == except_event


def test_event_from_string_tag_only() -> None:
    line = "+ #h Sacar la basura"
    event = Event.from_string(line)

    except_event = Event(description="Sacar la basura", tag="h")
    assert event == except_event


def test_event_from_string_description_only() -> None:
    line = "+ Descansar un poco"
    event = Event.from_string(line)

    except_event = Event(
        description="Descansar un poco",
    )
    assert event == except_event


def test_event_from_string_start_time_only() -> None:
    line = "+ 14:00 Ir al médico"
    event = Event.from_string(line)

    except_event = Event(
        description="Ir al médico",
        start_time="14:00",
    )
    assert event == except_event


def test_event_from_string_time_range_only() -> None:
    line = "+ 09:30-12:00 Bloque de trabajo"
    event = Event.from_string(line)

    except_event = Event(
        description="Bloque de trabajo",
        start_time="09:30",
        end_time="12:00",
    )
    assert event == except_event


def test_event_from_string_extra_spaces() -> None:
    line = "  +   10:00   #w    Muchos espacios  "
    event = Event.from_string(line)

    except_event = Event(
        description="Muchos espacios",
        start_time="10:00",
        tag="w",
    )
    assert event == except_event


def test_event_from_string_invalid_format() -> None:
    # sin '+'

    line_1 = "Sin el plus"

    with pytest.raises(InvalidEventFormatError) as err:
        Event.from_string(line_1)

    assert str(err.value) == "La línea de evento debe empezar con '+': 'Sin el plus'"

    # Línea vacía después de '+'

    line_2 = "+ "
    with pytest.raises(InvalidEventFormatError) as err:
        Event.from_string(line_2)
    assert str(err.value) == "La línea de evento no puede estar vacía: '+ '"
