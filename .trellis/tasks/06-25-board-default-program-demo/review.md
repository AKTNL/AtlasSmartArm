# High-Risk Review Checklist

## Reviewed

- Single-task lock: board mode rejects a second task with `ARM_BUSY` while a
  default program task is active.
- Camera ownership: frontend does not request a video stream during default
  program execution; UI marks the camera as reserved by the ROS2 program.
- Cancellation semantics: task cancellation sends an interrupt to the launched
  process and explicitly does not claim to be an emergency stop.
- Process startup failure: failed launch returns a unified API error and does
  not leave an active task lock behind.
- Inventory correctness: default program tasks do not mutate inventory or write
  fake object-location records.
- Module boundary: routes call `TaskService`; ROS2 launch details are hidden
  behind `board_program_runner.py`.

## Needs Manual Board Confirmation

- Confirm `ros2 launch robot_arm_bringup block_cls_bringup.launch.py` starts the
  board's default sorting program from `ROBOT_ARM_ROOT`.
- Confirm `ros2 launch robot_arm_bringup color_stacking_bringup.launch.py`
  starts the board's default stacking program from `ROBOT_ARM_ROOT`.
- Confirm SIGINT cleanly stops the default ROS2 launch without leaving arm or
  camera processes running.
- Confirm no separate process opens `/dev/video0` while a default program task
  is running.
