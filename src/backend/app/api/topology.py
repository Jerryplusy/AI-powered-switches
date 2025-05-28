from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from ...services.task_service import deploy_to_device

router = APIRouter()

class TopologyRequest(BaseModel):
    devices: list
    config: dict

@router.post("/deploy")
async def deploy_topology(
    request: TopologyRequest,
    bg_tasks: BackgroundTasks
):
    task_ids = []
    for device in request.devices:
        task = deploy_to_device.delay(device, request.config)
        task_ids.append(task.id)
    return {"task_ids": task_ids}
