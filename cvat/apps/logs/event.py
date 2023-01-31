# Copyright (C) 2023 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from rest_framework.renderers import JSONRenderer
from datetime import datetime, timezone

def event_scope(action, resource):
    return f"{action}:{resource}"


class EventScopes:
    RESOURCES = {
        "project": ["create", "update", "delete"],
        "task": ["create", "update", "delete"],
        "job": ["create", "update"],
        "organization": ["create", "update", "delete"],
        # "user": ["create", "update", "delete"],
        "cloudstorage": ["create", "update", "delete"],
        "issue": ["create", "update", "delete"],
        "comment": ["create", "update", "delete"],
        "invitation": ["create", "delete"],
        "membership": ["update", "delete"],
        "annotations": ["create", "update", "delete"],
    }

    @classmethod
    def select(cls, resources):
        return [
            f"{event_scope(action, resource)}"
            for resource in resources
            for action in cls.RESOURCES.get(resource, [])
        ]

def create_event(scope, source, **kwargs):
    payload = kwargs.pop('payload', None)

    data = {
        "scope": scope,
        "timestamp": str(datetime.now(timezone.utc).timestamp()),
        "source": source,
        **kwargs,
    }
    if payload:
        data["payload"] = JSONRenderer().render(payload).decode('UTF-8')

    return data

def update_event(data, pid=None, tid=None, jid=None, oid=None):
    if pid:
        data["project"] = pid
    if oid:
        data["organization"] = oid
    if tid:
        data["task"] = tid
    if jid:
        data["job"] = jid

    return data

class EventScopeChoice:
    @classmethod
    def choices(cls):
        return sorted((val, val.upper()) for val in AllEvents.events)

class AllEvents:
    events = list(
        event_scope(action, resource)
        for resource, actions in EventScopes.RESOURCES.items()
        for action in actions
    )