from __future__ import annotations
from datetime import datetime

from .base import _Base
from .users import User


class CommentReaction(_Base):
    type: str
    author: User
    created_at: datetime


class Comment(_Base):
    id: int
    body: str
    inline_text: str | None = None
    parent_id: int | None = None
    author: User
    thread_id: int | None = None
    created_at: datetime
    is_deleted: bool
    resolve_status: str | None = None
    reactions: list[CommentReaction] = []


class ThreadInfo(_Base):
    total_posts: int
    last_comment: Comment | None = None


class CommentExtended(Comment):
    thread_info: ThreadInfo | None = None


class DeleteCommentResult(_Base):
    comments_count: int
