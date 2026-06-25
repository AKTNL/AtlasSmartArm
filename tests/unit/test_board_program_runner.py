from src.backend.services.board_program_runner import SubprocessProgramRunner


class FakeStdout:
    def __iter__(self):
        return iter(())


class FakeProcess:
    pid = 5151
    returncode = None
    stdout = FakeStdout()

    def poll(self):
        return self.returncode


class FakePopen:
    def __init__(self) -> None:
        self.calls = []
        self.process = FakeProcess()

    def __call__(self, args, **kwargs):
        self.calls.append((args, kwargs))
        return self.process


def test_subprocess_program_runner_builds_pick_sort_launch_command():
    fake_popen = FakePopen()
    runner = SubprocessProgramRunner(
        robot_arm_root="/opt/robot_arm",
        popen=fake_popen,
        start_log_reader=False,
    )

    handle = runner.start("pick_sort_default", lambda line: None)

    assert handle.pid == 5151
    args, kwargs = fake_popen.calls[0]
    assert args == [
        "bash",
        "-lc",
        "cd /opt/robot_arm && . ./setenv.sh && exec ros2 launch robot_arm_bringup block_cls_bringup.launch.py",
    ]
    assert kwargs["cwd"] == "/opt/robot_arm"


def test_subprocess_program_runner_builds_stack_launch_command():
    fake_popen = FakePopen()
    runner = SubprocessProgramRunner(
        robot_arm_root="/opt/robot_arm",
        popen=fake_popen,
        start_log_reader=False,
    )

    runner.start("stack_default", lambda line: None)

    args, _ = fake_popen.calls[0]
    assert args[2].endswith(
        "exec ros2 launch robot_arm_bringup color_stacking_bringup.launch.py"
    )
