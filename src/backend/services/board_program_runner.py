from collections.abc import Callable
import os
import shlex
import signal
import subprocess
import threading
from typing import Protocol


BoardProgram = str


class ProgramHandle(Protocol):
    pid: int

    def poll(self) -> int | None:
        ...

    def interrupt(self) -> None:
        ...


class ProgramRunner(Protocol):
    def start(
        self,
        program: BoardProgram,
        on_output: Callable[[str], None],
    ) -> ProgramHandle:
        ...


BOARD_PROGRAM_LAUNCHES = {
    "pick_sort_default": "ros2 launch robot_arm_bringup block_cls_bringup.launch.py",
    "stack_default": "ros2 launch robot_arm_bringup color_stacking_bringup.launch.py",
}


class SubprocessProgramHandle:
    def __init__(self, process) -> None:
        self._process = process
        self.pid = process.pid

    def poll(self) -> int | None:
        return self._process.poll()

    def interrupt(self) -> None:
        try:
            os.killpg(self._process.pid, signal.SIGINT)
        except ProcessLookupError:
            return
        except Exception:
            try:
                self._process.send_signal(signal.SIGINT)
            except ProcessLookupError:
                return


class SubprocessProgramRunner:
    def __init__(
        self,
        *,
        robot_arm_root: str,
        popen=subprocess.Popen,
        start_log_reader: bool = True,
    ) -> None:
        self.robot_arm_root = robot_arm_root
        self._popen = popen
        self._start_log_reader = start_log_reader

    def start(
        self,
        program: BoardProgram,
        on_output: Callable[[str], None],
    ) -> ProgramHandle:
        try:
            launch = BOARD_PROGRAM_LAUNCHES[program]
        except KeyError as exc:
            raise ValueError(f"Unsupported board program: {program}") from exc
        root = shlex.quote(self.robot_arm_root)
        command = f"cd {root} && . ./setenv.sh && exec {launch}"
        process = self._popen(
            ["bash", "-lc", command],
            cwd=self.robot_arm_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True,
        )
        if self._start_log_reader:
            thread = threading.Thread(
                target=self._read_output,
                args=(process, on_output),
                daemon=True,
            )
            thread.start()
        return SubprocessProgramHandle(process)

    def _read_output(self, process, on_output: Callable[[str], None]) -> None:
        if process.stdout is None:
            return
        for line in process.stdout:
            text = line.rstrip()
            if text:
                on_output(text)
