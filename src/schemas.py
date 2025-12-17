# Pydantic models for request validation and response serialization.
# They ensure that input data sent to the API is valid and that responses have a consistent format.
# Schemas are separate from ORM models to decouple database structure from API interface.

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import date

class ProjectLang(str, Enum):
    pt = "pt"
    en = "en"

class ProjectStatus(str, Enum):
    idea = "idea"
    planning = "planning"
    in_progress = "in_progress"
    paused = "paused"
    finished = "finished"
    archived = "archived"

class ProjectDescCreate(BaseModel):
    lang: ProjectLang
    name: str
    about: Optional[str] = None
    full_desc: Optional[str] = None

class ProjectCreate(BaseModel):
    #table projects fields
    status: ProjectStatus
    slug: str
    deploy_date: Optional[date] = None
    #stacks
    stacks: Optional[List[str]] = Field(default_factory=list) #if field is not received its viewed as empty list - avoid  'NoneType' object is not iterable
    #project_desc table
    descriptions: List[ProjectDescCreate] = Field(..., min_items=1) #guarantee list is not received empty


class ProjectOut(BaseModel):
    id: int
    slug: str
    name: str
    about: Optional[str] = None
    stack_names: Optional[List[str]] = Field(default_factory=list)

    model_config = {
        "from_attributes": True 
    }

class ProjectDetailOut(BaseModel):
    id: int
    lang: ProjectLang
    slug: str
    deploy_date: Optional[date] = None
    status: str
    stack_names: Optional[List[str]] = Field(default_factory=list)
    full_desc: Optional[str] = None


    model_config = {
        "from_attributes": True 
    }
    

class ProjectDescPatch(BaseModel):
    lang: str
    name: Optional[str] = None
    about: Optional[str] = None
    full_desc: Optional[str] = None

    model_config = {"extra": "forbid"}

class ProjectPatch(BaseModel):
    status: Optional[str] = None
    slug: Optional[str] = None
    deploy_date: Optional[date] = None

    description: Optional[ProjectDescPatch] = None
    stacks: Optional[List[str]] = None 

    model_config = {"extra": "forbid"}