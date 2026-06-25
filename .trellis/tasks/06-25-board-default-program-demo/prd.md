# Board Default Program Demo

## Goal

Build a true-board demo where the frontend runs locally, the backend runs on
the Atlas board, and backend task APIs launch the board's existing ROS2 sorting
and stacking programs.

## Success Criteria

- Users can start default pick-sort and stack programs from the frontend.
- In board mode, only one hardware task can run at a time.
- Task details expose program name, pid, exit code, start/end times, and recent
  ROS output logs.
- Cancelling a task sends an interrupt to the running program and clearly does
  not claim to be an emergency stop.
- The demo does not open a video stream while a default program owns the camera.
- The management panel shows task records and logs only; it does not write fake
  inventory or object-location results.

## Board Commands

- Pick-sort:
  `cd $ROBOT_ARM_ROOT && . ./setenv.sh && ros2 launch robot_arm_bringup block_cls_bringup.launch.py`
- Stack:
  `cd $ROBOT_ARM_ROOT && . ./setenv.sh && ros2 launch robot_arm_bringup color_stacking_bringup.launch.py`
- Default `ROBOT_ARM_ROOT`:
  `/home/HwHiAiUser/E2ESamples/src/E2E-Sample/ros2_robot_arm`

## Public Interfaces

- Preserve existing task endpoints:
  `POST /api/v1/tasks/pick-sort`, `POST /api/v1/tasks/stack`,
  `GET /api/v1/tasks/{task_id}`, and `POST /api/v1/tasks/{task_id}/cancel`.
- Extend task detail data with `program`, `pid`, `exit_code`, `logs`,
  `started_at`, and `ended_at`.
- Extend system status with `program_mode`, `active_task_id`, and
  `camera_policy`.

## Testing Requirements

- Contract tests cover board-mode command selection, single-task locking,
  process output logs, success/failure/cancel state mapping, and no automatic
  inventory mutation.
- Frontend API tests cover new task/system fields.
- Full verification runs backend pytest plus frontend tests and build.

## Risk Notes

This task touches hardware-control and concurrency behavior. Before completion,
run an explicit review for single-task locking, camera exclusivity, cancellation
semantics, process cleanup, and false inventory writes.
