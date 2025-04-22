"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

from slugify import slugify
from .uobject import UObject

class UContract(UObject):
    def __init__(self, name, customer_id=None, provider_id=None):
        super().__init__(name)
        self.customer = customer_id
        self.provider = provider_id
        self.state = "template"
        self.customer_credit = []
        self.customer_debet = []
        self.provider_credit = []
        self.provider_debet = []
        self.history = []

    def get_file_name(self):
        return f"{slugify(self.name)}.ctp"