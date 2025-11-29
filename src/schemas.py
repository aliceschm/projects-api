# Pydantic models for request validation and response serialization.
# They ensure that input data sent to the API is valid and that responses have a consistent format.
# Schemas are separate from ORM models to decouple database structure from API interface.

from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum
from datetime import date


class ProjectStatus(str, Enum):
    idea = "idea"
    planning = "planning"
    in_progress = "in_progress"
    paused = "paused"
    finished = "finished"
    archived = "archived"

class ProjectDescCreate(BaseModel):
    lang: str
    name: str
    about: Optional[str] = None
    full_desc: Optional[str] = None

class ProjectCreate(BaseModel):
    #table projects fields
    status: ProjectStatus
    slug: str
    deploy_date: Optional[date] = None
    #stacks
    stacks: List[str]           
    #table project_desc fields
    descriptions: ProjectDescCreate


