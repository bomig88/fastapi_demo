from enum import Enum


class MemberStatus(str, Enum):
    JOIN = 'join'
    LOCK = 'lock'
    LEAVE = 'leave'


class OrderStatus(str, Enum):
    ALL_PAID = 'all_paid'
    ALL_REFUND = 'all_refund'
    PARTIAL_REFUND = 'partial_refund'


class OrderProductStatus(str, Enum):
    PAID = 'paid'
    REFUND = 'refund'
