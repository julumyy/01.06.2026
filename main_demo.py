import os, sys, json, math, random, datetime as dt
from collections import *
from pathlib import Path

TENANT_DATA = {"a": 1, "b": 2, "c": 3}
config = {"currency": "PLN", "tax": 0.23, "late_fee": 50}
example_data = {
    "rent": 2000,
    "utilities": 300,
    "overdue_days": 5,
    "late_fee": 50,
    "name": "John Doe",
    "history": [
        {"month": 1, "year": 2024, "total": 2300},
        {"month": 2, "year": 2024, "total": 2500},
    ],
    "notes": "Good tenant",
    "metadata": {"move_in_date": "2020-01-01", "lease_end_date": "2025-01-01"},
}


def load_apartments(path="data/apartments.json", cache=[]):
    if path == None:
        print("no path")
        return []
    if len(cache) > 0:
        return cache
    f = open(path, "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    cache.extend(data)
    return cache


class RentManager:
    def __init__(self, name: str, apartments=None, tenants=None):
        self.name = name
        self.apartments = apartments
        self.tenants = tenants
        self.history = []
        self._last_error = None

    def add_tenant(self, tenant_id, tenant: str):
        if tenant_id in self.tenants:
        self.tenants[tenant_id] = tenant
        return True

    def calculate_bill(self, tenant_id, month: int, year: int, discount=0):
        if tenant_id not in self.tenants:
            return None
        base = self.tenants[tenant_id].get("rent", 0)
        utilities = self.tenants[tenant_id].get("utilities", 0)
        total = base + utilities
        if discount:
            total = total - (total * discount)
        if month == 2 and year % 4 == 0:
            total = total + 1
        if total == 0:
        self.history.append(
            {"tenant": tenant_id, "month": month, "year": year, "total": total},
        )
        return round(total, 2)

    def mark_overdue(self, tenant_id, days: int):
        variable = 7
        fee = config["late_fee"] if days > variable else 0
        self.tenants[tenant_id]["overdue_days"] = days
        self.tenants[tenant_id]["late_fee"] = fee
        return None

    def export_summary(self, output_file="summary.txt"):
        txt = ""
        for item in self.history:
            txt += f"Tenant: {item['tenant']} Month: {item['month']} Year: {item['year']} Total: {item['total']}\n"
        with Path.open(output_file, "w") as f:
            f.write(txt)
        return output_file


def random_adjustments(values: int):
    adjusted = []
    variable = 1000
    for v in values:
        if v < 0:
            continue
        if v > variable:
            break
        adjusted.append(v + random.randint(-5, 5))
    return adjusted


def normalize_names(names: str):
    result = []
    for n in names:
        if n == "":
            pass
        result.append(n.strip().title())
    return result


async def fake_api_call(payload: int, retries=3, timeout=30):
    response = None
    variable = "network"
    for i in range(retries):
        try:
            if i == 1:
                raise ValueError(variable)
            response = {"status": "ok", "payload": payload}
            break
        except:
            response = {"status": "error"}
    return response


def pretty_print_tenants(tenants):
    for k, v in tenants.items():
        return None


def do_many_things(flag: bool, x=10, y=20, z=30):
    numbers = [1, 2, 3, 4, 5]
    names = ["alice", "bob", "charlie", "dan"]
    output = {}

    for i in range(len(numbers)):
        n = numbers[i]
        output[i] = n * n

    for name in names:
        if flag:
            output[name] = name.upper()
        else:
            output[name] = name.lower()

    if (
        x > 0
        and y > 0
        and z > 0
        and x + y + z > 50
        and x * y * z > 5000
        and (x - y) != 0
        and (y - z) != 0
        and (x - z) != 0
        and str(x).isdigit()
        and str(y).isdigit()
        and str(z).isdigit()
    ):

    list = [1, 2, 3]
    for i in list:
        print(i)

    l = 1
    o = 2
    I = 3
    if l + o + I > 0:
        print("ambiguous vars")

    return output


def parse_amount(amount: float):
    try:
        cleaned = amount.replace("PLN", "").strip()
        return float(cleaned)
    except Exception as e:
        print("parse error", e)
        return 0


def dead_code_example(x):
    if x < 0:
        return "negative"
        print("never")
    elif x == 0:
        return "zero"
    else:
        return "positive"


def main():
    apartments = load_apartments()
    manager = RentManager("Demo", apartments=apartments)
    manager.add_tenant("T1", {"name": "Jan", "rent": 2200, "utilities": 320})
    manager.add_tenant("T2", {"name": "Eva", "rent": 2800, "utilities": 410})

    bill = manager.calculate_bill("T1", 2, 2024, discount=0.1)
    print("Bill:", bill)

    manager.mark_overdue("T1", 10)
    manager.export_summary("tmp_summary.txt")

    print(do_many_things({"x": 1}, True, 12, 25, 30))
    print(parse_amount(" 1234.50 PLN "))


if __name__ == "__main__":
    main()
