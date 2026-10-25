from ..domain import EnergyConsumer

# отчет сколько всего единиц
class FleetSummary:
    def __init__(self, vehicles, items, by_kind):
        self.vehicles = vehicles
        self.items = items
        self.total = vehicles + items
        self.by_kind = by_kind
# в нашем случае отчетам нужно 2 помощника
# один из помощников это fleet другой beginner_policy
class FleetReports:
    def __init__(self, fleet, beginner_policy):
        self._fleet = fleet
        self._beginner_policy = beginner_policy
    # считаем сколько раз встретился каждый вид
    # то есть условно перебирает все имуещство и просто делает +1
    def summary(self):
        by_kind = {}
        for asset in self._fleet.assets:
            kind = asset.kind
            if kind in by_kind:
                by_kind[kind] = by_kind[kind] + 1
            else:
                by_kind[kind] = 1
        return FleetSummary(len(self._fleet.vehicles), len(self._fleet.items), by_kind)

    def total_daily_energy_kwh(self):
        total = 0
        for asset in self._fleet.assets:
            if isinstance(asset, EnergyConsumer):
                total = total + asset.daily_energy_kwh
        return total

    def beginner_friendly_vehicles(self):
        result = []
        for vehicle in self._fleet.vehicles:
            if self._beginner_policy.is_suitable(vehicle):
                result.append(vehicle)
        return result

    def inventory(self):
        return sorted(self._fleet.assets, key=by_number)


def by_number(asset):
    return asset.inventory_number