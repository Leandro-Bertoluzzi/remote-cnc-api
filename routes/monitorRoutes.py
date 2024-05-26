from authMiddleware import GetAdminDep
from config import GRBL_LOGS_FILE
from core.utils.logs import LogsInterpreter
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

monitorRoutes = APIRouter(prefix="/monitor", tags=["Monitor"])


class LogResponseModel(BaseModel):
    datetime: str
    level: str
    type: Optional[str]
    message: str


@monitorRoutes.get('/logs')
def get_logs(
    admin: GetAdminDep
) -> list[LogResponseModel]:
    logs = []
    log_sets = LogsInterpreter().interpret_file(GRBL_LOGS_FILE)

    for datetime, level, type, message in log_sets:
        log_dict = {
            'datetime': datetime,
            'level': level,
            'type': type,
            'message': message,
        }
        logs.append(log_dict)

    return logs
